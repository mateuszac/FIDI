"""This part of program is responsible for taking values of prism attributes from user indirect
from the console"""


def num_input(description):
    """function checking if attributes are numbers"""
    attribute = None
    while True:
        try:
            attribute = float(input(description))
        except ValueError:
            print('please enter the number')
        if type(attribute) == float:
            break
        else:
            continue
    return attribute


def positive_num_input(description):
    """function checking if attributes are positive numbers"""
    attribute = None
    while True:
        try:
            attribute = float(input(description))
            if attribute <= 0:
                raise ValueError
        except ValueError:
            print('please enter the positive number')
        if type(attribute) == float and attribute > 0:
            break
        else:
            continue
    return attribute


def support_input(description):
    """function checking if supports are numbers 0, 1 or 2"""
    attribute = None
    while True:
        try:
            attribute = int(input(description))
        except ValueError:
            print('please enter the number 0,1 or 2')
        if attribute == 0:
            break
        elif attribute == 1:
            break
        elif attribute == 2:
            break
        else:
            print('please enter the number 0,1 or 2')
    return attribute


def type_input(description):
    """function checking if user is saving plate or shield"""
    attribute = None
    while True:
        try:
            attribute = int(input(description))
        except ValueError:
            print('please enter the number 1 or 2')
        if attribute == 1:
            break
        elif attribute == 2:
            break
        else:
            print('please enter the number 1 or 2')
    return attribute


def console_collecting_attributes():
    """function collecting attributes into established json dictionary via console"""

    while True:
        name = str(input("enter the name of element "))
        if name == "":
            print('error, you cannot create file with no name')
        else:
            break

    type_of_element = type_input('choose the type of the element : enter 1 for shield, 2 for plate or 3 for shell ')

    """Geometry of prism, and density of regular mesh in [m] (dimensions are fitted to mesh)"""

    thickness = positive_num_input('enter the thickness of element in [m] ')

    width_input = positive_num_input('enter the width of element in [m] ')

    height_input = positive_num_input('enter the height of element in [m] ')

    while True:
        density = positive_num_input('enter the density of mesh in [m] - warning : dimensions of'
                                     ' element will be fitted to mesh density ')

        width = density * round(width_input / density, 0)
        height = density*round(height_input/density, 0)
        Nx = int(width / density + 1)
        Ny = int(height / density + 1)
        if Nx > 4 and Ny > 4:
            break
        else:
            print('error, the mesh is too rare, please choose another density')
            continue

    """material properties. E in GPa, v is dimensionless"""

    E = positive_num_input('enter the modulus of elasticity of element in [GPa] ')

    v = positive_num_input('enter the modulus of poisson of element in [-] ')

    """Information about object type"""

    if type_of_element == 1:
        object_type = "shield"
    elif type_of_element == 2:
        object_type = "plate"
    else:
        object_type = "shell"

    """All values of loads are given in kN/m"""

    loads_plate = None   # initial setting of loads_plate
    loads_shield = None  # initial setting of loads_shield

    if type_of_element == 1 or type_of_element == 3:
        loads_shield = {'x_direction': {'left': 0.0,    # for now only uniformly distributed
                                        'right': 0.0,   # loads are taken into consideration
                                        'top': 0.0,
                                        'bottom': 0.0},
                        'y_direction': {'left': 0.0,
                                        'right': 0.0,
                                        'top': 0.0,
                                        'bottom': 0.0}}

        loads_shield['x_direction']['left'] = num_input('enter the value of load in horizontal direction'
                                                        ' on left boundary in [kN/m] ')
        loads_shield['x_direction']['right'] = num_input('enter the value of load in horizontal direction'
                                                         ' on right boundary in [kN/m] ')
        loads_shield['x_direction']['top'] = num_input('enter the value of load in horizontal direction on'
                                                       ' top boundary in [kN/m] ')
        loads_shield['x_direction']['bottom'] = num_input('enter the value of load in horizontal direction'
                                                          ' on bottom boundary in [kN/m] ')
        loads_shield['y_direction']['left'] = num_input('enter the value of load in vertical direction on'
                                                        ' left boundary in [kN/m] ')
        loads_shield['y_direction']['right'] = num_input('enter the value of load in vertical direction on'
                                                         ' right boundary in [kN/m] ')
        loads_shield['y_direction']['top'] = num_input('enter the value of load in vertical direction on'
                                                       ' top boundary in [kN/m] ')
        loads_shield['y_direction']['bottom'] = num_input('enter the value of load in vertical direction on'
                                                          ' bottom boundary in [kN/m] ')

    elif type_of_element == 2 or type_of_element == 3:
        loads_plate = num_input('enter the value of load in [kN/m] ')
        # for now only uniformly distributed loads are taken into consideration

    """Boundary conditions - supports: 0 for free end, 1 for hinged connection and 2 for fixed connection"""

    supports = {'left': 0,
                'right': 0,
                'top': 0,
                'bottom': 0}
    pass

    supports['left'] = support_input('choose the type of the left boundary : enter 0 for free end, 1 for '
                                     'hinged or 2 for fixed connection ')
    supports['right'] = support_input('choose the type of the right boundary : enter 0 for free end, 1 for '
                                      'hinged or 2 for fixed connection ')
    supports['top'] = support_input('choose the type of the top boundary : enter 0 for free end, 1 for '
                                    'hinged or 2 for fixed connection ')
    supports['bottom'] = support_input('choose the type of the bottom boundary : enter 0 for free end, 1 for '
                                       'hinged or 2 for fixed connection ')

    return [name,
            thickness,
            width,
            height,
            E,
            v,
            object_type,
            loads_shield,
            loads_plate,
            density,
            supports]


if __name__ == '__main__':
    pass
