"""This part of program is responsible for applying appropriate boundary conditions and computing values of displacement
    in each node of regular mesh using finite differences method for plate objects"""

import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors


def compute_plate(displacements, Dp, q, supports, density, v, h):
    """Apply boundary conditions for plate objects and compute values of displacement in every node of mesh"""

    """ 1. Data """
    wf = displacements[2]  # displacements on z dimension
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
    p = np.ones((n, 1))

    """ 3. Setting equations for corner points (A) """

    if supports["top"] in [1, 2] or supports["left"] in [1, 2]:   # top-left
        p[0, 0] = 0
        A[0, 0] = 1  # after A*w=P it gives result 1*w1 = 0
    else:
        p[0, 0] = (q * density ** 4) / (4 * Dp)
        A[0, 0] = (3 + v) * (1 - v)
        A[0, 1] = -(3 + v) * (1 - v)
        A[0, 2] = (1 - v ** 2) / 2
        A[0, i] = -(3 + v) * (1 - v)
        A[0, i + 1] = 2 - 2 * v
        A[0, 2 * i] = (1 - v ** 2) / 2

    if supports["top"] in [1, 2] or supports["right"] in [1, 2]:   # top-right
        p[i - 1, 0] = 0
        A[i - 1, i - 1] = 1
    else:
        p[i - 1, 0] = (q * density ** 4) / (4 * Dp)
        A[i - 1, i - 1] = (3 + v) * (1 - v)
        A[i - 1, i - 2] = -(3 + v) * (1 - v)
        A[i - 1, i - 3] = (1 - v ** 2) / 2
        A[i - 1, i + i - 1] = -(3 + v) * (1 - v)
        A[i - 1, i + i - 2] = 2 - 2 * v
        A[i - 1, 2 * i + i - 1] = (1 - v ** 2) / 2

    if supports["bottom"] in [1, 2] or supports["left"] in [1, 2]:   # bottom-left
        p[(j - 1) * i, 0] = 0
        A[(j - 1) * i, (j - 1) * i] = 1
    else:
        p[(j - 1) * i, 0] = (q * density ** 4) / (4 * Dp)
        A[(j - 1) * i, (j - 1) * i] = (3 + v) * (1 - v)
        A[(j - 1) * i, (j - 1) * i + 1] = -(3 + v) * (1 - v)
        A[(j - 1) * i, (j - 1) * i + 2] = (1 - v ** 2) / 2
        A[(j - 1) * i, (j - 2) * i] = -(3 + v) * (1 - v)
        A[(j - 1) * i, (j - 2) * i + 1] = 2 - 2 * v
        A[(j - 1) * i, (j - 3) * i] = (1 - v ** 2) / 2

    if supports["bottom"] in [1, 2] or supports["right"] in [1, 2]:   # bottom-right
        p[(j - 1) * i + i - 1, 0] = 0
        A[(j - 1) * i + i - 1, (j - 1) * i + i - 1] = 1
    else:
        p[(j - 1) * i + i - 1, 0] = (q * density ** 4) / (4 * Dp)
        A[(j - 1) * i + i - 1, (j - 1) * i + i - 1] = (3 + v) * (1 - v)
        A[(j - 1) * i + i - 1, (j - 1) * i + i - 2] = -(3 + v) * (1 - v)
        A[(j - 1) * i + i - 1, (j - 1) * i + i - 3] = (1 - v ** 2) / 2
        A[(j - 1) * i + i - 1, (j - 2) * i + i - 1] = -(3 + v) * (1 - v)
        A[(j - 1) * i + i - 1, (j - 2) * i + i - 2] = 2 - 2 * v
        A[(j - 1) * i + i - 1, (j - 3) * i + i - 1] = (1 - v ** 2) / 2

    """ 4. Setting equations for corner-edge points (B) """

    def corner_edge_nodes(main_edge, secondary_edge, node, n1, n2, n3, n4, n5, n6, n7, n8,
                          _A=A, _p=p, _i=i, _j=j, _v=v, _density=density, _Dp=Dp, _q=q):
        if main_edge in [1, 2]:
            _p[node, 0] = 0
            _A[node, node] = 1
        elif secondary_edge == 0:
            _p[node, 0] = (_q * _density ** 4) / (2 * _Dp)
            _A[node, n1] = -(3 + _v) * (1 - _v)
            _A[node, n2] = (15 - 8 * _v - 5 * _v ** 2) / 2
            _A[node, n3] = -2 * (2 + _v) * (1 - _v)
            _A[node, n4] = (1 - _v ** 2) / 2
            _A[node, n5] = 2 - _v
            _A[node, n6] = -2 * (3 - _v)
            _A[node, n7] = 2 - _v
            _A[node, n8] = 1
        elif secondary_edge == 1:
            _p[node, 0] = (_q * _density ** 4) / (2 * _Dp)
            _A[node, n2] = (15 - 8 * _v - 5 * _v ** 2) / 2
            _A[node, n3] = -2 * (2 + _v) * (1 - _v)
            _A[node, n4] = (1 - _v ** 2) / 2
            _A[node, n6] = -2 * (3 - _v)
            _A[node, n7] = 2 - _v
            _A[node, n8] = 1
        else:
            _p[node, 0] = (_q * _density ** 4) / (2 * _Dp)
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

    def edge_nodes(edge, node, n1, n2, n3, n4, n5, n6, n7, n8, n9,
                          _A=A, _p=p, _i=i, _j=j, _v=v, _density=density, _Dp=Dp, _q=q):
        if edge in [1, 2]:
            _p[node, 0] = 0
            _A[node, node] = 1
        else:
            _p[node, 0] = (_q * _density ** 4) / (2 * _Dp)
            _A[node, n1] = (1 - _v ** 2) / 2
            _A[node, n2] = -2 * (2 + _v) * (1 - _v)
            _A[node, n3] = 8 - 4 * _v - 3 * _v ** 2
            _A[node, n4] = -2 * (2 + _v) * (1 - _v)
            _A[node, n5] = (1 - _v ** 2) / 2
            _A[node, n6] = 2 - _v
            _A[node, n7] = -2 * (3 - _v)
            _A[node, n8] = 2 - _v
            _A[node, n9] = 1
        return [_A, _p]

    for m in range(2, i - 2, 1):    # top
        [A, p] = edge_nodes(supports["top"],
                            m, m - 2, m - 1, m, m + 1, m + 2, i + m - 1, i + m, i + m + 1, 2 * i + m)
    for m in range(2 * i, (j - 2) * i, i):  # left
        [A, p] = edge_nodes(supports["left"],
                            m, -2 * i + m, -1 * i + m, m, i + m, 2 * i + m, -1 * i + m + 1, m + 1, i + m + 1, m + 2)
    for m in range((j - 1) * i + 2, (j - 1) * i + i - 2, 1):  # bottom
        [A, p] = edge_nodes(supports["bottom"],
                            m, m - 2, m - 1, m, m + 1, m + 2, -1 * i + m - 1, -1 * i + m, -1 * i + m + 1, -2 * i + m)
    for m in range(2 * i + i - 1, (j - 2) * i + i - 1, i):  # right
        [A, p] = edge_nodes(supports["right"],
                            m, -2 * i + m, -1 * i + m, m, i + m, 2 * i + m, -1 * i + m - 1, m - 1, i + m - 1, m - 2)

    """ 5. Setting equations for corner-mid points (D) """

    def corner_mid_nodes(horizontal_edge, vertical_edge, node, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11,
                          _A=A, _p=p, _i=i, _j=j, _v=v, _density=density, _Dp=Dp, _q=q):
        if vertical_edge == 0:
            if horizontal_edge == 0:
                _p[node, 0] = (_q * _density ** 4) / _Dp
                _A[node, n1] = 2 * (1 - _v)
                _A[node, n2] = -2 * (3 - _v)
                _A[node, n3] = 2 - _v
                _A[node, n4] = -2 * (3 - _v)
                _A[node, n5] = 18
                _A[node, n6] = -8
                _A[node, n7] = 1
                _A[node, n8] = 2 - _v
                _A[node, n9] = -8
                _A[node, n10] = 2
                _A[node, n11] = 1
            elif horizontal_edge == 1:
                _p[node, 0] = (_q * _density ** 4) / _Dp
                _A[node, n2] = -2 * (3 - _v)
                _A[node, n3] = 2 - _v
                _A[node, n5] = 18
                _A[node, n6] = -8
                _A[node, n7] = 1
                _A[node, n9] = -8
                _A[node, n10] = 2
                _A[node, n11] = 1
            else:
                _p[node, 0] = (_q * _density ** 4) / _Dp
                _A[node, n2] = -2 * (3 - _v)
                _A[node, n3] = 2 - _v
                _A[node, n5] = 20
                _A[node, n6] = -8
                _A[node, n7] = 1
                _A[node, n9] = -8
                _A[node, n10] = 2
                _A[node, n11] = 1

        elif vertical_edge == 1:
            if horizontal_edge == 0:
                _p[node, 0] = (_q * _density ** 4) / _Dp
                _A[node, n4] = -2 * (3 - _v)
                _A[node, n5] = 18
                _A[node, n6] = -8
                _A[node, n7] = 1
                _A[node, n8] = 2 - _v
                _A[node, n9] = -8
                _A[node, n10] = 2
                _A[node, n11] = 1
            elif horizontal_edge == 1:
                _p[node, 0] = (_q * _density ** 4) / _Dp
                _A[node, n5] = 18
                _A[node, n6] = -8
                _A[node, n7] = 1
                _A[node, n9] = -8
                _A[node, n10] = 2
                _A[node, n11] = 1
            else:
                _p[node, 0] = (_q * _density ** 4) / _Dp
                _A[node, n5] = 20
                _A[node, n6] = -8
                _A[node, n7] = 1
                _A[node, n9] = -8
                _A[node, n10] = 2
                _A[node, n11] = 1

        else:
            if horizontal_edge == 0:
                _p[node, 0] = (_q * _density ** 4) / _Dp
                _A[node, n4] = -2 * (3 - _v)
                _A[node, n5] = 20
                _A[node, n6] = -8
                _A[node, n7] = 1
                _A[node, n8] = 2 - _v
                _A[node, n9] = -8
                _A[node, n10] = 2
                _A[node, n11] = 1
            elif horizontal_edge == 1:
                _p[node, 0] = (_q * _density ** 4) / _Dp
                _A[node, n5] = 20
                _A[node, n6] = -8
                _A[node, n7] = 1
                _A[node, n9] = -8
                _A[node, n10] = 2
                _A[node, n11] = 1
            else:
                _p[node, 0] = (_q * _density ** 4) / _Dp
                _A[node, n5] = 22
                _A[node, n6] = -8
                _A[node, n7] = 1
                _A[node, n9] = -8
                _A[node, n10] = 2
                _A[node, n11] = 1
        return [_A, _p]

    [A, p] = corner_mid_nodes(supports["top"], supports["left"],  # top-left-mid
                              i + 1, 0, 1, 2, i, i + 1, i + 2, i + 3, 2 * i, 2 * i + 1, 2 * i + 2, 3 * i + 1)
    [A, p] = corner_mid_nodes(supports["top"], supports["right"],  # top-right-mid
                              i + i - 2, i - 1, i - 2, i - 3, i + i - 1, i + i - 2, i + i - 3,
                              i + i - 4, 2 * i + i - 1, 2 * i + i - 2, 2 * i + i - 3, 3 * i + i - 2)
    [A, p] = corner_mid_nodes(supports["bottom"], supports["left"],  # bottom-left-mid
                              (j - 2) * i + 1, (j - 1) * i, (j - 1) * i + 1, (j - 1) * i + 2, (j - 2) * i,
                              (j - 2) * i + 1, (j - 2) * i + 2, (j - 2) * i + 3, (j - 3) * i, (j - 3) * i + 1,
                              (j - 3) * i + 2, (j - 4) * i + 1)
    [A, p] = corner_mid_nodes(supports["bottom"], supports["right"],  # bottom-right-mid
                              (j - 2) * i + i - 2, (j - 1) * i + i - 1, (j - 1) * i + i - 2, (j - 1) * i + i - 3,
                              (j - 2) * i + i - 1, (j - 2) * i + i - 2, (j - 2) * i + i - 3, (j - 2) * i + i - 4,
                              (j - 3) * i + i - 1, (j - 3) * i + i - 2, (j - 3) * i + i - 3, (j - 4) * i + i - 2)

    """ 6. Setting equations for edge-mid points (E) """

    def edge_mid_nodes(edge, node, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12,
                          _A=A, _p=p, _i=i, _j=j, _v=v, _density=density, _Dp=Dp, _q=q):
        if edge == 0:
            _p[node, 0] = (_q * _density ** 4) / _Dp
            _A[node, n1] = 2 - _v
            _A[node, n2] = -2 * (3 - _v)
            _A[node, n3] = 2 - _v
            _A[node, n4] = 1
            _A[node, n5] = -8
            _A[node, n6] = 19
            _A[node, n7] = -8
            _A[node, n8] = 1
            _A[node, n9] = 2
            _A[node, n10] = -8
            _A[node, n11] = 2
            _A[node, n12] = 1
        elif edge == 1:
            _p[node, 0] = (_q * _density ** 4) / _Dp
            _A[node, n4] = 1
            _A[node, n5] = -8
            _A[node, n6] = 19
            _A[node, n7] = -8
            _A[node, n8] = 1
            _A[node, n9] = 2
            _A[node, n10] = -8
            _A[node, n11] = 2
            _A[node, n12] = 1
        else:
            _p[node, 0] = (_q * _density ** 4) / _Dp
            _A[node, n4] = 1
            _A[node, n5] = -8
            _A[node, n6] = 21
            _A[node, n7] = -8
            _A[node, n8] = 1
            _A[node, n9] = 2
            _A[node, n10] = -8
            _A[node, n11] = 2
            _A[node, n12] = 1
        return [_A, _p]

    for m in range(i + 2, i + i - 2, 1):    # top
        [A, p] = edge_mid_nodes(supports["top"],
                                m, -1 * i + m - 1, -1 * i + m, -1 * i + m + 1, m - 2, m - 1, m, m + 1, m + 2, i + m - 1,
                                i + m, i + m + 1, 2 * i + m)
    for m in range(2 * i + 1, (j - 2) * i + 1, i):  # left
        [A, p] = edge_mid_nodes(supports["left"],
                                m, -1 * i + m - 1, m - 1, i + m - 1, -2 * i + m, -1 * i + m, m, i + m, 2 * i + m,
                                -1 * i + m + 1, m + 1, i + m + 1, m + 2)
    for m in range((j - 2) * i + 2, (j - 2) * i + i - 2, 1):  # bottom
        [A, p] = edge_mid_nodes(supports["bottom"],
                                m, i + m - 1, i + m, i + m + 1, m - 2, m - 1, m, m + 1, m + 2, -1 * i + m - 1,
                                -1 * i + m, -1 * i + m + 1, -2 * i + m)
    for m in range(2*i + i - 2, (j - 2) * i + i - 2, i):  # right
        [A, p] = edge_mid_nodes(supports["right"],
                                m, -1 * i + m + 1, m + 1, i + m + 1, -2 * i + m, -1 * i + m, m, i + m, 2 * i + m,
                                -1 * i + m - 1, m - 1, i + m - 1, m - 2)

    """ 7. Setting equations for mid points (F) """

    def mid_nodes(node, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13,
                          _A=A, _p=p, _i=i, _j=j, _v=v, _density=density, _Dp=Dp, _q=q):

        _p[node, 0] = (_q * _density ** 4) / _Dp
        _A[node, n1] = 1
        _A[node, n2] = 2
        _A[node, n3] = -8
        _A[node, n4] = 2
        _A[node, n5] = 1
        _A[node, n6] = -8
        _A[node, n7] = 20
        _A[node, n8] = -8
        _A[node, n9] = 1
        _A[node, n10] = 2
        _A[node, n11] = -8
        _A[node, n12] = 2
        _A[node, n13] = 1
        return [_A, _p]

    for vm in range(2, j - 2, 1):
        for m in range(2, i - 2, 1):
            [A, p] = mid_nodes(vm * i + m, (vm - 2) * i + m, (vm - 1) * i + m - 1, (vm - 1) * i + m,
                               (vm - 1) * i + m + 1, vm * i + m - 2, vm * i + m - 1, vm * i + m, vm * i + m + 1,
                               vm * i + m + 2, (vm + 1) * i + m - 1, (vm + 1) * i + m, (vm + 1) * i + m + 1,
                               (vm + 2) * i + m)

    """ 8. Calculation of Aw = p equation """

    wf = np.linalg.solve(A, p)
    W = np.zeros((i, j))
    s = 0
    for vm in range(j):
        for m in range(i):
            W[m, vm] = round(wf[s, 0], 14)
            s += 1

    """ 9. Calculation of sigma x, sigma y and tau xy and moments from W matrix """

    blank = np.zeros((i,j))

    mxx = np.zeros((i, j))

    # corners

    mxx[0, 0] = (-Dp / density ** 2) * ((1+v) * W[0, 0] - 2 * W[1, 0] + 1 * W[2, 0] - 2*v * W[0, 1] + v * W[0, 2])
    mxx[i-1, 0] = (-Dp / density ** 2) * ((1 + v) * W[i-1, 0] - 2 * W[i-2, 0] + 1 * W[i-3, 0] - 2 * v * W[i-1, 1]
                                          + v * W[i-1, 2])
    mxx[0, j-1] = (-Dp / density ** 2) * ((1 + v) * W[0, j-1] - 2 * W[1, j-1] + 1 * W[2, j-1] - 2 * v * W[0, j-2]
                                          + v * W[0, j-3])
    mxx[i-1, j-1] = (-Dp / density ** 2) * ((1 + v) * W[i-1, j-1] - 2 * W[i-2, j-1] + 1 * W[i-3, j-1]
                                            - 2 * v * W[i-1, j-2] + v * W[i-1, j-3])

    # edges

    for m in range(i-2):  # top
        m += 1
        mxx[m, 0] = (-Dp / density ** 2) * (1 * W[m-1, 0] + (-2+v) * W[m, 0] + 1 * W[m+1, 0]
                                            - 2*v * W[m, 1] + v * W[m, 2])
    for m in range(i-2):  # bottom
        m += 1
        mxx[m, j-1] = (-Dp / density ** 2) * (1 * W[m-1, j-1] + (-2+v) * W[m, j-1] + 1 * W[m+1, j-1]
                                            - 2*v * W[m, j-2] + v * W[m, j-3])
    for m in range(j-2):  # left
        m += 1
        mxx[0, m] = (-Dp / density ** 2) * (v * W[0, m-1] + (-2*v+1) * W[0, m] + v * W[0, m+1]
                                            - 2 * W[1, m] + 1 * W[2, m])
    for m in range(j - 2):  # right
        m += 1
        mxx[i-1, m] = (-Dp / density ** 2) * (v * W[i-1, m - 1] + (-2 * v + 1) * W[i-1, m] + v * W[i-1, m + 1]
                                            - 2 * W[i-2, m] + 1 * W[i-3, m])

    # central points

    for vm in range(j-2):
        vm += 1
        for m in range(i-2):
            m += 1
            mxx[m, vm] = (-Dp / density ** 2) * (1 * W[m-1, vm] + v * W[m, vm-1]+ (-2-2*v) * W[m, vm] + 1 * W[m+1, vm]
                                                 + v * W[m, vm+1])

    myy = np.zeros((i, j))

    # corners

    myy[0, 0] = (-Dp / density ** 2) * ((1 + v) * W[0, 0] - 2*v * W[1, 0] + v * W[2, 0] - 2 * W[0, 1] + 1 * W[0, 2])
    myy[i - 1, 0] = (-Dp / density ** 2) * (
                (1 + v) * W[i - 1, 0] - 2*v * W[i - 2, 0] + v * W[i - 3, 0] - 2 * W[i - 1, 1]
                + 1 * W[i - 1, 2])
    myy[0, j - 1] = (-Dp / density ** 2) * (
                (1 + v) * W[0, j - 1] - 2 * v * W[1, j - 1] + v * W[2, j - 1] - 2 * W[0, j - 2]
                + 1 * W[0, j - 3])
    myy[i - 1, j - 1] = (-Dp / density ** 2) * ((1 + v) * W[i - 1, j - 1] - 2 * v * W[i - 2, j - 1] +
                                                v * W[i - 3, j - 1] - 2 * W[i - 1, j - 2] + 1 * W[i - 1, j - 3])

    # edges

    for m in range(i - 2):  # top
        m += 1
        myy[m, 0] = (-Dp / density ** 2) * (v * W[m - 1, 0] + (-2*v + 1) * W[m, 0] + v * W[m + 1, 0]
                                            - 2 * W[m, 1] + 1 * W[m, 2])
    for m in range(i - 2):  # bottom
        m += 1
        myy[m, j - 1] = (-Dp / density ** 2) * (v * W[m - 1, j - 1] + (-2*v + 1) * W[m, j - 1] + v * W[m + 1, j - 1]
                                                - 2 * W[m, j - 2] + 1 * W[m, j - 3])
    for m in range(j - 2):  # left
        m += 1
        myy[0, m] = (-Dp / density ** 2) * (1 * W[0, m - 1] + (-2 + v) * W[0, m] + 1 * W[0, m + 1]
                                            - 2 * v * W[1, m] + v * W[2, m])
    for m in range(j - 2):  # right
        m += 1
        myy[i - 1, m] = (-Dp / density ** 2) * (1 * W[i - 1, m - 1] + (-2 + v) * W[i - 1, m] + 1 * W[i - 1, m + 1]
                                                - 2 * v * W[i - 2, m] + v * W[i - 3, m])

    # central points

    for vm in range(j - 2):
        vm += 1
        for m in range(i - 2):
            m += 1
            myy[m, vm] = (-Dp / density ** 2) * (
                        v * W[m - 1, vm] + 1 * W[m, vm - 1] + (-2 - 2 * v) * W[m, vm] + v * W[m + 1, vm]
                        + 1 * W[m, vm + 1])

    mxy = np.zeros((i, j))

    mxy[0, 0] = ((Dp * (1-v))/(density ** 2)) * (W[0, 0] - W[1, 0] - W[0, 1] + W[1, 1])
    mxy[i - 1, 0] = ((-Dp * (1-v))/(density ** 2)) * (W[i - 1, 0] - W[i - 2, 0] - W[i - 1, 1] + W[i - 2, 1])
    mxy[0, j - 1] = ((-Dp * (1-v))/(density ** 2)) * (W[0, j - 1] - W[1, j - 1] - W[0, j - 2] + W[1, j - 2])
    mxy[i - 1, j - 1] = ((Dp * (1-v))/(density ** 2)) * (W[i - 1, j - 1] - W[i - 2, j - 1] - W[i - 1, j - 2]
                                                          + W[i - 2, j - 2])

    # edges

    for m in range(i - 2):  # top
        m += 1
        mxy[m, 0] = ((Dp * (1-v))/(2*density ** 2)) * (W[m-1, 0] - W[m+1, 0] - W[m-1, 1] + W[m+1, 1])
    for m in range(i - 2):  # bottom
        m += 1
        mxy[m, j - 1] = ((-Dp * (1-v))/(2*density ** 2)) * (W[m-1, j - 1] - W[m+1, j - 1] - W[m-1, j - 2]
                                                            + W[m+1, j - 2])
    for m in range(j - 2):  # left
        m += 1
        mxy[0, m] = ((Dp * (1-v))/(2*density ** 2)) * (W[0, m-1] - W[0, m+1] - W[1, m-1] + W[1, m+1])
    for m in range(j - 2):  # right
        m += 1
        mxy[i - 1, m] = ((-Dp * (1-v))/(2*density ** 2)) * (W[i - 1, m-1] - W[i - 1, m+1] - W[i - 2, m-1]
                                                            + W[i - 2, m+1])

    # central points

    for vm in range(j - 2):
        vm += 1
        for m in range(i - 2):
            m += 1
            mxy[m, vm] = ((-Dp * (1-v))/(4*density ** 2)) * (-W[m - 1, vm-1] + W[m + 1, vm - 1] + W[m - 1, vm + 1]
                                                             - W[m + 1, vm + 1])

    sigma_x = (12*mxx*0.5*h)/(h**3)

    sigma_y = (12 * myy * 0.5 * h) / (h ** 3)

    tau_xy = (12 * mxy * 0.5 * h) / (h ** 3)

    return [blank, blank, W.T, sigma_x.T, sigma_y.T, tau_xy.T, mxx.T, myy.T, mxy.T, blank, blank, blank]


