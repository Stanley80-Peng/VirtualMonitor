import os
import time
import struct
from multiprocessing import Pool
import multiprocessing as mp


class DataShadow(object):
    def __init__(self, path):
        proc_dir(path)


def proc_dir(path):
    p = Pool(mp.cpu_count())
    DIR = os.listdir(path)
    for dir_in in DIR:
        if os.path.isdir(path + '/' + str(dir_in)):
            files = os.listdir(path + '/' + str(dir_in))
            for file in files:
                with open(path + '/' + str(dir_in) + '/' + file, 'rb') as f:
                    if f.name.split('/')[-1].find('slam') + 1:
                        proc_slam(f, str(dir_in), )
                    # p.apply_async(proc_slam, args=(f, str(dir),))
    p.close()
    p.join()


def proc_slam(in_file, dir_name):
    first_flag = True
    if not os.path.exists('./positions'):
        os.mkdir('./positions')
        os.mkdir('./positions/shadow')
    elif not os.path.exists('./positions/shadow'):
        os.mkdir('./positions/shadow')

    out_file = open('./positions/shadow/' + str(dir_name) + '-slam.csv', 'w', encoding='UTF-8')
    tup_time = str(dir_name).split('-')
    inihour = int(tup_time[3])
    inimin = int(tup_time[4])
    inisec = int(tup_time[5])
    always_minus = -1

    while True:
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
        out_file.write('%02d:%02d:%02d,' % (hour, min, sec))
        # #print('%u,' % unpack, end='')  #
        temp = in_file.read(4)
        unpack = struct.unpack('=I', struct.pack('4B', *temp))
        data_float = float(unpack[0]) / pow(10, 9)
        out_file.write('0.%s,' % str(data_float)[2:7])
        # #print('%u,' % unpack, end='')  #
        for i in range(7):
            temp = in_file.read(4)
            unpack = struct.unpack('=f', struct.pack('4B', *temp))
            out_file.write('%.4f,' % unpack[0])
            # #print('%f,' % unpack, end='')  #
        out_file.write('\n')
        # #print('\n')  #
    in_file.close()
    out_file.close()


if __name__ == '__main__':
    data = DataShadow('../ShadowData')
