import os
import time
import math
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
        self.imgHeight = 0
        self.imgWidth = 0
        self.d = {
            'mapPath': '',
            'day_num': int(date),
            'beg_index': int(0),
            'end_index': int(0),
            'dataCount': int(0),
            'auto_del': int(0),
            'pause_flag': False,
            'sing_incre': int(0),
            'logSpeed': int(0),
            'baseSpeed': float(0),
            'mode': str(mode),
            'x_excur': float(0),
            'y_excur': float(0),
            'max_fps': int(0),
            'sleepTime': float(0),
            'len_robot': int(0),
            'wid_robot': int(0),
        }
        self.get_config()

    def get_config(self):
        f = open('config.txt', 'r', encoding='UTF-8')
        lines = f.readlines()
        self.d['mapPath'] = lines[1].split('\'')[1]
        self.d['auto_del'] = int(lines[4].split('\'')[1])
        self.d['max_fps'] = int(lines[9].split('\'')[1])
        if self.d['max_fps'] > 48:
            self.d['max_fps'] = 48
        if self.d['mode'] == 'planner':
            self.d['logSpeed'] = int(lines[5].split('\'')[1])
            self.d['baseSpeed'] = float(lines[6].split('\'')[1])
        else:
            self.d['logSpeed'] = int(lines[7].split('\'')[1])
            self.d['baseSpeed'] = float(lines[8].split('\'')[1])
        self.d['len_robot'] = int(lines[10].split('\'')[1])
        self.d['wid_robot'] = int(lines[10].split('\'')[3])
        f.close()

    def getData(self, mapid):
        img = Image.open(self.d['mapPath'] + '/' + str(mapid) + '.png')
        self.imgHeight = int(img.height)  # 图片的高
        self.imgWidth = int(img.width)
        if self.d['mode'] == 'planner':
            return self.plan_get()
        elif self.d['mode'] == 'shadow':
            self.slam_get(mapid)

    def plan_get(self):
        DIR = os.listdir('./positions/planner')
        DIR.sort()
        '''for file in DIR:
            print(file)'''
        for file in DIR:
            with open('./positions/planner/' + file, encoding='UTF-8') as f:
                self.proc_csv_plan(f)
        return self.d['dataCount']

    def proc_csv_plan(self, f):
        while True:
            line = f.readline()
            if not line:
                break
            if not int(line[0:4]) == self.d['day_num']:
                continue
            line = line.strip('\n')
            info = line.split(',')
            self.time_list.append(str(info[1]))
            self.x_list.append(int(info[2]))
            self.y_list.append(int(info[3]))
            self.v_list.append(float(info[5]))
            self.theta_list.append(float(info[4]))
            self.d['dataCount'] += 1

    def slam_get(self, mapid):
        self.get_excur(mapid)
        f = open('./positions/shadow/slam.csv', 'r')
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip('\n')
            info = line.split(',')
            self.time_list.append(str(info[0]) + '.' + str(info[1]))
            self.x_list.append(int(float(info[2]) * 50 - self.d['x_excur'] * 50))
            self.y_list.append(int(self.imgHeight - (float(info[3]) * 50 - self.d['y_excur'] * 50)))
            self.theta_list.append(float(self.get_theta(info)))
            self.d['dataCount'] += 1
        f.close()

    def get_excur(self, mapid):
        conf = open('config.txt', 'r', encoding='UTF-8')
        conf.readline()
        line = conf.readline()
        self.d['mapPath'] = line.split('\'')[1]
        conf.close()
        mapJson = open(self.d['mapPath'] + '/' + str(mapid) + '.json')
        line = mapJson.readline()
        self.d['x_excur'] = float(line.split(':')[3][0:9])
        self.d['y_excur'] = float(line.split(':')[4][0:9])

    def get_theta(self, info):
        theta = float(0)
        for i in range(5, 9):
            theta += float(info[i])
        return str(theta)

    def start(self, mes, mapid):
        def jump():
            sec = int(mes.get())
            self.d['end_index'] += sec * self.d['logSpeed']
            if self.d['end_index'] >= self.d['dataCount']:
                self.d['end_index'] = self.d['dataCount'] - 1
            if self.d['end_index'] <= 0:
                self.d['end_index'] = 0
            self.d['beg_index'] = self.d['end_index']  # 以防非自动清除路径模式下出现故障

        def speed():
            spd = mes.get()
            adjustFrame(spd)

        def adjustFrame(speed):
            sec_incre = float(speed) * float(self.d['baseSpeed']) * float(self.d['logSpeed'])
            self.d['sing_incre'] = math.ceil(sec_incre / float(self.d['max_fps']))
            actual_rate = sec_incre / float(self.d['sing_incre'])
            self.d['sleepTime'] = float(1000) / actual_rate - 20

        def ajustFrame(speed):
            self.d['sing_incre'] = math.ceil(float(speed) * float(self.d['baseSpeed'])
                                             * float(self.d['logSpeed']) / float(self.d['max_fps']))
            self.d['sleepTime'] = float(1000) * float(self.d['sing_incre']) / float(speed) \
                                  / float(self.d['baseSpeed']) / float(self.d['logSpeed']) - 1

        def skip():
            if self.d['mode'] == 'planner':
                while True:
                    if not self.v_list[self.d['end_index']]:
                        self.d['end_index'] += 1
                    else:
                        break

        def auto():
            sec = int(mes.get())
            self.d['auto_del'] = int(sec * self.d['logSpeed'])

        def getScope():
            if self.d['auto_del']:
                if self.d['end_index'] > self.d['logSpeed'] * self.d['auto_del']:
                    return self.x_list[self.d['end_index'] - self.d['logSpeed'] *
                                       self.d['auto_del']:self.d['end_index'] + 1], \
                           self.y_list[self.d['end_index'] - self.d['logSpeed'] *
                                       self.d['auto_del']:self.d['end_index'] + 1]
                else:
                    return self.x_list[0:self.d['end_index'] + 1], self.y_list[0:self.d['end_index'] + 1]
            else:
                return self.x_list[self.d['beg_index']:self.d['end_index'] + 1], \
                       self.y_list[self.d['beg_index']:self.d['end_index'] + 1]

        def check_mes():
            if not mes.empty():
                message = mes.get()
                if message == 'pause':
                    self.d['pause_flag'] = True if not self.d['pause_flag'] is True else False
                elif message == 'jump':
                    jump()
                elif message == 'speed':
                    speed()
                elif message == 'skip':
                    skip()
                elif message == 'clear':
                    self.d['beg_index'] = self.d['end_index']
                    self.d['auto_del'] = 0
                elif message == 'auto':
                    auto()
                elif message == 'stamp':
                    print(self.time_list[self.d['end_index']])
            if not self.d['pause_flag']:
                self.d['end_index'] += self.d['sing_incre']
            if self.d['end_index'] >= self.d['dataCount']:
                self.d['end_index'] = self.d['dataCount'] - 1

        def get_arrow():
            return [[self.x_list[self.d['end_index']],
                     self.x_list[self.d['end_index']] +
                     math.cos(self.theta_list[self.d['end_index']]) * self.d['len_robot'] / 4],
                    [self.y_list[self.d['end_index']],
                     self.y_list[self.d['end_index']] +
                     math.sin(self.theta_list[self.d['end_index']]) * self.d['len_robot'] / 4]]

        def get_border():
            pass

        def update(no_use):
            check_mes()
            xsco, ysco = getScope()
            line.set_data(xsco, ysco)
            point.set_data(self.x_list[self.d['end_index']], self.y_list[self.d['end_index']])
            arrow_data = get_arrow()
            arrow.set_data(arrow_data[0], arrow_data[1])
            txt.set_text(self.time_list[self.d['end_index']])
            time.sleep(self.d['sleepTime'] / float(1000))
            return line, point, txt, arrow,

        fig, ax = plt.subplots(figsize=(self.imgWidth / 400, self.imgHeight / 400))
        line, = ax.plot([], [], linewidth=2)
        point, = ax.plot([], [], 'o', markersize=10)
        arrow, = ax.plot([], [], linewidth=2, color='green')
        border, = ax.plot([], [], linewidth=1, color='black')
        txt = ax.text(10, 200, '  ', fontsize=10)
        adjustFrame(1)
        ani = FuncAnimation(fig, update, frames=[i for i in range(0, 10000)],
                            interval=1, blit=True, repeat=True)
        im = plt.imread(self.d['mapPath'] + '/' + str(mapid) + '.png')
        plt.imshow(im)
        plt.axis('off')
        plt.show()
        mes.put('over')
