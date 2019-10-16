"""This part of program is responsible for generating appropriate mesh for finite differences method calculations"""
import numpy as np


class Mesh(object):
    """Creation of empty mesh matrix"""
    def __init__(self, width, height, density):
        Nx = int(width/density + 1)
        Ny = int(height/density + 1)
        self.nodes = (Nx, Ny)

    @property
    def resolution(self):
        return self.nodes


class Displacements(object):
    """ Matrix containing displacements of element """

    def __init__(self, mesh, element_type, supports):
        """ preallocate memory for 3D array """
        self._data = np.zeros((mesh.nodes[0], mesh.nodes[1], 3), dtype=np.float64)
        # boundary conditions from supports
        if element_type == "shell" or "plate":
            if supports["top"] == 1 or supports["top"] == 2:
                self._data[0, :, 2] = 0
            if supports["left"] == 1 or supports["left"] == 2:
                self._data[:, 0, 2] = 0
            if supports["bottom"] == 1 or supports["bottom"] == 2:
                self._data[mesh.nodes[0] - 1, :, 2] = 0
            if supports["right"] == 1 or supports["right"] == 2:
                self._data[:, mesh.nodes[1] - 1, 2] = 0
        if element_type == "shell" or "shield":  # Boundary conditions for wx and wy would be added later
            pass

    @property
    def wx(self):
        return self._data[:, :, 0]

    @property
    def wy(self):
        return self._data[:, :, 1]

    @property
    def wz(self):
        return self._data[:, :, 2]

    @property
    def displacements(self):
        return self._data


class Rotations(object):
    """ Matrix containing rotations of element """

    def __init__(self, mesh, element_type, supports):
        """ preallocate memory for 3D array """
        self.data = np.zeros((mesh.nodes[0], mesh.nodes[1], 3), dtype=np.float64)
        # boundary conditions from supports
        if element_type == "shell" or "plate":
            if supports["top"] == 2:
                self.data[0, :, 2] = 0
            if supports["left"] == 2:
                self.data[:, 0, 2] = 0
            if supports["bottom"] == 2:
                self.data[mesh.nodes[0] - 1, :, 2] = 0
            if supports["right"] == 2:
                self.data[:, mesh.nodes[1] - 1, 2] = 0
        if element_type == "shell" or "shield": # Boundary conditions for wx and wy would be added later
            pass

    @property
    def fix(self):
        return self.data[:, :, 0]

    @property
    def fiy(self):
        return self.data[:, :, 1]

    @property
    def fiz(self):
        return self.data[:, :, 2]

    @property
    def rotations(self):
        return self.data


class MembraneForces(object):
    """Represents membrane forces over the shield or shell objects
    """

    def __init__(self, mesh):
        """ preallocate memory for 3D array """
        self.data = np.zeros((mesh.nodes[0], mesh.nodes[1], 3), dtype=np.float64)

    @property
    def nxx(self):
        return self.data[:, :, 0]

    @property
    def nyy(self):
        return self.data[:, :, 1]

    @property
    def nxy(self):
        return self.data[:, :, 2]

    @property
    def forces(self):
        return self.data


class MembraneMoment(object):
    """Represents membrane moments over the plate or shell objects
    """

    def __init__(self, mesh):
        """ preallocate memory for 3D array """
        self.data = np.zeros((mesh.nodes[0], mesh.nodes[1], 3), dtype=np.float64)

    @property
    def mxx(self):
        return self.data[:, :, 0]

    @property
    def myy(self):
        return self.data[:, :, 1]

    @property
    def mxy(self):
        return self.data[:, :, 2]

    @property
    def moments(self):
        return self.data


if __name__ == '__main__':    # TEST

    class AnyClass(object):            # This is only for testing mesh, supports would be imported from Prism class
        def __init__(self):
            self.supports = {
                            "bottom": 0,
                            "left": 0,
                            "right": 0,
                            "top": 0
                            }

        def sup(self):
            return self.supports

    AnyObject = AnyClass()
    prism = AnyObject.sup()

    test_mesh = Mesh(2, 5, 0.1)
    test_displacement_matrix = Displacements(test_mesh, "plate", prism)

    print(test_displacement_matrix.wz)