"""This part of program is responsible for generating appropriate mesh for finite differences method calculations"""
import numpy as np


class Mesh(object):
    """Creation of empty mesh matrix"""
    def __init__(self, width, height, density):
        Nx = int(width/density)
        Ny = int(height/density)
        self.nodes = (Nx, Ny)

    @property
    def resolution(self):
        return self.nodes


class Displacements(object):
    """ Matrix containing displacements of element """

    def __init__(self, mesh):
        """ preallocate memory for 3D array """
        self.data = np.zeros((3, mesh.nodes[1], mesh.nodes[0]), dtype=np.float64)


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

    test_mesh = Mesh(0.1, 5, 2)
    test_displacement_matrix = Displacements(test_mesh)

    print(test_displacement_matrix.data)
