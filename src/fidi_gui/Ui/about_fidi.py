# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_fidi.ui',
# licensing of 'about_fidi.ui' applies.
#
# Created: Thu Sep 19 23:06:14 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AboutFidi(object):
    def setupUi(self, AboutFidi):
        AboutFidi.setObjectName("AboutFidi")
        AboutFidi.resize(387, 470)
        self.OkButton = QtWidgets.QDialogButtonBox(AboutFidi)
        self.OkButton.setGeometry(QtCore.QRect(150, 320, 71, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.OkButton.setFont(font)
        self.OkButton.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.OkButton.setObjectName("OkButton")
        self.label = QtWidgets.QLabel(AboutFidi)
        self.label.setGeometry(QtCore.QRect(148, 20, 71, 51))
        font = QtGui.QFont()
        font.setFamily("Constantia")
        font.setPointSize(26)
        font.setWeight(50)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AboutFidi)
        self.label_2.setGeometry(QtCore.QRect(150, 70, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(AboutFidi)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 110, 321, 211))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_3 = QtWidgets.QLabel(AboutFidi)
        self.label_3.setGeometry(QtCore.QRect(110, 90, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(AboutFidi)
        QtCore.QObject.connect(self.OkButton, QtCore.SIGNAL("clicked(QAbstractButton*)"), AboutFidi.close)
        QtCore.QMetaObject.connectSlotsByName(AboutFidi)

    def retranslateUi(self, AboutFidi):
        AboutFidi.setWindowTitle(QtWidgets.QApplication.translate("AboutFidi", "Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("AboutFidi", "FIDI", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("AboutFidi", "Version 0.1", None, -1))
        self.plainTextEdit.setPlainText(QtWidgets.QApplication.translate("AboutFidi", "some text about FIDI, for what it would be used and about master thesis", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("AboutFidi", "Author : Mateusz Borecki", None, -1))

