"""This part of program is responsible for generating appropriate mesh for finite differences method calculations"""
import numpy as np
from src.fidi_attributes import loading_attributes

d = loading_attributes.Mesh.density
width = loading_attributes.Prism.geometry["width"]
height = loading_attributes.Prism.geometry["height"]
Nx = int(width/d + 1)  # number of nodes on horizontal direction
Ny = int(height/d + 1)  # number of nodes on horizontal direction
# note : Nx and Ny, should always be neutral numbers provided by algorithm making dimensions of
#        element fitted to mesh density in src/fidi_attributes/collecting_attributes method

"""Creation of mesh"""

fidi_mesh = np.zeros((Nx, Ny))


class FidiW:
    """Matrix containing displacements of element"""
    pass


class FidiFi:
    """Matrix containing rotations of element"""
    pass


class FidiNxx:
    """Matrix containing Nxx forces of element"""
    pass


class FidiNxy:
    """Matrix containing Nxy forces of element"""
    pass


class FidiNyy:
    """Matrix containing Nyy forces of element"""
    pass


class FidiMxx:
    """Matrix containing Mxx moments of element"""
    pass


class FidiMxy:
    """Matrix containing Mxy moments of element"""
    pass


class FidiMyy:
    """Matrix containing Myy moments of element"""
    pass


if __name__ == '__main__':    # TEST
    print(fidi_mesh)