"""This part of program is responsible for taking values of prism attributes from user indirect
from the console"""

"""name of element"""

name = str(input("enter the name of element"))


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
            continue
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
            continue
    return attribute


type_of_element = type_input('choose the type of the element : enter 1 for shield or 2 for plate')

"""Density of regular mesh in [m]"""

density = num_input('enter the density of mesh in [m] - warning : dimensions of element will be fitted to mesh density')

"""Geometry of prism, dimensions are fitted to mesh"""

thickness = num_input('enter the thickness of element in [m]')

width_input = num_input('enter the width of element in [m]')
width = density*round(width_input/density, 0)

height_input = num_input('enter the height of element in [m]')
height = density*round(height_input/density, 0)

"""material properties. E in GPa, v is dimensionless"""

E = num_input('enter the modulus of elasticity of element in [GPa]')

v = num_input('enter the modulus of poisson of element in [-]')

"""All values of loads are given in kN/m"""

if type_of_element == 1:
    loads_shield = {'x_direction': {'left': 0.0,  # for now only uniformly distributed loads are taken into consideration
                                    'right': 0.0,
                                    'top': 0.0,
                                    'bottom': 0.0},
                    'y_direction': {'left': 0.0,
                                    'right': 0.0,
                                    'top': 0.0,
                                    'bottom': 0.0}}

    loads_shield['x_direction']['left'] = num_input('enter the value of load in horizontal direction'
                                                    ' on left boundary in [kN/m]')
    loads_shield['x_direction']['right'] = num_input('enter the value of load in horizontal direction'
                                                     ' on right boundary in [kN/m]')
    loads_shield['x_direction']['top'] = num_input('enter the value of load in horizontal direction on'
                                                   ' top boundary in [kN/m]')
    loads_shield['x_direction']['bottom'] = num_input('enter the value of load in horizontal direction'
                                                      ' on bottom boundary in [kN/m]')
    loads_shield['y_direction']['left'] = num_input('enter the value of load in vertical direction on'
                                                    ' left boundary in [kN/m]')
    loads_shield['y_direction']['right'] = num_input('enter the value of load in vertical direction on'
                                                     ' right boundary in [kN/m]')
    loads_shield['y_direction']['top'] = num_input('enter the value of load in vertical direction on'
                                                   ' top boundary in [kN/m]')
    loads_shield['y_direction']['bottom'] = num_input('enter the value of load in vertical direction on'
                                                      ' bottom boundary in [kN/m]')

    loads_plate = None

else:
    loads_plate = num_input('enter the value of load in [kN/m]')
    # for now only uniformly distributed loads are taken into consideration

    loads_shield = None

"""Boundary conditions - supports: 0 for free end, 1 for hinged connection and 2 for fixed connection"""

supports = {'left': 0,
            'right': 0,
            'top': 0,
            'bottom': 0}
pass

supports['left'] = support_input('choose the type of the left boundary : enter 0 for free end, 1 for'
                                 'hinged or 2 for fixed connection')
supports['right'] = support_input('choose the type of the right boundary : enter 0 for free end, 1 for'
                                  'hinged or 2 for fixed connection')
supports['top'] = support_input('choose the type of the top boundary : enter 0 for free end, 1 for'
                                'hinged or 2 for fixed connection')
supports['bottom'] = support_input('choose the type of the bottom boundary : enter 0 for free end, 1 for'
                                   'hinged or 2 for fixed connection')
