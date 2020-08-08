import os
import re
import time
import multiprocessing as mp
from multiprocessing import Pool


class Data_planner(object):
    def __init__(self, path):
        # self.starttime = time.perf_counter()  #
        self.fileCount = -1
        self.files = self.sort_dir(path)
        self.pool_files(path)
        # print(time.perf_counter() - self.starttime)  #

    def sort_dir(self, path):
        DIR = os.listdir(path)
        self.fileCount = len(DIR)
        return sorted(DIR)

    def pool_files(self, path):
        p = Pool(mp.cpu_count())
        for i in range(self.fileCount):
            if self.files[i].find('planner') + 1 and self.files[i].find('root') + 1 \
                    and self.files[i].find('INFO') + 1:
                p.apply_async(proc_file, args=(path, self.files[i],))
        p.close()
        p.join()
    
def proc_file(path, filename):
    def appe(data_line, line_num):
        pattern = re.compile(r'[(][^)]*[)]')
        find_list = pattern.findall(data_line)
        x_y_theta = find_list[1].split(',')
        v_omega = find_list[3].split(',')
        get_time = data_line.split(' ')
        after_ignore = get_time[1].split('.')
        day_list.append(data_line[1:5])
        time_list.append(after_ignore[0])
        x_list.append(x_y_theta[0][1:])
        y_list.append(x_y_theta[1][1:])
        theta_list.append(x_y_theta[2][1:-1])
        v_list.append(v_omega[0][1:])
        line_list.append(line_num)
        other_list.append('0')

    def appe_load():
        if len(x_list):
            other_list[len(x_list)-1] = '1'

    def appe_swapMap(mapid):
        if len(x_list):
            other_list[len(x_list)-1] = mapid
        
    def write_csv(name):  # 把有用的数据写到positions文件夹内的csv文件中
        if not os.path.exists('./positions'):
            os.mkdir('./positions')
        if not os.path.exists('./positions/planner'):
            os.mkdir('./positions/planner')
        out_file = open('./positions/planner/' + name + '.csv', 'w', encoding='UTF-8')
        # out_file.write('day,time,x,y,theta,v\n')  #
        for i in range(len(x_list)):
            out_file.write(day_list[i] + ',')
            out_file.write(time_list[i] + ',')
            out_file.write(x_list[i] + ',')
            out_file.write(y_list[i] + ',')
            out_file.write(theta_list[i] + ',')
            out_file.write(v_list[i] + ',')
            out_file.write(str(name).split('root.')[1] + ',')
            out_file.write(str(line_list[i]) + ',')
            out_file.write(str(other_list[i]) + '\n')
        out_file.close()

    day_list = []
    time_list = []
    x_list = []
    y_list = []
    theta_list = []
    v_list = []
    line_list = []
    other_list = []
    linenum = 0
    f = open(path + '/' + filename)
    # print('open file ' + filename)  #
    while True:
        line = f.readline()
        linenum += 1
        if not line:
            break
        if re.search('(x, y, theta)', line):
            appe(line, linenum)
        elif re.search('Forklift Unload Success', line):
            appe_load()
        elif re.search('localization', line):
            appe_swapMap(line.split('mapid: ')[1][0:5])
    f.close()
    write_csv(filename)


if __name__ == '__main__':
    data = Data_planner('../planner')