if __name__ == '__main__':

    class TestMeshClass(object):
        def __init__(self):
            self.data = [None, None, np.zeros((9, 9))]


    test_class = TestMeshClass()
    test_mesh = test_class.data
    test_flexural_stiffness = 0.2
    test_load = 2000
    test_supports = {           # 0 - free end  1 - hinged  2 - fixed
                    "bottom": 0,
                    "left": 0,
                    "right": 2,
                    "top": 0
                    }
    test_density = 0.5
    test_poisson_ratio = 0.3
    test_thickness = 0.25
    start = datetime.datetime.now()
    g = compute_plate(test_mesh, test_flexural_stiffness, test_load, test_supports, test_density, test_poisson_ratio,
                      test_thickness)
    duration = datetime.datetime.now() - start   # time of calculations
    print(g[2])
    print(duration)
    fig, ax = plt.subplots(1, 2)
    cmap = cm.get_cmap(name='jet', lut=40)
    norm = matplotlib.colors.Normalize()
    mappable = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    mappable.set_array(g[2])
    mappable.autoscale()
    matplotlib.pyplot.colorbar(mappable, ax[1])
    ax[0].imshow(g[2], extent=(0, 50, 0, 50), interpolation='hermite', cmap=cmap)
    mappable.changed()
    plt.show()
