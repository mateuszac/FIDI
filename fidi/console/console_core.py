"""This part of program is responsible launching console version of FIDI"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import datetime
from fidi.attributes.saving_attributes import console_save_file
from fidi.attributes.collecting_attributes.console_input_attributes import console_collecting_attributes
from fidi.attributes import loading_attributes


class ConsoleFidi(object):
    """Class opening starting window of console version of FIDI"""
    def __init__(self):
        """Setting initial value for work as True and printing initial message"""
        print("Hello user, welcome in console version of FIDI program")
        self.work = True
        self.element = None

    def run(self):
        """Main loop in which the program is running"""
        while self.work is True:
            self.next_action()
        else:
            quit()

    def next_action(self):
        """Asking user what action to perform next"""
        chosen_option = input("Choose :"
                              " 1 - for collecting and saving new attributes"
                              " 2 - for loading existing attributes"
                              " 3 - for performing calculations"
                              " 4 - for showing results (for now only displacements map for plate"
                              " 0 - for exit FIDI"
                              " ")
        try:
            chosen_option = int(chosen_option)
            if chosen_option not in [0, 1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            chosen_option = None

        if chosen_option == 0:
            self.work = False
        elif chosen_option == 1:
            self.save()
        elif chosen_option == 2:
            self.load()
        elif chosen_option == 3:
            self.compute()
        elif chosen_option == 4:
            self.results()
        else:
            print("please enter the number for one of possible actions")

    def save(self):
        console_save_file(console_collecting_attributes())

    def load(self):
        self.element = loading_attributes.create_element()

    def compute(self):
        if self.element is None:
            print("please firstly load the element")
        else:
            start = datetime.datetime.now()
            self.element.compute()
            duration = datetime.datetime.now() - start
            print(duration)

    def results(self):
        if self.element._computed is True:
            plt.imshow(self.element.displacements[2],
                       extent=(0, self.element.nodes[0] - 1, 0, self.element.nodes[1] - 1),
                       interpolation='hermite', cmap=cm.inferno)
            plt.show()
        else:
            print("please firstly perform the calculations")


if __name__ == '__main__':

    fidi_app = ConsoleFidi()
    fidi_app.run()
