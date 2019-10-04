"""This part of program is responsible for collecting properties of prism
attributes from user and saving it in json format"""

import json
from collecting_attributes import console_input_attributes as C  # for now only console input, I will add GUI later


def fidi_save_file(filename, t, w, h, e, v, n, sh, p, d, s):
    """Function for saving properties of elements in json format"""

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
                           'geometry': {'thickness': t, 'width': w, 'height': h},
                           'material': {'E': e, 'v': v},
                           'name': n,
                           'loads_shield': sh,
                           'loads_plate': p,
                           'density': d,
                           'supports': s}

        with open('../fidi_attributes/json_files/{}.json'.format(filename), 'w') as starting_file:
            starting_file.write(json.dumps(fidi_attributes, indent=4, sort_keys=True))


if __name__ == '__main__':
    fidi_save_file(C.name,
                   C.thickness,
                   C.width,
                   C.height,
                   C.E,
                   C.v,
                   C.name,
                   C.loads_shield,
                   C.loads_plate,
                   C.density,
                   C.supports)
