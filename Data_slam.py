import os
import time
import struct

class Data_slam(object):
    def __init__(self, path):
        procShadow(path)

def procShadow(path):
    in_file = open(path + '/' + 'slamRecord.bin', 'rb')
    out_file = open('./positions_shadow.csv', 'w')
    # out_file.write('sec,nsec,x,y,z,q0,q1,q2,q3\n')  #
    while True:
        temp = in_file.read(4)
        if not temp:
            break
        unpack = struct.unpack('=I', struct.pack('4B', *temp))
        out_file.write('%d,' % unpack[0])
        # print('%u,' % unpack, end='')  #
        temp = in_file.read(4)
        unpack = struct.unpack('=I', struct.pack('4B', *temp))
        data_float = float(unpack[0]) / pow(10, 9)
        out_file.write('%s,' % str(data_float)[2:7])
        # print('%u,' % unpack, end='')  #
        for i in range(7):
            temp = in_file.read(4)
            unpack = struct.unpack('=f', struct.pack('4B', *temp))
            out_file.write('%.4f,' % unpack[0])
            # print('%f,' % unpack, end='')  #
        out_file.write('\n')
        # print('\n')  #
    in_file.close()
    out_file.close()


if __name__ == '__main__':
    data = Data_slam('../2020-07-28-16-31-11')