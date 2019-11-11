"""This part of program is responsible for joining all parts of GUI and adds functionality to all windows, that is not
assigned in QTdesigner - opening other windows and importing given data"""

from PySide2 import QtWidgets

from src.fidi_gui.Ui import starting_window, about_fidi, plate_window, shield_window, shell_window
from src.fidi_attributes.collecting_attributes import gui_input_attributes as attributes


class FidiInterface(starting_window.Ui_StartingWindow, QtWidgets.QMainWindow):
    """Class opening starting window of GUI and importing all methods of classes created by QTdesigner"""
    def __init__(self):
        """Opens starting window, imports all widgets from QTdesigner file and gives functionality to buttons
        in starting window"""
        super(FidiInterface, self).__init__()
        self.setupUi(self)
        self.ui = None
        self.data = None
        self.data_error = 1
        # Added functions :
        self.setWindowTitle("FIDI")
        self.InfoButton.clicked.connect(self.open_info)
        self.PlateButton.clicked.connect(self.new_plate)
        self.ShieldButton.clicked.connect(self.new_shield)
        self.ShellButton.clicked.connect(self.new_shell)

    def new_element(self):
        """Opens next window, that allows to create or load another element
        """
        self.new_app = QtWidgets.QMainWindow()
        self.next_app = FidiInterface()
        self.next_app.show()

    def open_info(self):
        """Opens info window, imports all widgets from QTdesigner file and gives functionality to widgets
        """
        self.about_fidi_window = QtWidgets.QMainWindow()
        self.ui = about_fidi.Ui_AboutFidi()
        self.ui.setupUi(self.about_fidi_window)
        self.about_fidi_window.setWindowTitle("About FIDI")
        self.about_fidi_window.show()

    def combobox(self):
        """Adds data to existing comboboxes"""
        self.ui.BottomSupportInput.addItem("Free")
        self.ui.BottomSupportInput.addItem("Hinged")
        self.ui.BottomSupportInput.addItem("Fixed")
        self.ui.TopSupportInput.addItem("Free")
        self.ui.TopSupportInput.addItem("Hinged")
        self.ui.TopSupportInput.addItem("Fixed")
        self.ui.LeftSupportInput.addItem("Free")
        self.ui.LeftSupportInput.addItem("Hinged")
        self.ui.LeftSupportInput.addItem("Fixed")
        self.ui.RightSupportInput.addItem("Free")
        self.ui.RightSupportInput.addItem("Hinged")
        self.ui.RightSupportInput.addItem("Fixed")

    def new_plate(self):
        """Opens plate window, imports all widgets from QTdesigner file and gives functionality to widgets
        """
        self.plate_window = QtWidgets.QMainWindow()
        self.ui = plate_window.Ui_MainPlateWindow()
        self.ui.setupUi(self.plate_window)
        FidiInterface.hide(self)
        self.plate_window.setWindowTitle("FIDI - Plate")
        self.plate_window.show()
        # Added functions :

    def new_shield(self):
        """Opens shield window, imports all widgets from QTdesigner file and gives functionality to widgets
        """
        self.shield_window = QtWidgets.QMainWindow()
        self.ui = shield_window.Ui_MainShieldWindow()
        self.ui.setupUi(self.shield_window)
        self.combobox()
        FidiInterface.hide(self)
        self.shield_window.setWindowTitle("FIDI - Shield")
        self.shield_window.show()
        # Added functions :
        self.ui.actionNew.triggered.connect(self.new_element)
        self.ui.actionAbout_FIDI.triggered.connect(self.open_info)
        self.ui.LoadButton.released.connect(self.check_shield_data)

    def new_shell(self):
        """Opens shell window, imports all widgets from QTdesigner file and gives functionality to widgets
        """
        self.shell_window = QtWidgets.QMainWindow()
        self.ui = shell_window.Ui_MainShellWindow()
        self.ui.setupUi(self.shell_window)
        FidiInterface.hide(self)
        self.shell_window.setWindowTitle("FIDI - Shell")
        self.shell_window.show()
        # Added functions :

    def warning(self, text):
        """Opens message box, that informs user input is inappropriate"""
        warning_window = QtWidgets.QMessageBox()
        warning_window.setText(text)
        warning_window.exec()

    def gui_input(self, inp):
        """Prevents from entering inappropriate input"""
        if inp == "error":
            self.warning("Please enter appropriate input")
        else:
            pass
        return inp

    def check_shield_data(self):
        """Checking if every attribute is proper and ready to save, then saving them in variables"""
        type_of_element = 1
        name = self.gui_input(attributes.gui_name(self.ui.NameInput.text()))
        thickness = self.gui_input(attributes.gui_positive_num_input(self.ui.ThicknessInput.value()))
        width_input = self.gui_input(attributes.gui_positive_num_input(self.ui.WidthInput.value()))
        height_input = self.gui_input(attributes.gui_positive_num_input(self.ui.HeightInput.value()))
        density = self.gui_input(attributes.gui_positive_num_input(self.ui.DensityInput.value()))
        E = self.gui_input(attributes.gui_positive_num_input(self.ui.EInput.value()))
        v = self.gui_input(attributes.gui_positive_num_input(self.ui.vInput.value()))

        x_left = self.gui_input(attributes.gui_num_input(self.ui.XLInput.value()))
        x_right = self.gui_input(attributes.gui_num_input(self.ui.XRInput.value()))
        x_bottom = self.gui_input(attributes.gui_num_input(self.ui.XBInput.value()))
        x_top = self.gui_input(attributes.gui_num_input(self.ui.XTInput.value()))
        y_left = self.gui_input(attributes.gui_num_input(self.ui.YLInput.value()))
        y_right = self.gui_input(attributes.gui_num_input(self.ui.YRInput.value()))
        y_bottom = self.gui_input(attributes.gui_num_input(self.ui.YBInput.value()))
        y_top = self.gui_input(attributes.gui_num_input(self.ui.YTInput.value()))

        support_left = self.gui_input(attributes.gui_support_input(self.ui.LeftSupportInput.currentText()))
        support_right = self.gui_input(attributes.gui_support_input(self.ui.RightSupportInput.currentText()))
        support_top = self.gui_input(attributes.gui_support_input(self.ui.TopSupportInput.currentText()))
        support_bottom = self.gui_input(attributes.gui_support_input(self.ui.BottomSupportInput.currentText()))

        loads_plate = None
        loads_shield = attributes.shield_loads_dict(x_left, x_bottom, x_right, x_top, y_left, y_bottom, y_right, y_top)

        errorness = 0

        for i in [type_of_element, name, thickness, width_input, height_input,
                  density, E, v, loads_plate, loads_shield, support_left,
                  support_right, support_top, support_bottom]:
            if i == "error":
                errorness += 1
            else:
                continue
            if errorness == 0:
                self.data_error = 0

        self.data = attributes.gui_collecting_attributes(type_of_element, name, thickness, width_input, height_input,
                                                         density, E, v, loads_plate, loads_shield, support_left,
                                                         support_right, support_top, support_bottom)
        for i in range(len(self.data)): # DELETE THIS LINES
            print(self.data[i])         # THERE ARE ONLY FOR TESTING


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = FidiInterface()
    qt_app.show()
    app.exec_()
