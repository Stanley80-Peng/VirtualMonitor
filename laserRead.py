import os
import struct

class laserRead(object):
    def __init__(self, laser_path):
        self.file = open(laser_path, 'rb')
        self.first_flag = True
        self.start_hour = 0
        self.start_min = 0
        self.start_sec = 0

    def read_line(self):
        time_bin = self.file.read(2*4)
        if not time_bin:
            return None, None, None,
        time_tup = struct.unpack('II', time_bin)

        return time_stamp, time_explicit, data,
