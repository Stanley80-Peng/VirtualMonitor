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
    save_sec = 0
    while True:
        temp = in_file.read(8)
        if not temp:
            break
        '''unpack1 = struct.unpack('=I', struct.pack('4B', *temp))
        # #print('%u,' % unpack, end='')  #
        temp = in_file.read(4)
        unpack2 = struct.unpack('=I', struct.pack('4B', *temp))'''
        unpack_time = struct.unpack('II', temp)
        sub_sec = int(str(unpack_time[1])[0:2])
        sub_sec -= sub_sec % 3
        now_sec = str(unpack_time[0]) + '.' + str(sub_sec)
        if now_sec == save_sec:
            in_file.read(4*7)
            continue
        save_sec = now_sec
        out_file.write('%s,' % now_sec)
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
