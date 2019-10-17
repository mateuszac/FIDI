"""This part of program is responsible for loading properties of prism
attributes from existing json file"""

import json


def fidi_load_file(filename):
    """Function for loading saved properties of elements"""

    try:

        with open('../fidi_attributes/json_files/{}.json'.format(filename)) as starting_file:
            return json.load(starting_file)

    except FileNotFoundError:

        print("There is no {}.json in json_files folder".format(filename))


def create_element():  # Later I will add possibility of using argument of filename instead of input
    """This function creates new Prism object"""
    _data = fidi_load_file(input('Please enter the name of file to load'))
    if _data['object_type'] == "plate":
        return Plate(_data)
    elif _data['object_type'] == "shield":
        return Shield(_data)
    else:
        return Shell(_data)


class Prism(object):
    """Prism object contain all the information gathered from user about properties of element, density of mesh
    and location of supports. Methods of this class are inherited to Shell, Shield and Plate classes
    """

    def __init__(self, json_data):
        """ Loading all properties from existing json file """

        self._geometry = json_data['geometry']
        self._material = json_data['material']
        self._name = json_data['name']
        self._density = json_data['density']
        self._supports = json_data['supports']
        self._object_type = json_data['object_type']

    @property
    def geometry(self):
        return self._geometry

    @property
    def material(self):
        return self._material

    @property
    def name(self):
        return self._name

    @property
    def density(self):
        return self._density

    @property
    def supports(self):
        return self._supports

    @property
    def object_type(self):
        return self._object_type


class Shield(Prism):
    """In case loads act in the prism plane"""

    def __init__(self, json_data):
        """ Loading all methods of any Prism object and shield loads"""
        super().__init__(json_data)
        self._loads_shield = json_data['loads_shield']

    @property
    def loads_shield(self):
        return self._loads_shield


class Plate(Prism):
    """In case loads act perpendicular to the prism plane"""

    def __init__(self, json_data):
        """ Loading all methods of any Prism object and plate loads"""
        super().__init__(json_data)
        self._loads_plate = json_data['loads_plate']

    @property
    def loads_plate(self):
        return self._loads_plate


class Shell(Shield, Plate):
    """In case loads act both perpendicular and in the prism plane"""

    def __init__(self, json_data):
        """ Loading all methods and attributes of any Shield or Plate object"""
        super().__init__(json_data)


if __name__ == '__main__':

    test_plate1 = create_element()
    test_plate2 = create_element()
    print(test_plate1.geometry)
    print(test_plate1.loads_plate)
    print(test_plate2.object_type)
