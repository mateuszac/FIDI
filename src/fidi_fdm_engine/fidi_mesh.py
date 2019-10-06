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

fidi_mesh = np.zeros((Ny+2, Nx+2)) # +2 is to add extra row/column on each edge for respecting boundary conditions

"""Next objects are matrices - initial values of displacement, rotation, plane forces and moments
   attribute A of each object is mutable matrix, prepared for FDM algorithm"""


class FidiW:
    """Matrix containing displacements of element"""
    A = fidi_mesh
    if loading_attributes.Prism.supports["top"] == 1 or 2:   # for now there is no possibility of initial displacement
        A[1, 1:Nx+1] = 0                                     # but in future value "0" may be changed
    if loading_attributes.Prism.supports["left"] == 1 or 2:  # to dirichlet boundary condition
        A[1:Ny+1, 1] = 0
    if loading_attributes.Prism.supports["bottom"] == 1 or 2:
        A[Ny, 1:Nx+1] = 0
    if loading_attributes.Prism.supports["right"] == 1 or 2:
        A[1:Ny+1, Nx] = 0


class FidiFi:
    """Matrix containing rotations of element"""
    A = fidi_mesh
    if loading_attributes.Prism.supports["top"] == 2:   # for now there is no possibility of initial rotation
        A[1, 1:Nx + 1] = 0                              # but in future value "0" may be changed
    if loading_attributes.Prism.supports["left"] == 2:  # to dirichlet boundary condition
        A[1:Ny + 1, 1] = 0
    if loading_attributes.Prism.supports["bottom"] == 2:
        A[Ny, 1:Nx + 1] = 0
    if loading_attributes.Prism.supports["right"] == 2:
        A[1:Ny + 1, Nx] = 0


class FidiNxx:
    """Matrix containing Nxx forces of element"""
    A = fidi_mesh
    if loading_attributes.Shield.loads_shield is not None:
        # top edge
        A[1, 1:Nx + 1] += 0
        # left edge
        A[1:Ny + 1, 1] -= loading_attributes.Shield.loads_shield["x_direction"]['left']
        # bottom edge
        A[Ny, 1:Nx + 1] += 0
        # right edge
        A[1:Ny + 1, Nx] += loading_attributes.Shield.loads_shield["x_direction"]['right']
    else:
        pass


class FidiNxy:
    """Matrix containing Nxy forces of element"""
    A = fidi_mesh
    if loading_attributes.Shield.loads_shield is not None:
        # top edge
        A[1, 1:Nx + 1] += loading_attributes.Shield.loads_shield["x_direction"]['top']
        # left edge
        A[1:Ny + 1, 1] -= loading_attributes.Shield.loads_shield["y_direction"]['left']
        # bottom edge
        A[Ny, 1:Nx + 1] -= loading_attributes.Shield.loads_shield["x_direction"]['bottom']
        # right edge
        A[1:Ny + 1, Nx] += loading_attributes.Shield.loads_shield["y_direction"]['right']
    else:
        pass


class FidiNyy:
    """Matrix containing Nyy forces of element"""
    A = fidi_mesh
    if loading_attributes.Shield.loads_shield is not None:
        # top edge
        A[1, 1:Nx + 1] += loading_attributes.Shield.loads_shield["y_direction"]['top']
        # left edge
        A[1:Ny + 1, 1] += 0
        # bottom edge
        A[Ny, 1:Nx + 1] -= loading_attributes.Shield.loads_shield["y_direction"]['bottom']
        # right edge
        A[1:Ny + 1, Nx] += 0
    else:
        pass


class FidiMxx:
    """Matrix containing Mxx moments of element"""
    A = fidi_mesh


class FidiMxy:
    """Matrix containing Mxy moments of element"""
    A = fidi_mesh


class FidiMyy:
    """Matrix containing Myy moments of element"""
    A = fidi_mesh


if __name__ == '__main__':    # TEST
    print(FidiNyy.A)