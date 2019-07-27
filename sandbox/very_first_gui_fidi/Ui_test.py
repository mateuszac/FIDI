from PySide2 import QtWidgets

from Ui import yyy


class MyQtApp(yyy.Ui_MainWindow , QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        self.cry_push_button.clicked.connect(self.sad_method)

    def sad_method(self):
        QtWidgets.QMessageBox.about(self,"Oh no, why did you do this",
                                    "You shouldn't click that button, now you have to cry")


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = MyQtApp()
    qt_app.show()
    app.exec_()
