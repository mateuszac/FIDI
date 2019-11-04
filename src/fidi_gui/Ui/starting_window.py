# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'starting_window.ui',
# licensing of 'starting_window.ui' applies.
#
# Created: Mon Nov  4 18:47:45 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_StartingWindow(object):
    def setupUi(self, StartingWindow):
        StartingWindow.setObjectName("StartingWindow")
        StartingWindow.resize(657, 392)
        self.centralwidget = QtWidgets.QWidget(StartingWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.ShieldButton = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ShieldButton.sizePolicy().hasHeightForWidth())
        self.ShieldButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.ShieldButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/button_icons/sprites/button_icons/shield_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ShieldButton.setIcon(icon)
        self.ShieldButton.setIconSize(QtCore.QSize(200, 200))
        self.ShieldButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ShieldButton.setObjectName("ShieldButton")
        self.gridLayout.addWidget(self.ShieldButton, 2, 0, 1, 1)
        self.PlateButton = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlateButton.sizePolicy().hasHeightForWidth())
        self.PlateButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.PlateButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/button_icons/sprites/button_icons/plate_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlateButton.setIcon(icon1)
        self.PlateButton.setIconSize(QtCore.QSize(200, 200))
        self.PlateButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.PlateButton.setObjectName("PlateButton")
        self.gridLayout.addWidget(self.PlateButton, 2, 2, 1, 1)
        self.ShellButton = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ShellButton.sizePolicy().hasHeightForWidth())
        self.ShellButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.ShellButton.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/button_icons/sprites/button_icons/shell_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ShellButton.setIcon(icon2)
        self.ShellButton.setIconSize(QtCore.QSize(200, 200))
        self.ShellButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ShellButton.setObjectName("ShellButton")
        self.gridLayout.addWidget(self.ShellButton, 2, 3, 1, 1)
        self.InfoButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.InfoButton.setFont(font)
        self.InfoButton.setCheckable(True)
        self.InfoButton.setObjectName("InfoButton")
        self.gridLayout.addWidget(self.InfoButton, 4, 3, 1, 1)
        self.Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Constantia")
        font.setPointSize(26)
        font.setWeight(50)
        font.setBold(False)
        self.Label.setFont(font)
        self.Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Label.setObjectName("Label")
        self.gridLayout.addWidget(self.Label, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        StartingWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(StartingWindow)
        self.statusbar.setObjectName("statusbar")
        StartingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StartingWindow)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow):
        StartingWindow.setWindowTitle(QtWidgets.QApplication.translate("StartingWindow", "MainWindow", None, -1))
        self.ShieldButton.setText(QtWidgets.QApplication.translate("StartingWindow", "SHIELD", None, -1))
        self.PlateButton.setText(QtWidgets.QApplication.translate("StartingWindow", "PLATE", None, -1))
        self.ShellButton.setText(QtWidgets.QApplication.translate("StartingWindow", "SHELL", None, -1))
        self.InfoButton.setText(QtWidgets.QApplication.translate("StartingWindow", "about FIDI", None, -1))
        self.Label.setText(QtWidgets.QApplication.translate("StartingWindow", "FIDI", None, -1))

import Images_rc
