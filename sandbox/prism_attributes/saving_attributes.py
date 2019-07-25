"""This part of program is responsible for collecting properties of prism
attributes from user and saving it in json format"""

import json


def fidi_save_file(filename, t, w, h, e, v, n, s, p, d):
    """Function for saving properties of elements in json format"""

    try:

        with open('../prism_attributes/json_files/{}.json'.format(filename)):
            answer = str(input("File named {}.json has already been created,"
                               " do you want to override this file [y/n]?".format(filename)))
            if answer == "n":
                pass
            elif answer == "y":
                raise FileNotFoundError
            else:
                print("please enter the letter y for yes or n for no")

    except FileNotFoundError:

        fidi_attributes = {
                           'geometry': {'thickness': t, 'width': w, 'height': h},
                           'material': {'E': e, 'v': v},
                           'name': n,
                           'loads_shield': s,
                           'loads_plate': p,
                           'density': d}

        with open('../prism_attributes/json_files/{}.json'.format(filename), 'w') as starting_file:
            starting_file.write(json.dumps(fidi_attributes))


# TEST


fidi_save_file('test_file', 10, 5, 3, 200000000000, 0.4, "Shield_foo", 0, 0, 5)
