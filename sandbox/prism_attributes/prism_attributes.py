"""This is the first attempt to make file that contains information about
 material, geometry, loads, type of element and density of FDM mesh """


class Prism:
    """Considered elements are solids with constant thickness"""

    geometry = {
                "thickness": float(0.12),  # [m]
                "width": float(3),         # [m]
                "height": float(5),        # [m]
    }

    material = {
                "E": float(210000000000),  # [Pa]
                "v": float(0.3),           # [-]
    }

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
shield_123 = Shield("shield_123")
print(shield_123.geometry)