# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_fidi.ui',
# licensing of 'about_fidi.ui' applies.
#
# Created: Sat Nov  2 16:19:09 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AboutFidi(object):
    def setupUi(self, AboutFidi):
        AboutFidi.setObjectName("AboutFidi")
        AboutFidi.resize(404, 456)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutFidi.sizePolicy().hasHeightForWidth())
        AboutFidi.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(AboutFidi)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Constantia")
        font.setPointSize(26)
        font.setWeight(50)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.OkButton = QtWidgets.QDialogButtonBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.OkButton.setFont(font)
        self.OkButton.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.OkButton.setObjectName("OkButton")
        self.verticalLayout.addWidget(self.OkButton)
        AboutFidi.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AboutFidi)
        self.statusbar.setObjectName("statusbar")
        AboutFidi.setStatusBar(self.statusbar)

        self.retranslateUi(AboutFidi)
        QtCore.QObject.connect(self.OkButton, QtCore.SIGNAL("clicked(QAbstractButton*)"), AboutFidi.close)
        QtCore.QMetaObject.connectSlotsByName(AboutFidi)

    def retranslateUi(self, AboutFidi):
        AboutFidi.setWindowTitle(QtWidgets.QApplication.translate("AboutFidi", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("AboutFidi", "FIDI", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("AboutFidi", "Version 0.2", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("AboutFidi", "Author : Mateusz Borecki", None, -1))
        self.plainTextEdit.setPlainText(QtWidgets.QApplication.translate("AboutFidi", "FIDI is open source program released under GNU GPL v3.0 license.\n"
"\n"
"Program is able to analyze plate, shield and flat shell structures using Finite Differences Method. Project has been written as master’s thesis by Eng. Mateusz Borecki under the supervision of PhD Eng. Roman Putanowicz at the Cracow University of Technology.\n"
"", None, -1))

