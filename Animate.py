import os
import time
from math import *
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.animation import FuncAnimation


class Animate(object):
    def __init__(self, mode, date):
        self.time_list = []
        self.x_list = []
        self.y_list = []
        self.v_list = []
        self.theta_list = []
        self.file_list = []
        self.line_list = []
        self.other_list = []
        self.load_x = []
        self.load_y = []
        self.imgHeight = 0
        self.imgWidth = 0
        self.mapPath = ''
        self.day_num = int(date)
        self.beg_index = int(0)
        self.end_index = 1
        self.dataCount = int(0)
        self.auto_del = int(0)
        self.pause_flag = False
        self.hide_path = False
        self.hide_load = False
        self.load_here = False
        self.sing_incre = int(0)
        self.logSpeed = int(0)
        self.baseSpeed = float(0)
        self.mode = str(mode)
        self.x_excur = float(0)
        self.y_excur = float(0)
        self.max_fps = int(0)
        self.sleepTime = float(0)
        self.len_robot = int(0)
        self.wid_robot = int(0)
        self.get_config()

    def get_config(self):
        f = open('config.txt', 'r', encoding='UTF-8')
        lines = f.readlines()
        self.mapPath = lines[1].split('\'')[1]
        self.auto_del = int(lines[4].split('\'')[1])
        self.max_fps = int(lines[9].split('\'')[1])
        if self.max_fps > 36:
            self.max_fps = 36
        if self.mode == 'planner':
            self.logSpeed = int(lines[5].split('\'')[1])
            self.baseSpeed = float(lines[6].split('\'')[1])
        else:
            self.logSpeed = int(lines[7].split('\'')[1])
            self.baseSpeed = float(lines[8].split('\'')[1])
        self.len_robot = int(lines[10].split('\'')[1]) / 2
        self.wid_robot = int(lines[10].split('\'')[3]) / 2
        f.close()

    def getData(self, mapid):
        img = Image.open(self.mapPath + '/' + str(mapid) + '.png')
        self.imgHeight = int(img.height)  # 图片的高
        self.imgWidth = int(img.width)
        if self.mode == 'planner':
            return self.plan_get()
        elif self.mode == 'shadow':
            self.slam_get(mapid)

    def plan_get(self):
        DIR = os.listdir('./positions/planner')
        DIR.sort()
        for file in DIR:
            with open('./positions/planner/' + file, encoding='UTF-8') as f:
                self.proc_csv_plan(f)
        return self.dataCount

    def proc_csv_plan(self, f):
        while True:
            line = f.readline()
            if not line:
                break
            if not int(line[0:4]) == self.day_num:
                continue
            line = line.strip('\n')
            info = line.split(',')
            self.time_list.append(str(info[1]))
            self.x_list.append(int(info[2]))
            self.y_list.append(int(info[3]))
            self.v_list.append(float(info[5]))
            theta_now = float(info[4])
            if theta_now < 0:
                theta_now += 2 * pi
            self.theta_list.append(theta_now)
            self.file_list.append(info[6])
            self.line_list.append(info[7])
            self.other_list.append(info[8])
            self.dataCount += 1

    def slam_get(self, mapid):
        DIR = os.listdir('./positions/shadow')
        DIR.sort()
        for file in DIR:
            with open('./positions/shadow/' + file, encoding='UTF-8') as f:
                self.proc_csv_slam(f, mapid)

    def proc_csv_slam(self, f, mapid):
        self.get_excur(mapid)
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip('\n')
            info = line.split(',')
            self.time_list.append(str(info[0]) + '.' + str(info[1]))
            self.x_list.append(int(float(info[2]) * 50 - self.x_excur * 50))
            self.y_list.append(int(self.imgHeight - (float(info[3]) * 50 - self.y_excur * 50)))
            self.theta_list.append(float(self.get_theta(info)))
            self.dataCount += 1
        f.close()

    def get_excur(self, mapid):
        conf = open('config.txt', 'r', encoding='UTF-8')
        conf.readline()
        line = conf.readline()
        self.mapPath = line.split('\'')[1]
        conf.close()
        mapJson = open(self.mapPath + '/' + str(mapid) + '.json')
        line = mapJson.readline()
        self.x_excur = float(line.split(':')[3][0:9])
        self.y_excur = float(line.split(':')[4][0:9])

    def get_theta(self, info):
        theta = -2 * atan2(float(info[7]), float(info[8]))
        if theta < 0:
            theta += 2 * pi
        return str(theta)

    def start(self, mes, mapid):
        def jump():
            sec = int(mes.get())
            self.end_index += sec * self.logSpeed
            if self.end_index >= self.dataCount:
                self.end_index = self.dataCount - 1
            if self.end_index <= 1:
                self.end_index = 1
            self.beg_index = self.end_index  # 以防非自动清除路径模式下出现故障

        def speed():
            spd = mes.get()
            adjustFrame(spd)

        def adjustFrame(speed):
            sec_incre = float(speed) * float(self.baseSpeed) * float(self.logSpeed)
            self.sing_incre = ceil(sec_incre / float(self.max_fps))
            actual_rate = sec_incre / float(self.sing_incre)
            self.sleepTime = float(1000) / actual_rate - 27

        def ajustFrame(speed):
            self.sing_incre = ceil(float(speed) * float(self.baseSpeed)
                                   * float(self.logSpeed) / float(self.max_fps))
            self.sleepTime = float(1000) * float(self.sing_incre) / float(speed) \
                             / float(self.baseSpeed) / float(self.logSpeed) - 1

        def skip():
            if self.mode == 'planner':
                while True:
                    if not self.v_list[self.end_index]:
                        self.end_index += 1
                    else:
                        break

        def auto():
            sec = int(mes.get())
            self.auto_del = int(sec * self.logSpeed)

        def getScope():
            if self.auto_del:
                if self.end_index > self.logSpeed * self.auto_del:
                    xsco, ysco = self.x_list[self.end_index - self.logSpeed * self.auto_del:self.end_index], \
                           self.y_list[self.end_index - self.logSpeed * self.auto_del:self.end_index]
                else:
                    xsco, ysco = self.x_list[0:self.end_index], self.y_list[0:self.end_index]
            else:
                xsco, ysco = self.x_list[self.beg_index:self.end_index], \
                       self.y_list[self.beg_index:self.end_index]
            xsco.append((self.x_list[self.end_index] + self.x_list[self.end_index - 1]) / 2)
            ysco.append((self.y_list[self.end_index] + self.y_list[self.end_index - 1]) / 2)
            return xsco, ysco

        def check_mes():
            if not mes.empty():
                message = mes.get()
                if message == 'pause':
                    self.pause_flag = True if self.pause_flag is False else False
                elif message == 'jump':
                    jump()
                elif message == 'speed':
                    speed()
                elif message == 'skip':
                    skip()
                elif message == 'clear_path':
                    self.beg_index = self.end_index
                    self.auto_del = 0
                elif message == 'hide_path':
                    self.hide_path = True if self.hide_path is False else False
                elif message == 'clear_load':
                    self.load_x.clear()
                    self.load_y.clear()
                elif message == 'hide_load':
                    self.hide_load = True if self.hide_load is False else False
                elif message == 'auto':
                    auto()
                elif message == 'stamp':
                    print(self.time_list[self.end_index])
                    if not os.path.exists('figures'):
                        os.mkdir('figures')
                    times = str(self.time_list[self.end_index]).split(':')
                    if self.mode == 'planner':
                        plt.savefig('figures' + '/' + 'planner-' + str(self.day_num) + '-' +
                                times[0] + times[1] + times[2][0:3] + '.png', dpi=300)
                    else:
                        plt.savefig('figures' + '/' + 'shadow_slam-' +
                                    times[0] + times[1] + times[2][0:3] + '.png', dpi=300)
            if not self.pause_flag:
                self.end_index += self.sing_incre
            if self.end_index >= self.dataCount:
                self.end_index = self.dataCount - 1
            if self.mode == 'planner':
                if self.other_list[self.end_index] == '1':
                    self.load_x.append(self.x_list[self.end_index])
                    self.load_y.append(self.y_list[self.end_index])
                elif not self.other_list[self.end_index] == '0':
                    new_im = plt.imread(self.mapPath + '/' + self.other_list[self.end_index] + '.png')
                    plt.imshow(new_im)

        '''def get_arrow():
            return [[self.x_list[self.end_index],
                     self.x_list[self.end_index] +
                     cos(self.theta_list[self.end_index]) * self.len_robot],
                    [self.y_list[self.end_index],
                     self.y_list[self.end_index] +
                     sin(self.theta_list[self.end_index]) * self.len_robot]]'''

        def get_border():
            #print(self.theta_list[self.end_index])
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

        def update(no_use):
            check_mes()

            xsco, ysco = getScope()
            if self.hide_path:
                line.set_data([], [])
            else:
                line.set_data(xsco, ysco)
            if self.mode == 'planner':
                if self.hide_load:
                    load.set_data([], [])
                else:
                    load.set_data(self.load_x, self.load_y)

            '''arrow_x, arrow_y = get_arrow()
            arrow.set_data(arrow_x, arrow_y)'''

            border_x, border_y, head_x, head_y = get_border()
            head.set_data(head_x, head_y)
            border.set_data(border_x, border_y)
            # point.set_data(self.x_list[self.end_index], self.y_list[self.end_index])
            text = 'time: %s   (x, y) = (%4d, %4d)   theta = %.04lf' %(str(self.time_list[self.end_index]),
                                                                   self.x_list[self.end_index],
                                                                   self.y_list[self.end_index],
                                                                   self.theta_list[self.end_index])
            txt.set_text(text)
            if self.mode == 'planner':
                text2 = 'in file: \"%30s\"  line: %7s' % (self.file_list[self.end_index], self.line_list[self.end_index])
                txt2.set_text(text2)

            time.sleep(self.sleepTime / float(1000))
            if self.mode == 'planner':
                return line, txt, head, border, txt2, load,  # point, arrow,
            else:
                return line, txt, head, border,

        fig, ax = plt.subplots(figsize=(self.imgWidth / 300, self.imgHeight / 300))
        line, = ax.plot([], [], linewidth=1, color='#a771fd')
        # point, = ax.plot([], [], 'o', markersize=10)
        # arrow, = ax.plot([], [], linewidth=1, color='black')
        head, = ax.plot([], [], linewidth=1.6, color='#ff00e6')  #ff00e6
        border, = ax.plot([], [], linewidth=1.6, color='#00b1fe')  #00b1fe
        if self.mode == 'planner':
            load, = ax.plot([], [], 'o', markersize=4, color='orange')
        txt = ax.text(30, 125, '  ', fontsize=8)
        if self.mode == 'planner':
            txt2 = ax.text(30, 220, '  ', fontsize=8)
        adjustFrame(1)
        ani = FuncAnimation(fig, update, frames=[i for i in range(0, 10000)],
                            interval=1, blit=True, repeat=True)
        im = plt.imread(self.mapPath + '/' + str(mapid) + '.png')
        plt.imshow(im)
        plt.axis('off')
        plt.show()
        mes.put('over')
