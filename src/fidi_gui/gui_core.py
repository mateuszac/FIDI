from PySide2 import QtWidgets

from Ui import starting_window, about_fidi


class StartingWindow(starting_window.Ui_StartingWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(StartingWindow, self).__init__()
        self.setupUi(self)
        self.InfoButton.clicked.connect(self.open_info)

    def open_info(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = about_fidi.Ui_AboutFidi()
        self.ui.setupUi(self.window)
        self.window.show()
        about_fidi.Ui_AboutFidi.OkButton.clicked.connect(self.close())


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = StartingWindow()
    qt_app.show()
    app.exec_()

