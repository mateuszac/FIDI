"""This part of program is responsible for taking values of prism attributes from user indirect
from the GUI"""


def gui_num_input(description):
    """function checking if attributes are numbers"""
    attribute = "error"
    try:
        attribute = float(description)
    except ValueError:
        attribute = "error"
    finally:
        return attribute


def gui_positive_num_input(description):
    """function checking if attributes are positive numbers"""
    attribute = "error"
    try:
        attribute = float(description)
        if attribute <= 0:
            raise ValueError
    except ValueError:
        attribute = "error"
    finally:
        return attribute


def gui_support_input(description):
    """function checking if supports are numbers 0, 1 or 2"""
    attribute = "error"
    if description == "Free":
        attribute = 0
    elif description == "Hinged":
        attribute = 1
    elif description == "Fixed":
        attribute = 2
    return attribute


def gui_name(description):
    """function checking if name of element is appropriate"""
    attribute = "error"
    try:
        attribute = str(description)
        if attribute == "":
            raise ValueError
        else:
            pass
    except ValueError:
        attribute = "error"
    finally:
        return attribute


def shield_loads_dict(x_left, x_bottom, x_right, x_top, y_left, y_bottom, y_right, y_top):
    """function organizing shield loads into dictionary"""
    loads_shield = {'x_direction': {'left': x_left,  # for now only uniformly distributed
                                    'right': x_right,  # loads are taken into consideration
                                    'top': x_top,
                                    'bottom': x_bottom},
                    'y_direction': {'left': y_left,
                                    'right': y_right,
                                    'top': y_top,
                                    'bottom': y_bottom}}
    return loads_shield


def gui_collecting_attributes(type_of_element, name, thickness, width_input, height_input, density, E, v,
                              loads_plate, loads_shield, support_left, support_right, support_top, support_bottom):
    """function collecting attributes into established json dictionary via GUI"""

    """Geometry of prism, and density of regular mesh in [m] (dimensions are fitted to mesh)"""

    width = density * round(width_input / density, 0)
    height = density * round(height_input / density, 0)
    Nx = int(width / density + 1)
    Ny = int(height / density + 1)
    if Nx > 4 and Ny > 4:
        pass
    else:
        raise ValueError

    """Information about object type"""

    if type_of_element == 1:
        object_type = "shield"
    elif type_of_element == 2:
        object_type = "plate"
    else:
        object_type = "shell"

    """Boundary conditions - supports: 0 for free end, 1 for hinged connection and 2 for fixed connection"""

    supports = {'left': support_left,
                'right': support_right,
                'top': support_top,
                'bottom': support_bottom}
    pass

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
