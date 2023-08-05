import ctypes
import struct
import serial
import numpy as np
from time import sleep
from toon.input.device import BaseDevice
from serial.tools import list_ports

# thanks to ROS http://docs.ros.org/fuerte/api/cyberglove/html/serial__glove_8hpp.html
# for commands
# http://web.cs.ucdavis.edu/~neff/papers/GloveCalibration_WangNeff_SCA2013.pdf
# for sensor layout
# https://static1.squarespace.com/static/559c381ee4b0ff7423b6b6a4/t/58ca1b16be6594e83fb42402/1489640216840/CyberGlove+III.pdf
# is mostly relevant, and also describes the responses following commands

thumb_fields = ['roll', 'mcp', 'pip']  # index "owns" abduction
finger_fields = ['mcp', 'pip', 'abd']  # index through pinky
palm_wrist = ['arch', 'pitch', 'yaw']


class ThumbData(ctypes.Structure):
    _fields_ = [(n, ctypes.c_double) for n in thumb_fields]


class FingerData(ctypes.Structure):
    _fields_ = [(n, ctypes.c_double) for n in finger_fields]


class WristData(ctypes.Structure):
    _fields_ = [(n, ctypes.c_double) for n in palm_wrist]


fingers = [(n, FingerData) for n in ['index', 'middle', 'ring', 'pinky']]


class GloveData(ctypes.Structure):
    _fields_ = [('thumb', ThumbData)]
    _fields_.extend(fingers)
    _fields_.append(('wrist', WristData))


class Cyberglove(BaseDevice):
    sampling_frequency = 150
    shape = (1,)
    ctype = GloveData

    def __init__(self, port=None, **kwargs):
        super(Cyberglove, self).__init__(**kwargs)
        self.port = port  # TODO: auto-detect using serial.tools.list_ports
        self.dev = None

    def enter(self):
        if not self.port:
            self.port = next(x.device for x in list_ports.comports() if x.product == 'USB-Serial Controller')
        self.dev = serial.Serial(self.port, 115200, timeout=0.02)
        self.dev.reset_input_buffer()
        sleep(0.1)
        # test whether the device is connected/on
        self.dev.write(b'l ?\r')
        # should echo back & give result
        if not self.dev.read():
            raise ValueError('Make sure the device is switched on.')
        self.dev.write(b'f 0\r')  # stop filtering
        self.dev.write(b't 1152 1\r')  # 100 Hz
        self.dev.write(b'u 0\r')  # don't transmit status
        self.dev.write(b'l 1\r')  # light on
        sleep(0.1)
        self.dev.reset_input_buffer()
        self.dev.write(b'S')  # start streaming
        self.dev.flush()
        # not sure how to get rid of the rest of the garbage,
        # so spin until we find the first b'S'
        for i in range(40):
            tmp = self.dev.read()
            if tmp == b'S':
                self.dev.read(19)  # read the rest of the line
                break
        if i >= 39:
            raise ValueError('Did not find the start byte.')

    def read(self):
        # one byte (S)
        val = self.dev.read(1)
        time = self.clock()
        if val:
            data = self.dev.read(19)  # read remaining bytes ('18 sensors + \x00')
            data = struct.unpack('<' + 'B' * 18, data[:-1])
            data = [(d - 1.0)/254.0 for d in data]
            # pack into proper location
            thumb_data = ThumbData(data[0], data[1], data[2])  # data[3] is abduction
            index_data = FingerData(data[4], data[5], data[3])
            middle_data = FingerData(data[6], data[7], data[8])
            ring_data = FingerData(data[9], data[10], data[11])
            pinky_data = FingerData(data[12], data[13], data[14])
            wrist_data = WristData(data[15], data[16], data[17])
            return time, GloveData(thumb=thumb_data,
                                   index=index_data, middle=middle_data,
                                   ring=ring_data, pinky=pinky_data,
                                   wrist=wrist_data)

    def exit(self):
        self.dev.write(b'\x03')  # stop streaming
        self.dev.write(b'l 0\r')  # light off
        sleep(0.1)
        self.dev.reset_input_buffer()
        self.dev.reset_output_buffer()
        self.dev.close()


if __name__ == '__main__':
    import time
    from toon.input.mpdevice import MpDevice
    dev = MpDevice(Cyberglove())
    with dev:
        start = time.time()
        while time.time() - start < 10:
            dat = dev.read()
            if dat is not None:
                print(dat)  # access joints via dat[-1]['thumb']['mcp']
            time.sleep(0.016)  # pretend to have a screen
