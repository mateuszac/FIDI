"""This part of program is responsible for collecting properties of prism
attributes from user and saving it in json format"""

import json
from src.fidi_attributes.collecting_attributes import console_input_attributes as console


def fidi_save_file(props):
    """Function for saving properties of elements in json format"""

    filename = props[0]

    try:

        with open('../prism_attributes/json_files/{}.json'.format(filename)):
            answer = str(input("File named {}.json has already been created,"
                               " do you want to override this file [y/n]?".format(filename)))
            if answer == "n":
                filename = filename + ".(2)"
                raise FileNotFoundError
            elif answer == "y":
                raise FileNotFoundError
            else:
                print("please enter the letter y for yes or n for no")

    except FileNotFoundError:

        fidi_attributes = {
                           'name': props[0],
                           'geometry': {'thickness': props[1], 'width': props[2], 'height': props[3]},
                           'material': {'E': props[4], 'v': props[5]},
                           'object_type': props[6],
                           'loads_shield': props[7],
                           'loads_plate': props[8],
                           'density': props[9],
                           'supports': props[10]}

        with open('../fidi_attributes/json_files/{}.json'.format(filename), 'w') as starting_file:
            starting_file.write(json.dumps(fidi_attributes, indent=4, sort_keys=True))


if __name__ == '__main__':

    properties = console.console_collecting_attributes()
    fidi_save_file(properties)
