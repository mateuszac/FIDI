"""This part of program is responsible for joining all parts of GUI and adds functionality to all windows, that is not
assigned in QTdesigner - opening other windows and importing given data"""

from PySide2 import QtWidgets

from fidi.gui.Ui import starting_window, about_fidi, plate_window, shield_window, shell_window
from fidi.attributes.collecting_attributes import gui_input_attributes as att
from fidi.attributes.saving_attributes import gui_save_file
from fidi.attributes import loading_attributes as obj
import json
import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors


class FidiInterface(starting_window.Ui_StartingWindow, QtWidgets.QMainWindow):
    """Class opening starting window of GUI and importing all methods of classes created by QTdesigner"""
    def __init__(self):
        """Opens starting window, imports all widgets from QTdesigner file and gives functionality to buttons
        in starting window"""
        super(FidiInterface, self).__init__()
        self.setupUi(self)
        self.ui = None
        self.data = None
        self.prism = None
        self.data_error = 0
        self.stability_error = 0
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
        self.combobox()
        FidiInterface.hide(self)
        self.plate_window.setWindowTitle("FIDI - Plate")
        self.plate_window.show()
        self.ui.type = 2
        # Added functions :
        self.ui.actionNew.triggered.connect(self.new_element)
        self.ui.actionAbout_FIDI.triggered.connect(self.open_info)
        self.ui.LoadButton.released.connect(self.load)
        self.ui.SaveButton.released.connect(self.save)
        self.ui.CalculateButton.released.connect(self.calculate)
        # Results of calculations :
        self.ui.w_button.released.connect(self.w_results)
        self.ui.sigma_x_button.released.connect(self.sigma_x_results)
        self.ui.sigma_y_button.released.connect(self.sigma_y_results)
        self.ui.tau_xy_button.released.connect(self.tau_xy_results)
        self.ui.Mxx_button.released.connect(self.mxx_results)
        self.ui.Myy_button.released.connect(self.myy_results)
        self.ui.Mxy_button.released.connect(self.mxy_results)

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
        self.ui.type = 1
        # Added functions :
        self.ui.actionNew.triggered.connect(self.new_element)
        self.ui.actionAbout_FIDI.triggered.connect(self.open_info)
        self.ui.LoadButton.released.connect(self.load)
        self.ui.SaveButton.released.connect(self.save)
        self.ui.CalculateButton.released.connect(self.calculate)
        # Results of calculations :
        self.ui.u_button.released.connect(self.u_results)
        self.ui.v_button.released.connect(self.v_results)
        self.ui.sigma_x_button.released.connect(self.sigma_x_results)
        self.ui.sigma_y_button.released.connect(self.sigma_y_results)
        self.ui.tau_xy_button.released.connect(self.tau_xy_results)
        self.ui.Nxx_button.released.connect(self.nxx_results)
        self.ui.Nyy_button.released.connect(self.nyy_results)
        self.ui.Nxy_button.released.connect(self.nxy_results)

    def new_shell(self):
        """Opens shell window, imports all widgets from QTdesigner file and gives functionality to widgets
        """
        self.shell_window = QtWidgets.QMainWindow()
        self.ui = shell_window.Ui_MainShellWindow()
        self.ui.setupUi(self.shell_window)
        self.combobox()
        FidiInterface.hide(self)
        self.shell_window.setWindowTitle("FIDI - Shell")
        self.shell_window.show()
        self.ui.type = 3
        # Added functions :
        self.ui.actionNew.triggered.connect(self.new_element)
        self.ui.actionAbout_FIDI.triggered.connect(self.open_info)
        self.ui.LoadButton.released.connect(self.load)
        self.ui.SaveButton.released.connect(self.save)
        self.ui.CalculateButton.released.connect(self.calculate)
        # Results of calculations :
        self.ui.u_button.released.connect(self.u_results)
        self.ui.v_button.released.connect(self.v_results)
        self.ui.w_button.released.connect(self.w_results)
        self.ui.sigma_x_button.released.connect(self.sigma_x_results)
        self.ui.sigma_y_button.released.connect(self.sigma_y_results)
        self.ui.tau_xy_button.released.connect(self.tau_xy_results)
        self.ui.Nxx_button.released.connect(self.nxx_results)
        self.ui.Nyy_button.released.connect(self.nyy_results)
        self.ui.Nxy_button.released.connect(self.nxy_results)
        self.ui.Mxx_button.released.connect(self.mxx_results)
        self.ui.Myy_button.released.connect(self.myy_results)
        self.ui.Mxy_button.released.connect(self.mxy_results)

    def gather_data(self):
            """Gathers data from user and saves it into a list with dict containing
             data and information if mesh is proper
             """
            type_of_element = self.ui.type
            loads_plate = None
            loads_shield = None
            if type_of_element == 1 or type_of_element == 3:  # shields or shells
                if type_of_element == 1:
                    loads_plate = None

                x_left = self.ui.XLInput.value()
                x_right = self.ui.XRInput.value()
                x_bottom = self.ui.XBInput.value()
                x_top = self.ui.XTInput.value()
                y_left = self.ui.YLInput.value()
                y_right = self.ui.YRInput.value()
                y_bottom = self.ui.YBInput.value()
                y_top = self.ui.YTInput.value()

                loads_shield = att.shield_loads_dict(x_left, x_bottom, x_right, x_top, y_left, y_bottom, y_right, y_top)
            if type_of_element == 2 or type_of_element == 3:  # plates or shells
                if type_of_element == 2:
                    loads_shield = None

                loads_plate = self.ui.QInput.value()

            return att.gui_collecting_attributes(type_of_element, self.ui.NameInput.text(),
                                                 self.ui.ThicknessInput.value(), self.ui.WidthInput.value(),
                                                 self.ui.HeightInput.value(), self.ui.DensityInput.value(),
                                                 self.ui.EInput.value(), self.ui.vInput.value(),
                                                 loads_plate, loads_shield, self.ui.LeftSupportInput.currentText(),
                                                 self.ui.RightSupportInput.currentText(),
                                                 self.ui.TopSupportInput.currentText(),
                                                 self.ui.BottomSupportInput.currentText())

    def save(self):
        """Saves attributes into json file in temporary folder json_files"""
        input_data = self.gather_data()

        if input_data[1] is True:
            self.warning("Error, the mesh is too rare, please choose another density")
        else:
            filename = self.ui.NameInput.text()
            try:
                with open('../attributes/json_files/{}.json'.format(filename)):
                    self.warning("File with that name already exists, please choose another")
            except FileNotFoundError:
                if filename != "":
                    gui_save_file(input_data[0], filename)
                    self.warning("File has been saved")
                else:
                    self.warning("You cannot save file with no name")

    def load(self):
        """Loads attributes from json file into input boxes"""

        file_name, file_ext = QtWidgets.QFileDialog.getOpenFileName(self, "Select json file")
        data = None
        type_of_element = self.ui.type

        try:

            with open(file_name) as file:
                data = json.load(file)

        except json.JSONDecodeError:

            self.warning("Error, please choose proper .json file")

        if data is not None:
            try:
                self.ui.NameInput.setProperty("text", (data["name"]))
                self.ui.DensityInput.setProperty("value", data["density"])
                self.ui.ThicknessInput.setProperty("value", data["geometry"]["thickness"])
                self.ui.WidthInput.setProperty("value", data["geometry"]["width"])
                self.ui.HeightInput.setProperty("value", data["geometry"]["height"])
                self.ui.EInput.setProperty("value", data["material"]["E"])
                self.ui.vInput.setProperty("value", data["material"]["v"])
                # forces:
                if type_of_element == 1 or type_of_element == 3:  # shields or shells
                    self.ui.XLInput.setProperty("value", data["loads_shield"]["x_direction"]["left"])
                    self.ui.XRInput.setProperty("value", data["loads_shield"]["x_direction"]["right"])
                    self.ui.XBInput.setProperty("value", data["loads_shield"]["x_direction"]["bottom"])
                    self.ui.XTInput.setProperty("value", data["loads_shield"]["x_direction"]["top"])
                    self.ui.YLInput.setProperty("value", data["loads_shield"]["y_direction"]["left"])
                    self.ui.YRInput.setProperty("value", data["loads_shield"]["y_direction"]["right"])
                    self.ui.YBInput.setProperty("value", data["loads_shield"]["y_direction"]["bottom"])
                    self.ui.YTInput.setProperty("value", data["loads_shield"]["y_direction"]["top"])
                if type_of_element == 2 or type_of_element == 3:  # plates or shells
                    self.ui.QInput.setProperty("value", data["loads_plate"])
                # supports:
                self.ui.LeftSupportInput.setProperty("currentText", data["supports"]["left"])
                self.ui.RightSupportInput.setProperty("currentText", data["supports"]["right"])
                self.ui.TopSupportInput.setProperty("currentText", data["supports"]["top"])
                self.ui.BottomSupportInput.setProperty("currentText", data["supports"]["bottom"])
                self.check_shield_data()  # check if every value is correct
            except KeyError:
                self.warning("Sorry, file is damaged")
            except TypeError:
                self.warning("Your element is another type (Shield/Plate/Shell)")
            except FileNotFoundError:
                pass
        else:
            pass

    def calculate(self):
        """Creates prism object and uses compute method, different for each type of element"""

        if self.data_error > 0:
            self.check_shield_data()
            if self.data_error > 0:
                self.warning("Data error, please check if every attribute is proper")
                return
            else:
                pass
        else:
            pass

        self.stability_check()
        if self.stability_error > 0:
            self.warning("Structure is unstable")
            return
        else:
            pass

        input_data = self.gather_data()
        type_of_element = self.ui.type

        if input_data[1] is True:
            self.warning("Error, the mesh is too rare, please choose another density")
        else:
            data = {
                   'name': input_data[0][0],
                   'geometry': {'thickness': input_data[0][1], 'width': input_data[0][2], 'height': input_data[0][3]},
                   'material': {'E': input_data[0][4], 'v': input_data[0][5]},
                   'object_type': input_data[0][6],
                   'loads_shield': input_data[0][7],
                   'loads_plate': input_data[0][8],
                   'density': input_data[0][9],
                   'supports': input_data[0][10]}
            if type_of_element == 1:
                self.prism = obj.Shield(data)
            elif type_of_element == 2:
                self.prism = obj.Plate(data)
            else:
                self.prism = obj.Shell(data)

            self.numeric_supports(self.prism.supports)
            start = datetime.datetime.now()
            self.prism.compute()
            duration = datetime.datetime.now() - start  # time of calculations
            self.warning("Calculations completed, time of solving - {}".format(duration))

    def warning(self, text):
        """Opens message box, that informs user input is inappropriate"""
        warning_window = QtWidgets.QMessageBox()
        warning_window.setText(text)
        warning_window.exec()

    def numeric_supports(self, some_supports):
        """converts strings in supports to numbers"""
        for direction in some_supports:
            if some_supports[direction] == "Free":
                some_supports[direction] = 0
            elif some_supports[direction] == "Hinged":
                some_supports[direction] = 1
            else:
                some_supports[direction] = 2

    def gui_input(self, inp):
        """Prevents from entering inappropriate input"""
        if inp == "error":
            self.warning("Please enter appropriate input")
        else:
            pass
        return inp

    def stability_check(self):
        """Checking if structure is stable, BDOF - blocked degrees of freedom """
        BDOF = 0
        for support in [self.ui.LeftSupportInput.currentText(), self.ui.RightSupportInput.currentText(),
                        self.ui.BottomSupportInput.currentText(), self.ui.TopSupportInput.currentText()]:
            if support == "Hinged":
                BDOF += 1
            elif support == "Fixed":
                BDOF += 2
            else:
                continue

        if BDOF <= 1:
            self.stability_error = 1
        else:
            self.stability_error = 0

    def check_shield_data(self):
        """Checking if every attribute is proper and ready to save, then saving them in variables"""
        type_of_element = 1
        name = self.gui_input(att.gui_name(self.ui.NameInput.text()))
        thickness = self.gui_input(att.gui_positive_num_input(self.ui.ThicknessInput.value()))
        width_input = self.gui_input(att.gui_positive_num_input(self.ui.WidthInput.value()))
        height_input = self.gui_input(att.gui_positive_num_input(self.ui.HeightInput.value()))
        density = self.gui_input(att.gui_positive_num_input(self.ui.DensityInput.value()))
        E = self.gui_input(att.gui_positive_num_input(self.ui.EInput.value()))
        v = self.gui_input(att.gui_positive_num_input(self.ui.vInput.value()))

        x_left = self.gui_input(att.gui_num_input(self.ui.XLInput.value()))
        x_right = self.gui_input(att.gui_num_input(self.ui.XRInput.value()))
        x_bottom = self.gui_input(att.gui_num_input(self.ui.XBInput.value()))
        x_top = self.gui_input(att.gui_num_input(self.ui.XTInput.value()))
        y_left = self.gui_input(att.gui_num_input(self.ui.YLInput.value()))
        y_right = self.gui_input(att.gui_num_input(self.ui.YRInput.value()))
        y_bottom = self.gui_input(att.gui_num_input(self.ui.YBInput.value()))
        y_top = self.gui_input(att.gui_num_input(self.ui.YTInput.value()))

        support_left = self.gui_input(att.gui_support_input(self.ui.LeftSupportInput.currentText()))
        support_right = self.gui_input(att.gui_support_input(self.ui.RightSupportInput.currentText()))
        support_top = self.gui_input(att.gui_support_input(self.ui.TopSupportInput.currentText()))
        support_bottom = self.gui_input(att.gui_support_input(self.ui.BottomSupportInput.currentText()))

        loads_plate = None
        loads_shield = att.shield_loads_dict(x_left, x_bottom, x_right, x_top, y_left, y_bottom, y_right, y_top)

        errorness = 0  # if value of errorness is 0, there is no data error and calculations may be done

        [data, too_rare_mesh] = att.gui_collecting_attributes(type_of_element, name, thickness, width_input,
                                                              height_input,
                                                              density, E, v, loads_plate, loads_shield, support_left,
                                                              support_right, support_top, support_bottom)

        for i in [type_of_element, name, thickness, width_input, height_input,
                  density, E, v, loads_plate, loads_shield, support_left,
                  support_right, support_top, support_bottom]:
            if i == "error":
                errorness += 1
            else:
                continue

        if errorness == 0 and too_rare_mesh is False:
            self.data_error = 0
        elif too_rare_mesh is True:
            self.data_error = 1
            self.warning("Error, the mesh is too rare, please choose another density")
        else:
            self.data_error = 1

        self.data = data

    def map_plot(self, data):
        """Creates window with map of results"""
        (ii, jj) = data.shape
        ii *= self.prism._density
        jj *= self.prism._density
        fig, ax = plt.subplots(1, 2)
        cmap = cm.get_cmap(name='jet', lut=40)
        norm = matplotlib.colors.Normalize()
        mappable = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
        mappable.set_array(data)
        mappable.autoscale()
        matplotlib.pyplot.colorbar(mappable, ax[1])
        ax[0].imshow(data, extent=(0, ii, 0, jj), interpolation='hermite', cmap=cmap)
        mappable.changed()
        plt.show()

    def u_results(self):
        """Displays results of displacements (u) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[0]*100)  # in [cm]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def v_results(self):
        """Displays results of displacements (v) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[1])  # in [cm]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def w_results(self):
        """Displays results of deflections (w) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[2])  # in [cm]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def sigma_x_results(self):
        """Displays results of stresses (sigma_x) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[3]/1000000)   # in [MPa]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def sigma_y_results(self):
        """Displays results of stresses (sigma_y) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[4]/1000000)   # in [MPa]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def tau_xy_results(self):
        """Displays results of stresses (tau_xy) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[5]/1000000)   # in [MPa]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def mxx_results(self):
        """Displays results of moments (mxx) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[6]/1000)   # in [kNm/m]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def myy_results(self):
        """Displays results of moments (myy) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[7]/1000)   # in [kNm/m]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def mxy_results(self):
        """Displays results of moments (mxy) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[8]/1000)   # in [kNm/m]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def nxx_results(self):
        """Displays results of membrane forces (nxx) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[9]/1000)   # in [kN/m]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def nyy_results(self):
        """Displays results of membrane forces (nyy) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[10]/1000)   # in [kN/m]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")

    def nxy_results(self):
        """Displays results of membrane forces (nxy) calculations"""
        try:
            if self.prism.computed is False:
                self.warning("Results are not available, please perform the calculations first")
            else:
                self.map_plot(self.prism.results[11]/1000)   # in [kN/m]
        except AttributeError:
            self.warning("Results are not available, please perform the calculations first")


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = FidiInterface()
    qt_app.show()
    app.exec_()
