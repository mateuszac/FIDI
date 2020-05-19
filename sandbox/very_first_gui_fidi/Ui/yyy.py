# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yyy.ui',
# licensing of 'yyy.ui' applies.
#
# Created: Sat Nov  2 15:01:46 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(834, 655)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("RomanD")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.cry_push_button = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/Ui/test_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cry_push_button.setIcon(icon)
        self.cry_push_button.setCheckable(True)
        self.cry_push_button.setAutoDefault(False)
        self.cry_push_button.setDefault(False)
        self.cry_push_button.setFlat(False)
        self.cry_push_button.setObjectName("cry_push_button")
        self.gridLayout.addWidget(self.cry_push_button, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 834, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "VERY FIRST FIDI GUI ", None, -1))
        self.checkBox.setText(QtWidgets.QApplication.translate("MainWindow", "This check box will do nothing :D", None, -1))
        self.cry_push_button.setText(QtWidgets.QApplication.translate("MainWindow", "DO NOT CLICK THAT BUTTON !", None, -1))

import test_resource_rc
