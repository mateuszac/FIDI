from PySide2 import QtWidgets

from Ui import starting_window, about_fidi, plate_window, shield_window, shell_window


class StartingWindow(starting_window.Ui_StartingWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(StartingWindow, self).__init__()
        self.setupUi(self)
        self.InfoButton.clicked.connect(self.open_info)
        self.PlateButton.clicked.connect(self.open_plate)
        self.ShieldButton.clicked.connect(self.open_shield)
        self.ShellButton.clicked.connect(self.open_shell)

    def open_info(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = about_fidi.Ui_AboutFidi()
        self.ui.setupUi(self.window)
        self.window.show()

    def open_plate(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = plate_window.Ui_MainPlateWindow()
        self.ui.setupUi(self.window)
        StartingWindow.hide(self)
        self.window.show()

    def open_shield(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = shield_window.Ui_MainShieldWindow()
        self.ui.setupUi(self.window)
        StartingWindow.hide(self)
        self.window.show()

    def open_shell(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = shell_window.Ui_MainShellWindow()
        self.ui.setupUi(self.window)
        StartingWindow.hide(self)
        self.window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = StartingWindow()
    qt_app.show()
    app.exec_()

