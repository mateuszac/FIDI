"""This part of program is responsible for applying appropriate boundary conditions and computing values of displacement
    in each node of regular mesh using finite differences method"""

import numpy as np


def compute_plate(displacements, Dp, q, supports, density, v):
    """Apply boundary conditions for plate objects and compute values of displacement in every node of mesh"""

    """ 1. Data """

    wf = displacements.data[2]  # displacements on z dimension
    (i, j) = wf.shape  # i/j - number of nodes on x/y dimension
    n = i * j  # amount of nodes

    """ 2. Displacements can be computed using equation Aw = p
           Legend of nodes naming for equation assembling :
    
               [ A B C C C B A ]
               [ B D E E E D B ]
               [ C E F F F E C ]
           W = [ C E F F F E C ]
               [ C E F F F E C ]
               [ B D E E E D B ]
               [ A B C C C B A ]
            
            w vector is flattened version of wf matrix, for i,j shape matrix :
            w[0] element is equal to wf[0, 0],
            w[0*i + i-1] is equal to wf[0, i-1]  
            w[1 * i] is equal to wf[1, 0]
            w[(j-1)*i] is equal to wf[j-1, 0]
            w[(j-1)*i + i-1] is equal  to wf[j-1, i-1]
            
            while assembling A matrix in A[a,b] a is a number of node in w vector for which equation is formed and b is
            a number of node in w vector for which coefficient is applied according to FDM scheme.
    """

    #    A - assembled matrix of FDM scheme equations, w - vector of displacements, p - vector of load
    #    Initial setting of matrices :

    A = np.zeros((n, n))
    w = wf.flatten()
    p = np.ones((n, 1))

    """ 3. Setting equations for corner points (A) """

    if supports["top"] in [1, 2] or supports["left"] in [1, 2]:   # top-left
        p[0, 0] = 0
        A[0, 0] = 1  # after A*w=P it gives result 1*w1 = 0
    else:
        p[0, 0] = (q * density ** 4) / 4 * Dp
        A[0, 0] = (3 + v) * (1 - v)
        A[0, 1] = -(3 + v) * (1 - v)
        A[0, 2] = (1 - v ** 2) / 2
        A[0, i] = -(3 + v) * (1 - v)
        A[0, i + 1] = 2 * (3 - v)
        A[0, 2 * i] = (1 - v ** 2) / 2

    if supports["top"] in [1, 2] or supports["right"] in [1, 2]:   # top-right
        p[i - 1, 0] = 0
        A[i - 1, i - 1] = 1
    else:
        p[i - 1, 0] = (q * density ** 4) / 4 * Dp
        A[i - 1, i - 1] = (3 + v) * (1 - v)
        A[i - 1, i - 2] = -(3 + v) * (1 - v)
        A[i - 1, i - 3] = (1 - v ** 2) / 2
        A[i - 1, i + i - 1] = -(3 + v) * (1 - v)
        A[i - 1, i + i - 2] = 2 * (3 - v)
        A[i - 1, 2 * i + i - 1] = (1 - v ** 2) / 2

    if supports["bottom"] in [1, 2] or supports["left"] in [1, 2]:   # bottom-left
        p[(j - 1) * i, 0] = 0
        A[(j - 1) * i, (j - 1) * i] = 1
    else:
        p[(j - 1) * i, 0] = (q * density ** 4) / 4 * Dp
        A[(j - 1) * i, (j - 1) * i] = (3 + v) * (1 - v)
        A[(j - 1) * i, (j - 1) * i + 1] = -(3 + v) * (1 - v)
        A[(j - 1) * i, (j - 1) * i + 2] = (1 - v ** 2) / 2
        A[(j - 1) * i, (j - 2) * i] = -(3 + v) * (1 - v)
        A[(j - 1) * i, (j - 2) * i + 1] = 2 * (3 - v)
        A[(j - 1) * i, (j - 3) * i] = (1 - v ** 2) / 2

    if supports["bottom"] in [1, 2] or supports["right"] in [1, 2]:   # bottom-right
        p[(j - 1) * i + i - 1, 0] = 0
        A[(j - 1) * i + i - 1, (j - 1) * i + i - 1] = 1
    else:
        p[(j - 1) * i + i - 1, 0] = (q * density ** 4) / 4 * Dp
        A[(j - 1) * i + i - 1, (j - 1) * i + i - 1] = (3 + v) * (1 - v)
        A[(j - 1) * i + i - 1, (j - 1) * i + i - 2] = -(3 + v) * (1 - v)
        A[(j - 1) * i + i - 1, (j - 1) * i + i - 3] = (1 - v ** 2) / 2
        A[(j - 1) * i + i - 1, (j - 2) * i + i - 1] = -(3 + v) * (1 - v)
        A[(j - 1) * i + i - 1, (j - 2) * i + i - 2] = 2 * (3 - v)
        A[(j - 1) * i + i - 1, (j - 3) * i + i - 1] = (1 - v ** 2) / 2

    """ 4. Setting equations for corner-edge points (B) """

    def corner_edge_nodes(main_edge, secondary_edge, node, n1, n2, n3, n4, n5, n6, n7, n8,
                          _A=A, _p=p, _i=i, _j=j, _v=v, _density=density, _Dp=Dp, _q=q):
        if main_edge in [1, 2]:
            _p[node, 0] = 0
            _A[node, node] = 1
        elif secondary_edge == 0:
            _p[node, 0] = (_q * _density ** 4) / 2 * _Dp
            _A[node, n1] = -(3 + _v) * (1 - _v)
            _A[node, n2] = (15 - 8 * _v - 5 * _v ** 2) / 2
            _A[node, n3] = -2 * (2 + _v) * (1 - _v)
            _A[node, n4] = (1 - _v ** 2) / 2
            _A[node, n5] = 2 - _v
            _A[node, n6] = -2 * (3 - _v)
            _A[node, n7] = 2 - _v
            _A[node, n8] = 1
        elif secondary_edge == 1:
            _A[node, n2] = (15 - 8 * _v - 5 * _v ** 2) / 2
            _A[node, n3] = -2 * (2 + _v) * (1 - _v)
            _A[node, n4] = (1 - _v ** 2) / 2
            _A[node, n6] = -2 * (3 - _v)
            _A[node, n7] = 2 - _v
            _A[node, n8] = 1
        else:
            _p[node, 0] = (_q * _density ** 4) / 2 * _Dp
            _A[node, n2] = (17 - 8 * _v - 7 * _v ** 2) / 2
            _A[node, n3] = -2 * (2 + _v) * (1 - _v)
            _A[node, n4] = (1 - _v ** 2) / 2
            _A[node, n6] = -2 * (3 - _v)
            _A[node, n7] = 2 - _v
            _A[node, n8] = 1
        return [_A, _p]

    [A, p] = corner_edge_nodes(supports["top"], supports["left"],   # top-left-top
                               1, 0, 1, 2, 3, i, i + 1, i + 2, 2 * i + 1)
    [A, p] = corner_edge_nodes(supports["left"], supports["top"],  # top-left-left
                               i, 0, i, 2 * i, 3 * i, 1, i + 1, 2 * i + 1, i + 2)
    [A, p] = corner_edge_nodes(supports["top"], supports["right"],  # top-right-top
                               i - 2, i - 1, i - 2, i - 3, i - 4, i + i - 1, i + i - 2, i + i - 3, 2 * i + i - 2)
    [A, p] = corner_edge_nodes(supports["right"], supports["top"],  # top-right-right
                               i + i - 1, i - 1, i + i - 1, 2 * i + i - 1, 3 * i + i - 1, i - 2, i + i - 2,
                               2 * i + i - 2, i + i - 3)
    [A, p] = corner_edge_nodes(supports["bottom"], supports["left"],  # bottom-left-bottom
                               (j - 1) * i + 1, (j - 1) * i, (j - 1) * i + 1, (j - 1) * i + 2, (j - 1) * i + 3,
                               (j - 2) * i, (j - 2) * i + 1, (j - 2) * i + 2, (j - 3) * i + 1)
    [A, p] = corner_edge_nodes(supports["left"], supports["bottom"],  # bottom-left-left
                               (j - 2) * i, (j - 1) * i, (j - 2) * i, (j - 3) * i, (j - 4) * i,
                               (j - 1) * i + 1, (j - 2) * i + 1, (j - 3) * i + 1, (j - 2) * i + 2)
    [A, p] = corner_edge_nodes(supports["bottom"], supports["right"],  # bottom-right-bottom
                               (j - 1) * i + i - 2, (j - 1) * i + i - 1, (j - 1) * i + i - 2, (j - 1) * i + i - 3,
                               (j - 1) * i + i - 4, (j - 2) * i + i - 1, (j - 2) * i + i - 2, (j - 2) * i + i - 3,
                               (j - 3) * i + i - 2)
    [A, p] = corner_edge_nodes(supports["right"], supports["bottom"],  # bottom-right-right
                               (j - 2) * i + i - 1, (j - 1) * i + i - 1, (j - 2) * i + i - 1, (j - 3) * i + i - 1,
                               (j - 4) * i + i - 1, (j - 1) * i + i - 2, (j - 2) * i + i - 2, (j - 3) * i + i - 2,
                               (j - 2) * i + i - 3)

    """ 5. Setting equations for edge points (C) """

    """ 5. Setting equations for corner-mid points (D) """

    """ 6. Setting equations for edge-mid points (E) """

    """ 7. Setting equations for mid points (F) """

    """ 8. Calculation of Aw = p equation """
    wf = A  # This line would be removed, it is only for testing A matrix
    return wf


def compute_shield(displacements, Ds, q, supports, density, v):
    """Apply boundary conditions for shield objects and compute values of displacement in every node of mesh"""
    pass


if __name__ == '__main__':

    class Anyclass(object):
        def __init__(self):
            self.data = [np.ones((4, 4)), np.ones((5, 5)), np.ones((4, 4))]


    a = Anyclass()
    b = 2
    c = 5
    d = {
        "bottom": 1,
        "left": 1,
        "right": 0,
        "top": 1
        }
    e = 1
    f = 0.3
    g = compute_plate(a, b, c, d, e, f)
    print(g)
