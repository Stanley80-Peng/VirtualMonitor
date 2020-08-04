from PyQt5.QtWidgets import QFileDialog, QMessageBox
from windowContents import *
from multiprocessing import Queue
from Animate import *
from Data_shadow import *
from Data_planner import *
import os
import sys
import datetime as dt


class Ui_ToolWindow(Ui_Form):

    def initUi(self, Form):
        self.setupUi(Form)
        self.globals()
        self.connectButtons()
        self.getDefaults()
        self.checkMapFolder()
        self.debug()

    def debug(self):
        self.lineEdit_date.setText('0731')

    def checkMapFolder(self):
        if not os.path.exists(self.mapPath):
            QMessageBox.information(None, '', 'Please set the correct map path in \"config.txt\"')
            exit(1)

    def globals(self):
        self.mapPath = None
        self.mes = Queue()
        self.mapid = None
        self.isRunning = False
        self.filepath = None

    def connectButtons(self):
        self.button_browse.clicked.connect(self.browse)
        self.button_init.clicked.connect(self.init)
        self.button_start.clicked.connect(self.start)
        self.button_pause.clicked.connect(lambda: self.putMes('pause'))
        self.slider_speed.valueChanged.connect(self.speedChange)
        self.button_forw15.clicked.connect(lambda: self.jump(str(15)))
        self.button_forw10.clicked.connect(lambda: self.jump(str(600)))
        self.button_forw1h.clicked.connect(lambda: self.jump(str(3600)))
        self.button_back15.clicked.connect(lambda: self.jump(str(-15)))
        self.button_back3.clicked.connect(lambda: self.jump(str(-180)))
        self.button_back30.clicked.connect(lambda: self.jump(str(-1800)))
        self.button_skip.clicked.connect(lambda: self.putMes('skip'))
        self.button_clear.clicked.connect(lambda: self.putMes('clear'))
        self.button_set.clicked.connect(self.set_auto_clear)
        self.button_stamp.clicked.connect(lambda: self.putMes('stamp'))

    def getDefaults(self):
        f = open('config.txt', 'r', encoding='UTF-8')
        if not f:
            print('Fail to open\'config.txt\'')
            return
        lines = f.readlines()
        self.lineEdit_filepath.setText(str(lines[0].split('\'')[1]))
        self.mapPath = str(lines[1].split('\'')[
                               1])
        self.lineEdit_mapid.setText(str(lines[2].split('\'')[1]))
        showMode = str(lines[3].split('\'')[1])
        f.close()
        if showMode == 'planner':
            self.radio_planner.setChecked(True)
        elif showMode == 'shadow':
            self.radio_shadow.setChecked(True)
        self.lineEdit_auto.setText(str(lines[4].split('\'')[1]))

    def browse(self):  # 以工作者目录为起始目录浏览planner文件夹的位置
        print('browse')  # debug
        start_path = os.path.expanduser('~')
        dir_choose = QFileDialog.getExistingDirectory(None, "选取文件夹", start_path)
        if dir_choose == "":
            return
        print('filepath = ' + dir_choose)  # debug
        self.lineEdit_filepath.setText(dir_choose)

    def init(self):
        print('init')
        self.mapid = self.lineEdit_mapid.text()
        self.filepath = self.lineEdit_filepath.text()

        if not os.path.exists(self.mapPath + '/' + str(self.mapid) + '.png'):
            QMessageBox.information(None, '', 'No available map in the \"maps\" folder!')
            return

        if not os.path.exists(self.filepath):
            QMessageBox.information(None, '', 'Path does not exist!')
            return

        if not os.path.isdir(self.filepath):
            QMessageBox.information(None, '', 'Please select a folder!')
            return

        if self.radio_planner.isChecked():
            proc_data_in_planner_mode = Data_planner(self.filepath)
            del proc_data_in_planner_mode
        elif self.radio_shadow.isChecked():
            proc_data_in_shadow_mode = Data_slam(self.filepath)
            del proc_data_in_shadow_mode
        else:
            QMessageBox.information(None, '', 'Please select replay mode!')

    def start(self):
        print('start')

        if not self.mes.empty():
            self.isRunning = False
            while not self.mes.empty():
                self.mes.get()

        if self.isRunning:  # 为防止将start误认为resume按下而新建模拟窗口，特设此检查
            QMessageBox.information(None, '', 'Animation is already running')
            return

        self.mapid = self.lineEdit_mapid.text()
        if not os.path.exists(self.mapPath + '/' + str(self.mapid) + '.png'):
            QMessageBox.information(None, '', 'No available map in the \"maps\" folder!\n')
            return

        if self.radio_planner.isChecked():

            if not os.path.exists('./positions/planner'):
                QMessageBox.information(None, 'ERROR', 'Please check the infos above and init!')
                return

            showDay = self.lineEdit_date.text()
            show = Animate('planner', showDay)

            if show.getData(self.mapid) == 0:
                QMessageBox.information(None, 'ERROR', 'No data of entered date!')
                return

            self.isRunning = True
            show.start(mes=self.mes, mapid=self.mapid)

        elif self.radio_shadow.isChecked():

            if not os.path.exists('./positions/shadow'):
                QMessageBox.information(None, 'ERROR', 'Please check the infos above and init!')
                return

            show = Animate('shadow', -1)
            show.getData(self.mapid)
            self.isRunning = True
            show.start(mes=self.mes, mapid=self.mapid)

    def speedChange(self):
        expo = self.slider_speed.value()
        speed = int(pow(2, expo - 1))
        print('change speed to %dx' % speed)
        self.mes.put('speed')
        self.mes.put(str(speed))

    def jump(self, sec):
        print('jump ' + sec + ' seconds')
        self.mes.put('jump')
        self.mes.put(sec)

    def set_auto_clear(self):
        clearTime = self.lineEdit_auto.text()
        print('set auto clear time: %ssec' % clearTime)
        self.mes.put('auto')
        self.mes.put(clearTime)

    def putMes(self, message):
        print('Put message: ' + message)
        self.mes.put(message)


def show_ToolWindow():  # 此函数为生成 QWidget 的标准函数，非必要时请尽量不要修改
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_ToolWindow()
    ui.initUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    show_ToolWindow()
