import os
import time
import struct


def readLaser(file_path):
    first_flag = True
    in_file = open(file_path, 'rb')
    out_file = open('./positions/shadow/2020-07-31-17-04-52-laser1.csv', 'w')
    '''    out_file.write('time1,stamp,time2,')
    for i in range(1081):
        out_file.write('data ' + str(i) + ',')
    out_file.write('\n')'''
    inihour = 17
    inimin = 4
    inisec = 52
    always_minus = -1
    data_count = 0
    while True:
        data_count += 1
        temp = in_file.read(4)
        if not temp:
            break
        unpack = struct.unpack('=I', struct.pack('4B', *temp))
        if first_flag:
            always_minus = int(unpack[0])
            first_flag = False
        cor_time = unpack[0] - always_minus
        cor_time += inihour * 3600 + inimin * 60 + inisec
        hour = int(cor_time / 3600)
        if hour > 23:
            hour -= 24
        min = int((cor_time % 3600 - cor_time % 60) / 60)
        if min > 59:
            min -= 60
        sec = int(cor_time % 60)
        if sec > 59:
            sec -= 60
        out_file.write('%02d:%02d:%02d,' % (hour, min, sec))  # time1
        out_file.write('%d,' % unpack[0])
        temp = in_file.read(4)
        unpack = struct.unpack('=I', struct.pack('4B', *temp))
        data_float = float(unpack[0]) / pow(10, 9)
        out_file.write('0.%s,' % str(data_float)[2:7])  # time2
        temp = in_file.read(4)
        frame_id_length = struct.unpack('=I', struct.pack('4B', *temp))[0]
        for i in range(frame_id_length):
            in_file.read(1)
        temp = in_file.read(4)
        # out_file.write('%.4f,' % struct.unpack('=f', struct.pack('4B', *temp))[0])  # angle_min
        temp = in_file.read(4)
        # out_file.write('%.4f,' % struct.unpack('=f', struct.pack('4B', *temp))[0])  # angle_max
        temp = in_file.read(4)
        # out_file.write('%.4f,' % struct.unpack('=f', struct.pack('4B', *temp))[0])  # angle_increment
        temp = in_file.read(4)
        # out_file.write('%.4f,' % struct.unpack('=f', struct.pack('4B', *temp))[0])  # time_increment
        temp = in_file.read(4)
        # out_file.write('%.4f,' % struct.unpack('=f', struct.pack('4B', *temp))[0])  # scan_time
        temp = in_file.read(4)
        # out_file.write('%.4f,' % struct.unpack('=f', struct.pack('4B', *temp))[0])  # range_min
        temp = in_file.read(4)
        # out_file.write('%.4f,' % struct.unpack('=f', struct.pack('4B', *temp))[0])  # range_max
        temp = in_file.read(4)
        # out_file.write('%.4f,' % struct.unpack('=f', struct.pack('4B', *temp))[0])
        ranges_length = struct.unpack('=I', struct.pack('4B', *temp))[0]
        for i in range(ranges_length):
            temp = in_file.read(4)
            out_file.write('%.4f,' % struct.unpack('=f', struct.pack('4B', *temp))[0])
        out_file.write('\n')
        temp = in_file.read(4)
        intensities_length = struct.unpack('=I', struct.pack('4B', *temp))[0]
        if intensities_length > 0:
            for i in range(intensities_length):
                in_file.read(4)



if __name__ == '__main__':
    print(time.perf_counter())
    readLaser('../ShadowData/2020-07-31-17-04-52/laser1Record.bin')
    print(time.perf_counter())
