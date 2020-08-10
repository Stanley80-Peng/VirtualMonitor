import os
import time
import matplotlib.pyplot as plt
import numpy as np
from math import *
from PIL import Image
from matplotlib.animation import FuncAnimation


class Animate(object):
    def __init__(self, mode, date):
        self.map_id = ''
        self.map_path = ''
        self.day_num = int(date)
        self.data_count = 0
        self.mode = mode

        self.time_list = []  # in csv col-2 [1]
        self.x_list = []  # in csv col-3 [2]
        self.y_list = []  # in csv col-4 [3]
        self.theta_list = []  # in csv col-5 [4]
        self.v_list = []  # in csv col-6 [5] (only in planner mode)
        self.file_list = []  # in csv col-7 [6] (only in planner mode)
        self.line_list = []  # in csv col-8 [7] (only in planner mode)
        self.map_list = []  # in csv col-9 [8] (only in planner mode)
        self.other_list = []  # in csv col-10 [9] (only in planner mode)

        self.loads_x = []  # (only in planner mode)
        self.loads_y = []  # (only in planner mode)

        self.x_excursion = 0  # (only in shadow mode)
        self.y_excursion = 0  # (only in shadow mode)

        self.img_height = 0  # used to adjust plot limits
        self.img_width = 0  # used to adjust plot limits

        self.beg_index = 0
        self.end_index = 0

        self.log_speed = 0
        self.base_speed = 0
        self.sing_aug = 0
        self.sleep_time = 0
        self.auto_del = 0
        self.max_fps = 0

        self.len_robot = 0
        self.wid_robot = 0

        self.pause_flag = False
        self.hide_path = False
        self.hide_loads = False  # (only in planner mode)

        self.fig_width = 10
        self.fig_height = 10

        self.get_config()

    def get_config(self):
        f = open('config.txt', 'r', encoding='UTF-8')
        lines = f.readlines()

        self.map_path = lines[1].split('\'')[1]
        self.auto_del = int(lines[4].split('\'')[1])

        if self.mode == 'planner':
            self.log_speed = int(lines[5].split('\'')[1])
            self.base_speed = float(lines[6].split('\'')[1])
        elif self.mode == 'shadow':
            self.log_speed = int(lines[7].split('\'')[1])
            self.base_speed = float(lines[8].split('\'')[1])

        self.max_fps = int(lines[9].split('\'')[1])
        self.len_robot = int(lines[10].split('\'')[1]) / 2
        self.wid_robot = int(lines[10].split('\'')[3]) / 2
        self.fig_width = int(lines[11].split('\'')[1])
        self.fig_height = int(lines[11].split('\'')[3])

        f.close()

    def plan_get(self):
        DIR = os.listdir('./positions/planner')
        DIR.sort()
        for file in DIR:
            with open('./positions/planner/' + file, encoding='UTF-8') as f:
                self.proc_csv_plan(f)
        return self.data_count

    def proc_csv_plan(self, f):
        lines = f.readlines()
        for line in lines:
            if not int(line[0:4]) == self.day_num:
                continue
            line = line.strip('\n')
            info = line.split(',')
            self.time_list.append(str(info[1]))
            self.x_list.append(int(info[2]))
            self.y_list.append(int(info[3]))
            self.theta_list.append(float(info[4]))
            self.v_list.append(float(info[5]))
            self.file_list.append(info[6])
            self.line_list.append(info[7])
            self.map_list.append(info[8])
            self.other_list.append(info[9])
            self.data_count += 1

    def shad_get(self, map_id):
        self.slam_get(map_id)

    def slam_get(self, map_id):
        DIR = os.listdir('./positions/shadow/slam')
        DIR.sort()
        for file in DIR:
            with open('./positions/shadow/slam/' + file, encoding='UTF-8') as f:
                self.proc_csv_slam(f, map_id)

    def proc_csv_slam(self, f, map_id):
        self.get_excursion(map_id)
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            info = line.split(',')
            self.time_list.append(info[0] + '.' + info[1])
            self.x_list.append(int(float(info[2]) * 50 - self.x_excursion))
            self.y_list.append(int(self.img_height - (float(info[3]) * 50 - self.y_excursion * 50)))
            self.theta_list.append(float(-2 * atan2(float(info[7]), float(info[8]))))
            self.data_count += 1
        f.close()

    def get_excursion(self, map_id):
        conf = open('config.txt', 'r', encoding='UTF-8')
        conf.readline()
        line = conf.readline()
        self.map_path = line.split('\'')[1]
        conf.close()
        mapJson = open(self.map_path + '/' + str(map_id) + '.json')
        line = mapJson.readline()
        self.x_excursion = float(line.split(':')[3][0:9])
        self.y_excursion = float(line.split(':')[4][0:9])

    def start(self, mes, map_id):

        def jump():
            sec = int(mes.get())
            self.end_index += sec * self.log_speed
            if self.end_index >= self.data_count:
                self.end_index = self.data_count - 1
            if self.end_index <= 1:
                self.end_index = 1
            if sec < 0:
                self.beg_index = self.end_index

        def adjustFrame(spd):
            sec_aug = float(spd) * float(self.base_speed) * float(self.log_speed)
            self.sing_aug = ceil(sec_aug / float(self.max_fps))
            actual_rate = sec_aug / float(self.sing_aug)
            self.sleep_time = float(1000) / actual_rate - 27

        def speed():
            new_speed = mes.get()
            adjustFrame(new_speed)

        def auto():
            sec = int(mes.get())
            self.auto_del = int(sec * self.log_speed)

        def pause():
            self.pause_flag = True if self.pause_flag is False else False

        def clear_path():
            self.beg_index = self.end_index
            self.auto_del = 0

        def hide_path():
            self.hide_path = True if self.hide_path is False else False

        def clear_loads():
            self.loads_x.clear()
            self.loads_y.clear()

        def hide_loads():
            self.hide_load = True if self.hide_load is False else False

        def stamp():
            print(self.time_list[self.end_index])
            if not os.path.exists('figures'):
                os.mkdir('figures')
            times = str(self.time_list[self.end_index]).split(':')
            if self.mode == 'planner':
                plt.savefig('figures' + '/' + 'planner-' + str(self.day_num) + '-' +
                            times[0] + times[1] + times[2][0:3] + '.png', dpi=300)
            elif self.mode == 'shadow':
                plt.savefig('figures' + '/' + 'shadow-' +
                            times[0] + times[1] + times[2][0:3] + '.png', dpi=300)

        func_dict = {
            'jump': jump,
            'speed': speed,
            'auto': auto,
            'pause': pause,
            'clear_path': clear_path,
            'hide_path': hide_path,
            'clear_loads': clear_loads,
            'hide_loads': hide_loads,
            'stamp': stamp,
        }

        def check_load():
            if self.other_list[self.end_index] == 'load':
                self.loads_x.append(self.x_list[self.end_index])
                self.loads_y.append(self.y_list[self.end_index])

        def check_mes():
            if not mes.empty():
                func = func_dict.get(mes.get())
                func()
            if not self.pause_flag:
                self.end_index += self.sing_aug
            if self.end_index >= self.data_count:
                self.end_index = self.data_count - 1
            if self.mode == 'planner':
                check_load()

        def get_path():
            if not self.hide_path:
                if self.auto_del:
                    begin = self.beg_index if self.beg_index > self.end_index - self.log_speed * \
                                              self.auto_del else self.end_index - self.log_speed * self.auto_del
                    return self.x_list[begin:self.end_index], self.y_list[begin:self.end_index]
                else:
                    return self.x_list[self.beg_index:self.end_index], \
                           self.y_list[self.beg_index:self.end_index]
            else:
                return [], []

        def get_edges():
            points_x = [0, 0, 0, 0, 0]
            points_y = [0, 0, 0, 0, 0]
            phi = atan(self.wid_robot / self.len_robot)
            theta_A = self.theta_list[self.end_index] - phi
            half_diag = sqrt(pow(self.len_robot, 2) + pow(self.wid_robot, 2)) / 2
            points_x[0] = points_x[4] = half_diag * cos(theta_A) + self.x_list[self.end_index]
            points_y[0] = points_y[4] = half_diag * sin(theta_A) + self.y_list[self.end_index]
            theta_B = self.theta_list[self.end_index] + pi + phi
            points_x[1] = half_diag * cos(theta_B) + self.x_list[self.end_index]
            points_y[1] = half_diag * sin(theta_B) + self.y_list[self.end_index]
            points_x[2] = 2 * self.x_list[self.end_index] - points_x[0]
            points_y[2] = 2 * self.y_list[self.end_index] - points_y[0]
            points_x[3] = 2 * self.x_list[self.end_index] - points_x[1]
            points_y[3] = 2 * self.y_list[self.end_index] - points_y[1]
            return points_x[0:4], points_y[0:4], points_x[3:5], points_y[3:5]

        def get_detail():
            return 'time: %s   (x, y) = (%4d, %4d)   theta = %.04lf' % (str(self.time_list[self.end_index]),
                                                                        self.x_list[self.end_index],
                                                                        self.y_list[self.end_index],
                                                                        self.theta_list[self.end_index])

        def get_file_line():
            return 'in file: \"%30s\"  line: %7s  Map ID: %5s' % (self.file_list[self.end_index],
                                                                  self.line_list[self.end_index],
                                                                  self.map_id)

        def get_loads():
            if not self.hide_loads:
                return self.loads_x, self.loads_y
            else:
                return [], []

        def switch_map():
            pass

        def update(no_use):
            check_mes()
            time.sleep(self.sleep_time / 1000)
            path.set_data(get_path())
            head.set_data(get_edges()[2:4])
            border.set_data(get_edges()[0:2])
            text_detail.set_text(get_detail())

            if self.mode == 'planner':
                text_file_line.set_text(get_file_line())
                loads.set_data(get_loads())

                if self.map_list[self.end_index] == self.map_id:
                    return path, head, border, text_detail, text_file_line, loads,
                else:
                    switch_map()
                    return path, head, border, text_detail, text_file_line, loads, img_show,

            elif self.mode == 'shadow':
                return path, head, border, text_detail,

        self.map_id = map_id
        fig, ax = plt.subplots(figsize=(10, 10))
        head, = ax.plot([], [], linewidth=1.6, color='#ff00e6')
        border, = ax.plot([], [], linewidth=1.6, color='#00b1fe')
        path, = ax.plot([], [], linewidth=1, color='#a771fd')
        text_detail = ax.text(30, 125, '  ', fontsize=8)
        if self.mode == 'planner':
            loads, = ax.plot([], [], 'o', markersize=4, color='orange')
            text_file_line = ax.text(30, 200, '  ', fontsize=6)
            im = plt.imread(self.map_path + '/' + str(self.map_id) + '.png')
            img_show = plt.imshow(im, 'gray')
        elif self.mode == 'shadow':
            im = plt.imread(self.map_path + '/' + self.map_id + '.png')
            img_show = plt.imshow(im)
        animation = FuncAnimation(fig, update, frames=[i for i in range(0, 1000)],
                                  interval=1, blit=True, repeat=True)
        plt.show()
        mes.put('over')
