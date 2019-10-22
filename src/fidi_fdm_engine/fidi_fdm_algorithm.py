"""This part of program is responsible for applying appropriate boundary conditions and computing values of displacement
    in each node of regular mesh using finite differences method"""

import numpy as np


def compute_plate(displacements, Dp, q, supports):
    """Apply boundary conditions for plate objects and compute values of displacement in every node of mesh"""

    """ 1. Data """

    wf = displacements.data[2].shape  # displacements on z dimension
    (i, j) = wf.shape  # i/j - number of nodes on x/y dimension
    n = i * j  # amount of nodes

    """ 2. Displacements can be computed using equation Aw = p """
    #    A - assembled matrix of FDM scheme equations, w - vector of displacements, p - vector of load
    #    Initial setting of matrices :

    A = np.zeros(n)
    w = np.zeros((1, n))
    p = np.zeros((1, n))

    #   Legend of nodes naming for equation assembling :
    #
    #     [ A B C C C B A ]
    #     [ B D E E E D B ]
    #     [ C E F F F E C ]
    # W = [ C E F F F E C ]
    #     [ C E F F F E C ]
    #     [ B D E E E D B ]
    #     [ A B C C C B A ]

    """ 3. Setting equations for corner points (A) """

    """ 4. Setting equations for corner-edge points (B) """

    """ 5. Setting equations for edge points (C) """

    """ 5. Setting equations for corner-mid points (D) """

    """ 6. Setting equations for edge-mid points (E) """

    """ 7. Setting equations for mid points (F) """

    """ 8. Calculation of Aw = p equation """

    return wf


def compute_shield(displacements, Ds, q, supports):
    """Apply boundary conditions for shield objects and compute values of displacement in every node of mesh"""
    pass


if __name__ == '__main__':
    pass
