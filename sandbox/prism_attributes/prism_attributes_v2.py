"""This is the attempt to use json format in order to load properties of elements"""

import json

with open('../json_files/data_underlay.json') as starting_file:
    data = json.load(starting_file)

geometry_data = data['geometry']
material_data = data['material']
name_data = data['name']
loads_shield_data = data['loads_shield']
loads_plate_data = data['loads_plate']
density_data = data['density']


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
