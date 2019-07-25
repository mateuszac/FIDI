"""This is the attempt to use json format in order to load properties of elements"""

import json


def fidi_load_file(filename):
    """Function for loading saved properties of elements"""

    try:

        with open('../prism_attributes/json_files/{}.json'.format(filename)) as starting_file:
            return json.load(starting_file)

    except FileNotFoundError:

        print("There is no {}.json in json_files folder".format(filename))


"Loading all properties from existing json file"
element_filename = input('Please enter the name of element to load')
data = fidi_load_file(element_filename)  # for now - there is only data_underlay file

try:
    geometry_data = data['geometry']
    material_data = data['material']
    name_data = data['name']
    loads_shield_data = data['loads_shield']
    loads_plate_data = data['loads_plate']
    density_data = data['density']

except [TypeError, NameError]:
    pass


class Prism:
    """Considered elements are solids with constant thickness"""

    geometry = geometry_data

    material = material_data

    def __init__(self, name):
        self.name = name


class Shield(Prism):
    """In case loads act in the prism plane"""
    # loads
    pass


class Plate(Prism):
    """In case loads act perpendicular to the prism plane"""
    # loads
    pass


class Mesh:
    # density
    pass


# TEST

element = Shield(name_data)
print(element.geometry)
