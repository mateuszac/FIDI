# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yyy.ui',
# licensing of 'yyy.ui' applies.
#
# Created: Sat Jul 27 13:43:24 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(838, 652)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(160, 100, 501, 351))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(4)
        self.frame.setMidLineWidth(5)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 300, 401, 51))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(50, 30, 411, 121))
        font = QtGui.QFont()
        font.setFamily("RomanD")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setGeometry(QtCore.QRect(300, 230, 241, 51))
        self.checkBox.setObjectName("checkBox")
        self.cry_push_button = QtWidgets.QPushButton(self.frame)
        self.cry_push_button.setGeometry(QtCore.QRect(170, 170, 181, 23))
        self.cry_push_button.setCheckable(True)
        self.cry_push_button.setAutoDefault(False)
        self.cry_push_button.setDefault(False)
        self.cry_push_button.setFlat(False)
        self.cry_push_button.setObjectName("cry_push_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 838, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "It will be FIDI one day", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow",
                                                            "It is only for checking if everything works fine ", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "VERY FIRST FIDI GUI ", None, -1))
        self.checkBox.setText(QtWidgets.QApplication.translate("MainWindow", "This check box will do nothing :D", None, -1))
        self.cry_push_button.setText(QtWidgets.QApplication.translate("MainWindow", "DO NOT CLICK THAT BUTTON !", None, -1))

