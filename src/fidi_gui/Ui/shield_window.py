# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shield_window.ui',
# licensing of 'shield_window.ui' applies.
#
# Created: Thu Sep 19 23:06:25 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainShieldWindow(object):
    def setupUi(self, MainShieldWindow):
        MainShieldWindow.setObjectName("MainShieldWindow")
        MainShieldWindow.resize(800, 554)
        self.ShieldWindow = QtWidgets.QWidget(MainShieldWindow)
        self.ShieldWindow.setObjectName("ShieldWindow")
        self.pushButton = QtWidgets.QPushButton(self.ShieldWindow)
        self.pushButton.setGeometry(QtCore.QRect(350, 390, 91, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.ShieldWindow)
        self.label.setGeometry(QtCore.QRect(230, 230, 361, 71))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        MainShieldWindow.setCentralWidget(self.ShieldWindow)
        self.menubar = QtWidgets.QMenuBar(MainShieldWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuGeometry = QtWidgets.QMenu(self.menubar)
        self.menuGeometry.setObjectName("menuGeometry")
        self.menuLoads = QtWidgets.QMenu(self.menubar)
        self.menuLoads.setObjectName("menuLoads")
        MainShieldWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainShieldWindow)
        self.statusbar.setObjectName("statusbar")
        MainShieldWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuGeometry.menuAction())
        self.menubar.addAction(self.menuLoads.menuAction())

        self.retranslateUi(MainShieldWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), MainShieldWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainShieldWindow)

    def retranslateUi(self, MainShieldWindow):
        MainShieldWindow.setWindowTitle(QtWidgets.QApplication.translate("MainShieldWindow", "MainWindow", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainShieldWindow", "Close window", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainShieldWindow", "Work in progress...", None, -1))
        self.menuGeometry.setTitle(QtWidgets.QApplication.translate("MainShieldWindow", "Geometry", None, -1))
        self.menuLoads.setTitle(QtWidgets.QApplication.translate("MainShieldWindow", "Loads", None, -1))

