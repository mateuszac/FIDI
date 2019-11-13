# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shell_window.ui',
# licensing of 'shell_window.ui' applies.
#
# Created: Sat Nov  2 16:43:35 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainShellWindow(object):
    def setupUi(self, MainShellWindow):
        MainShellWindow.setObjectName("MainShellWindow")
        MainShellWindow.resize(800, 600)
        self.ShellWindow = QtWidgets.QWidget(MainShellWindow)
        self.ShellWindow.setObjectName("ShellWindow")
        self.gridLayout = QtWidgets.QGridLayout(self.ShellWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.ShellWindow)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.ShellWindow)
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        MainShellWindow.setCentralWidget(self.ShellWindow)
        self.menubar = QtWidgets.QMenuBar(MainShellWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuGeometry = QtWidgets.QMenu(self.menubar)
        self.menuGeometry.setObjectName("menuGeometry")
        self.menuLoads = QtWidgets.QMenu(self.menubar)
        self.menuLoads.setObjectName("menuLoads")
        MainShellWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainShellWindow)
        self.statusbar.setObjectName("statusbar")
        MainShellWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuGeometry.menuAction())
        self.menubar.addAction(self.menuLoads.menuAction())

        self.retranslateUi(MainShellWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), MainShellWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainShellWindow)

    def retranslateUi(self, MainShellWindow):
        MainShellWindow.setWindowTitle(QtWidgets.QApplication.translate("MainShellWindow", "MainWindow", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainShellWindow", "Close window", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainShellWindow", "Work in progress...", None, -1))
        self.menuGeometry.setTitle(QtWidgets.QApplication.translate("MainShellWindow", "Geometry", None, -1))
        self.menuLoads.setTitle(QtWidgets.QApplication.translate("MainShellWindow", "Loads", None, -1))

