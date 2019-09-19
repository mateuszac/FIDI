# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plate_window.ui',
# licensing of 'plate_window.ui' applies.
#
# Created: Thu Sep 19 23:06:21 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainPlateWindow(object):
    def setupUi(self, MainPlateWindow):
        MainPlateWindow.setObjectName("MainPlateWindow")
        MainPlateWindow.resize(800, 600)
        self.PlateWindow = QtWidgets.QWidget(MainPlateWindow)
        self.PlateWindow.setObjectName("PlateWindow")
        self.pushButton = QtWidgets.QPushButton(self.PlateWindow)
        self.pushButton.setGeometry(QtCore.QRect(350, 390, 91, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.PlateWindow)
        self.label.setGeometry(QtCore.QRect(230, 230, 361, 71))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        MainPlateWindow.setCentralWidget(self.PlateWindow)
        self.menubar = QtWidgets.QMenuBar(MainPlateWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuGeometry = QtWidgets.QMenu(self.menubar)
        self.menuGeometry.setObjectName("menuGeometry")
        self.menuLoads = QtWidgets.QMenu(self.menubar)
        self.menuLoads.setObjectName("menuLoads")
        MainPlateWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainPlateWindow)
        self.statusbar.setObjectName("statusbar")
        MainPlateWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuGeometry.menuAction())
        self.menubar.addAction(self.menuLoads.menuAction())

        self.retranslateUi(MainPlateWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), MainPlateWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainPlateWindow)

    def retranslateUi(self, MainPlateWindow):
        MainPlateWindow.setWindowTitle(QtWidgets.QApplication.translate("MainPlateWindow", "MainWindow", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainPlateWindow", "Close window", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainPlateWindow", "Work in progress...", None, -1))
        self.menuGeometry.setTitle(QtWidgets.QApplication.translate("MainPlateWindow", "Geometry", None, -1))
        self.menuLoads.setTitle(QtWidgets.QApplication.translate("MainPlateWindow", "Loads", None, -1))

