"""This part of program is responsible for loading properties of prism
attributes from existing json file"""

import json
from fidi.fdm_engine import fdm_plate_algorithm as fdm_plate  # importing functions responsible for plate algorithm
from fidi.fdm_engine import fdm_shield_algorithm as fdm_shield  # importing functions responsible for shield algorithm
from fidi.fdm_engine import mesh as stat          # importing classes containing statical quantities


def fidi_load_file(filename):
    """Function for loading saved properties of elements"""

    try:

        with open('../attributes/json_files/{}.json'.format(filename)) as starting_file:
            return json.load(starting_file)

    except FileNotFoundError:

        print("There is no {}.json in json_files folder".format(filename))


def create_element():
    """This function creates new Prism object"""
    _data = fidi_load_file(input('Please enter the name of file to load'))
    if _data is None:
        return None
    else:
        if _data['object_type'] == "plate":
            return Plate(_data)
        elif _data['object_type'] == "shield":
            return Shield(_data)
        else:
            return Shell(_data)


def statical_quantities(width, height, density, element_type, supports):
    """Creating objects from statical quantities classes"""
    mesh = stat.Mesh(width, height, density)
    displacements = stat.Displacements(mesh, element_type, supports)
    rotations = stat.Rotations(mesh, element_type, supports)
    membrane_forces = stat.MembraneForces(mesh)
    membrane_moment = stat.MembraneMoment(mesh)
    return [mesh, displacements, rotations, membrane_forces, membrane_moment]


class Prism(object):
    """Prism object contain all the information gathered from user about properties of element, density of mesh
    and location of supports. Methods of this class are inherited to Shell, Shield and Plate classes
    """

    def __init__(self, json_data, computed=False):
        """ Loading all properties from existing json file """

        self._geometry = json_data['geometry']
        self._geometry["thickness"] *= 0.01  # thickness in now in [m]
        self._material = json_data['material']
        self._material["E"] *= 10**9  # modulus of elasticity is now in [N/m2]
        self._name = json_data['name']
        self._density = json_data['density']
        self._supports = json_data['supports']
        self._object_type = json_data['object_type']
        self._computed = computed

        """setting initial statical quantities"""
        statics = statical_quantities(self._geometry['width'], self._geometry['height'], self._density,
                                      self._object_type, self._supports)
        self._nodes = statics[0].nodes
        self._displacements = statics[1].data
        self._rotations = statics[2].data
        self._membrane_forces = statics[3].data
        self._membrane_moment = statics[4].data

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

    @property
    def nodes(self):
        return self._nodes

    @property
    def displacements(self):
        return self._displacements

    @property
    def rotations(self):
        return self._rotations

    @property
    def membrane_forces(self):
        return self._membrane_forces

    @property
    def membrane_moment(self):
        return self._membrane_moment


class Shield(Prism):
    """In case loads act in the prism plane"""

    def __init__(self, json_data):
        """ Loading all methods of any Prism object and shield loads"""
        super().__init__(json_data)
        self._loads_shield = json_data['loads_shield']
        for direction in self._loads_shield:
            for load in direction:
                load *= 1000  # loads are now in N/m
        # Stiffness of shield
        self._Ds = (self._material["E"] * self._geometry["height"]) / (1 - self._material["v"] ** 2)

    @property
    def loads_shield(self):
        return self._loads_shield

    def compute(self):
        self._computed = True
        fdm_shield.compute_shield(self._displacements, self._material["E"], self._loads_shield,
                           self._supports, self._density, self._material["v"])


class Plate(Prism):
    """In case loads act perpendicular to the prism plane"""

    def __init__(self, json_data):
        """ Loading all methods of any Prism object and plate loads"""
        super().__init__(json_data)
        self._loads_plate = json_data['loads_plate']
        self._loads_plate *= 1000  # load is now in N/m2
        # Flexural stiffness of plate
        self._Dp = (self._material["E"]*self._geometry["height"]**3)/(12*(1-self._material["v"]**2))

    @property
    def loads_plate(self):
        return self._loads_plate

    def compute(self):
        self._computed = True
        self._displacements[2] = fdm_plate.compute_plate(self._displacements, self._Dp, self._loads_plate,
                                                   self._supports, self._density, self._material["v"])


class Shell(Shield, Plate):
    """In case loads act both perpendicular and in the prism plane"""

    def __init__(self, json_data):
        """ Loading all methods and attributes of any Shield or Plate object"""
        super().__init__(json_data)

    def compute(self):
        self._computed = True
        fdm_plate.compute_plate(self._displacements, self._Dp, self._loads_plate,
                          self._supports, self._density, self._material["v"])
        fdm_shield.compute_shield(self._displacements, self._material["E"], self._loads_shield,
                           self._supports, self._density, self._material["v"])


if __name__ == '__main__':

    test_plate1 = create_element()
    test_plate2 = create_element()
    print(test_plate1.geometry)
    print(test_plate1.loads_plate)
    print(test_plate2.object_type)
