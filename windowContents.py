# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windowContents.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(298, 434)
        self.lineEdit_filepath = QtWidgets.QLineEdit(Form)
        self.lineEdit_filepath.setGeometry(QtCore.QRect(12, 35, 200, 21))
        self.lineEdit_filepath.setObjectName("lineEdit_filepath")
        self.button_browse = QtWidgets.QPushButton(Form)
        self.button_browse.setGeometry(QtCore.QRect(212, 31, 81, 32))
        self.button_browse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_browse.setObjectName("button_browse")
        self.label_please = QtWidgets.QLabel(Form)
        self.label_please.setGeometry(QtCore.QRect(19, 15, 251, 16))
        self.label_please.setObjectName("label_please")
        self.label_mapid = QtWidgets.QLabel(Form)
        self.label_mapid.setGeometry(QtCore.QRect(62, 92, 60, 16))
        self.label_mapid.setObjectName("label_mapid")
        self.lineEdit_mapid = QtWidgets.QLineEdit(Form)
        self.lineEdit_mapid.setGeometry(QtCore.QRect(131, 90, 81, 21))
        self.lineEdit_mapid.setObjectName("lineEdit_mapid")
        self.button_init = QtWidgets.QPushButton(Form)
        self.button_init.setGeometry(QtCore.QRect(212, 86, 81, 32))
        self.button_init.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_init.setObjectName("button_init")
        self.lineEdit_date = QtWidgets.QLineEdit(Form)
        self.lineEdit_date.setEnabled(True)
        self.lineEdit_date.setGeometry(QtCore.QRect(141, 120, 71, 21))
        self.lineEdit_date.setObjectName("lineEdit_date")
        self.label_date = QtWidgets.QLabel(Form)
        self.label_date.setGeometry(QtCore.QRect(52, 122, 71, 16))
        self.label_date.setObjectName("label_date")
        self.button_start = QtWidgets.QPushButton(Form)
        self.button_start.setGeometry(QtCore.QRect(22, 152, 101, 41))
        self.button_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_start.setObjectName("button_start")
        self.button_pause = QtWidgets.QPushButton(Form)
        self.button_pause.setGeometry(QtCore.QRect(142, 152, 131, 41))
        self.button_pause.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_pause.setObjectName("button_pause")
        self.label_speed = QtWidgets.QLabel(Form)
        self.label_speed.setGeometry(QtCore.QRect(128, 193, 60, 16))
        self.label_speed.setObjectName("label_speed")
        self.slider_speed = QtWidgets.QSlider(Form)
        self.slider_speed.setGeometry(QtCore.QRect(31, 213, 231, 22))
        self.slider_speed.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider_speed.setMinimum(1)
        self.slider_speed.setMaximum(10)
        self.slider_speed.setPageStep(1)
        self.slider_speed.setOrientation(QtCore.Qt.Horizontal)
        self.slider_speed.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider_speed.setObjectName("slider_speed")
        self.label_multiple = QtWidgets.QLabel(Form)
        self.label_multiple.setGeometry(QtCore.QRect(32, 235, 241, 16))
        self.label_multiple.setObjectName("label_multiple")
        self.button_forw15 = QtWidgets.QPushButton(Form)
        self.button_forw15.setGeometry(QtCore.QRect(22, 261, 81, 41))
        self.button_forw15.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_forw15.setObjectName("button_forw15")
        self.button_forw10 = QtWidgets.QPushButton(Form)
        self.button_forw10.setGeometry(QtCore.QRect(107, 261, 81, 41))
        self.button_forw10.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_forw10.setObjectName("button_forw10")
        self.button_forw1h = QtWidgets.QPushButton(Form)
        self.button_forw1h.setGeometry(QtCore.QRect(192, 261, 81, 41))
        self.button_forw1h.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_forw1h.setObjectName("button_forw1h")
        self.button_back15 = QtWidgets.QPushButton(Form)
        self.button_back15.setGeometry(QtCore.QRect(22, 301, 81, 41))
        self.button_back15.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_back15.setObjectName("button_back15")
        self.button_back3 = QtWidgets.QPushButton(Form)
        self.button_back3.setGeometry(QtCore.QRect(107, 301, 81, 41))
        self.button_back3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_back3.setObjectName("button_back3")
        self.button_back30 = QtWidgets.QPushButton(Form)
        self.button_back30.setGeometry(QtCore.QRect(192, 301, 81, 41))
        self.button_back30.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_back30.setObjectName("button_back30")
        self.button_skip = QtWidgets.QPushButton(Form)
        self.button_skip.setGeometry(QtCore.QRect(12, 341, 91, 41))
        self.button_skip.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_skip.setObjectName("button_skip")
        self.button_clear = QtWidgets.QPushButton(Form)
        self.button_clear.setGeometry(QtCore.QRect(192, 341, 91, 41))
        self.button_clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_clear.setObjectName("button_clear")
        self.label_auto = QtWidgets.QLabel(Form)
        self.label_auto.setGeometry(QtCore.QRect(22, 397, 191, 16))
        self.label_auto.setObjectName("label_auto")
        self.lineEdit_auto = QtWidgets.QLineEdit(Form)
        self.lineEdit_auto.setGeometry(QtCore.QRect(122, 395, 61, 21))
        self.lineEdit_auto.setObjectName("lineEdit_auto")
        self.button_set = QtWidgets.QPushButton(Form)
        self.button_set.setGeometry(QtCore.QRect(204, 390, 71, 32))
        self.button_set.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_set.setObjectName("button_set")
        self.button_stamp = QtWidgets.QPushButton(Form)
        self.button_stamp.setGeometry(QtCore.QRect(107, 341, 81, 41))
        self.button_stamp.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_stamp.setObjectName("button_stamp")
        self.radio_planner = QtWidgets.QRadioButton(Form)
        self.radio_planner.setGeometry(QtCore.QRect(52, 61, 100, 20))
        self.radio_planner.setObjectName("radio_planner")
        self.radio_shadow = QtWidgets.QRadioButton(Form)
        self.radio_shadow.setGeometry(QtCore.QRect(142, 61, 121, 20))
        self.radio_shadow.setObjectName("radio_shadow")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Virtual Monitor"))
        self.button_browse.setText(_translate("Form", "Browse"))
        self.label_please.setText(_translate("Form", "Select data folder and mode:"))
        self.label_mapid.setText(_translate("Form", "Map ID:"))
        self.button_init.setText(_translate("Form", "Init"))
        self.label_date.setText(_translate("Form", "Select date:"))
        self.button_start.setText(_translate("Form", "Start"))
        self.button_pause.setText(_translate("Form", "Pause / Resume"))
        self.label_speed.setText(_translate("Form", "Speed"))
        self.label_multiple.setText(_translate("Form", "1x         4x         16x        64x            512x"))
        self.button_forw15.setText(_translate("Form", "15sec>>"))
        self.button_forw10.setText(_translate("Form", "10min>>"))
        self.button_forw1h.setText(_translate("Form", "1hr>>"))
        self.button_back15.setText(_translate("Form", "<<15sec"))
        self.button_back3.setText(_translate("Form", "<<3min"))
        self.button_back30.setText(_translate("Form", "<<30min"))
        self.button_skip.setText(_translate("Form", "Skip Stop"))
        self.button_clear.setText(_translate("Form", "Clear Path"))
        self.label_auto.setText(_translate("Form", "Auto Clear Path:                  sec"))
        self.button_set.setText(_translate("Form", "Set"))
        self.button_stamp.setText(_translate("Form", "Stamp"))
        self.radio_planner.setText(_translate("Form", "planner"))
        self.radio_shadow.setText(_translate("Form", "shadow-slam"))
