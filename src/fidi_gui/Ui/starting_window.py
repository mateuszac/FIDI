# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'starting_window.ui',
# licensing of 'starting_window.ui' applies.
#
# Created: Wed Sep 18 23:20:18 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_StartingWindow(object):
    def setupUi(self, StartingWindow):
        StartingWindow.setObjectName("StartingWindow")
        StartingWindow.setWindowModality(QtCore.Qt.NonModal)
        StartingWindow.resize(701, 461)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(26)
        StartingWindow.setFont(font)
        self.Label = QtWidgets.QLabel(StartingWindow)
        self.Label.setGeometry(QtCore.QRect(310, 50, 71, 51))
        font = QtGui.QFont()
        font.setFamily("Constantia")
        font.setPointSize(26)
        font.setWeight(50)
        font.setBold(False)
        self.Label.setFont(font)
        self.Label.setObjectName("Label")
        self.PlateButton = QtWidgets.QPushButton(StartingWindow)
        self.PlateButton.setGeometry(QtCore.QRect(100, 190, 200, 120))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlateButton.sizePolicy().hasHeightForWidth())
        self.PlateButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.PlateButton.setFont(font)
        self.PlateButton.setCheckable(True)
        self.PlateButton.setObjectName("PlateButton")
        self.ShieldButton = QtWidgets.QPushButton(StartingWindow)
        self.ShieldButton.setGeometry(QtCore.QRect(390, 190, 200, 120))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ShieldButton.sizePolicy().hasHeightForWidth())
        self.ShieldButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.ShieldButton.setFont(font)
        self.ShieldButton.setCheckable(True)
        self.ShieldButton.setObjectName("ShieldButton")
        self.InfoButton = QtWidgets.QPushButton(StartingWindow)
        self.InfoButton.setGeometry(QtCore.QRect(580, 410, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.InfoButton.setFont(font)
        self.InfoButton.setCheckable(True)
        self.InfoButton.setObjectName("InfoButton")

        self.retranslateUi(StartingWindow)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow):
        StartingWindow.setWindowTitle(QtWidgets.QApplication.translate("StartingWindow", "Form", None, -1))
        self.Label.setText(QtWidgets.QApplication.translate("StartingWindow", "FIDI", None, -1))
        self.PlateButton.setText(QtWidgets.QApplication.translate("StartingWindow", "PLATE", None, -1))
        self.ShieldButton.setText(QtWidgets.QApplication.translate("StartingWindow", "SHIELD", None, -1))
        self.InfoButton.setText(QtWidgets.QApplication.translate("StartingWindow", "about FIDI", None, -1))

