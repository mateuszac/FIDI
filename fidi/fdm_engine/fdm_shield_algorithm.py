"""This part of program is responsible for applying appropriate boundary conditions and computing values of displacement
    in each node of regular mesh using finite differences method for shield objects"""

import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors


def compute_shield_one_direction(displacements, E, loads, supports, density, v, thickness, direction):
    """Apply boundary conditions for shield objects and compute values of displacement in every node of mesh"""

    """ 1. Data """

    uf = displacements[0]  # displacements on x dimension
    vf = displacements[1]  # displacements on y dimension
    (i, j) = uf.shape  # i/j - number of nodes on x/y dimension
    i += 2     # adding fictitious nodes
    j += 2     # adding fictitious nodes
    n = i * j  # amount of nodes

    load_xB = loads["x_direction"]["bottom"]
    load_xT = loads["x_direction"]["top"]
    load_xL = loads["x_direction"]["left"]
    load_xR = loads["x_direction"]["right"]
    load_yB = loads["y_direction"]["bottom"]
    load_yT = loads["y_direction"]["top"]
    load_yL = loads["y_direction"]["left"]
    load_yR = loads["y_direction"]["right"]

    G = E/(2*(1+v))
    Ds = E/(1-v**2)

    """ 2. Starting from the idea of Airy function, suppose that in case of isotropic material there is F(x,y)
           function of which partial derivatives give the projections of displacements as it follows:
           
           u = alpha1*Fxx + alpha2*Fxy + alpha3*Fyy 
           v = alpha4*Fxx + alpha5*Fxy + alpha6*Fyy 
           
           where u is projection on x axis, v on y axis and alphas are coefficients to be determined.
    
           Assuming load only in X direction we may determine alpha coefficients according to theory
           attached to Master's thesis, then we may do the same with only Y directed load. Eventually using
           superposition overall displacements are obtained by summing u and v for X directed load and Y directed load.
           
           Legend of nodes naming for equation assembling :

                 X   A3 B2 B2 B2 B2 B2 A3   X
                A2 [ A1 B1 B1 B1 B1 B1 A1 ] A2
                B2 [ B1 C1 C1 C1 C1 C1 B1 ] B2
                B2 [ B1 C1 C1 C1 C1 C1 B1 ] B2
           F =  B2 [ B1 C1 C1 C1 C1 C1 B1 ] B2
                B2 [ B1 C1 C1 C1 C1 C1 B1 ] B2
                B2 [ B1 C1 C1 C1 C1 C1 B1 ] B2
                A2 [ A1 B1 B1 B1 B1 B1 A1 ] A2
                 X   A3 B2 B2 B2 B2 B2 A3   X

            X - fictitious that does not belong to domain
            f vector is flattened version of F matrix, for i,j shape matrix :
            f[0] element is equal to F[0, 0], (that is fictitious node - not belonging to domain)
            f[0*i + i-1] is equal to F[0, i-1]  
            f[1 * i] is equal to F[1, 0]
            f[(j-1)*i] is equal to F[j-1, 0]
            f[(j-1)*i + i-1] is equal  to F[j-1, i-1]

    """

    #    A - assembled matrix of FDM scheme equations, f - vector of Airy function F values,
    #    p - vector of load/displacement (depends on boundary condition type)

    A = np.zeros((n, n))
    p = np.ones((n, 1))

    """ 3. Calculation of all coefficients and setting corner fictitious nodes, that does not belong to domain """

    # for vertical direction of load
    alpha1v = 0
    alpha2v = 1
    alpha3v = 0
    alpha4v = -Ds/(v*Ds+G)
    alpha5v = 0
    alpha6v = -G/(v*Ds+G)

    # for horizontal direction of load
    alpha1h = -G / (v * Ds + G)
    alpha2h = 0
    alpha3h = -Ds / (v * Ds + G)
    alpha4h = 0
    alpha5h = 1
    alpha6h = 0

    # for both directions
    beta0 = -1
    beta1 = (-G * Ds / (v * Ds + G))
    beta2 = (v * Ds + G - (Ds ** 2 + G ** 2) / (v * Ds + G))
    beta3 = (-G * Ds / (v * Ds + G))

    p[0, 0] = 0
    A[0, 0] = 1  # after A*f=P it gives result 1*f(top-left) = 0
    p[i - 1, 0] = 0
    A[i - 1, i - 1] = 1  # after A*f=P it gives result 1*f(top-right) = 0
    p[(j - 1) * i, 0] = 0
    A[(j - 1) * i, (j - 1) * i] = 1  # after A*f=P it gives result 1*f(bottom-left) = 0
    p[(j - 1) * i + i - 1, 0] = 0
    A[(j - 1) * i + i - 1, (j - 1) * i + i - 1] = 1  # after A*f=P it gives result 1*f(bottom-right) = 0

    #  for one direction of load

    if direction == "vertical":
        a1 = alpha1v
        a2 = alpha2v
        a3 = alpha3v
        a4 = alpha4v
        a5 = alpha5v
        a6 = alpha6v
        load_xB = 0
        load_xT = 0
        load_xL = 0
        load_xR = 0
    else:
        a1 = alpha1h
        a2 = alpha2h
        a3 = alpha3h
        a4 = alpha4h
        a5 = alpha5h
        a6 = alpha6h
        load_yB = 0
        load_yT = 0
        load_yL = 0
        load_yR = 0

    # C coefficients for sigma_x boundary conditions

    cx1 = Ds * a1
    cx2 = Ds * a2 + v * Ds * a4
    cx3 = Ds * a3 + v * Ds * a5
    cx4 = Ds * a6

    # C coefficients for sigma_y boundary conditions

    cy1 = v * Ds * a1
    cy2 = v * Ds * a2 + Ds * a4
    cy3 = v * Ds * a3 + Ds * a5
    cy4 = v * Ds * a6

    # C coefficients for tau_xy boundary conditions

    ct1 = G * a4
    ct2 = G * a1 + G * a5
    ct3 = G * a2 + G * a6
    ct4 = G * a3

    """ 4. Setting equations for corner points (A) for displacement boundary conditions """

    if supports["top"] in [1, 2] or supports["left"] in [1, 2]:  # 3 equations for corner point

        p[1, 0] = 0
        A[1, 1] = 1
        A[1, i] = -1  # after A*f=P it gives result f1-f2 = 0, so f1 = f2 for 2 fictitious nodes

        p[i, 0] = 0 * density ** 2  # support or forced displacement value in vertical direction
        A[i, i] = a1
        A[i, 1] = a3
        A[i, i + 1] = -2 * a1 - a2 - 2 * a3
        A[i, i + 2] = a1 + a2
        A[i, 2 * i + 1] = a2 + a3
        A[i, 2 * i + 2] = -a2

        p[i + 1, 0] = 0 * density ** 2  # support or forced displacement value in horizontal direction
        A[i + 1, i] = a4
        A[i + 1, 1] = a6
        A[i + 1, i + 1] = -2 * a4 - a5 - 2 * a6
        A[i + 1, i + 2] = a4 + a5
        A[i + 1, 2 * i + 1] = a5 + a6
        A[i + 1, 2 * i + 2] = -a5

    else:
        pass  # it mean that for this node static boundaries will be applied

    if supports["top"] in [1, 2] or supports["right"] in [1, 2]:  # 3 equations for corner point

        p[i - 2, 0] = 0
        A[i - 2, i - 2] = 1
        A[i - 2, 2 * i - 1] = -1  # after A*f=P it gives result f1-f2 = 0, so f1 = f2 for 2 fictitious nodes

        p[2 * i - 2, 0] = 0 * density ** 2  # support or forced displacement value in vertical direction
        A[2 * i - 2, i - 2] = a3
        A[2 * i - 2, 2 * i - 3] = a1 - a2
        A[2 * i - 2, 2 * i - 2] = -2 * a1 + a2 - 2 * a3
        A[2 * i - 2, 2 * i - 1] = a1
        A[2 * i - 2, 3 * i - 3] = a2
        A[2 * i - 2, 3 * i - 2] = -a2 + a3

        p[2 * i - 1, 0] = 0 * density ** 2  # support or forced displacement value in horizontal direction
        A[2 * i - 1, i - 2] = a6
        A[2 * i - 1, 2 * i - 3] = a4 - a5
        A[2 * i - 1, 2 * i - 2] = -2 * a4 + a5 - 2 * a6
        A[2 * i - 1, 2 * i - 1] = a4
        A[2 * i - 1, 3 * i - 3] = a5
        A[2 * i - 1, 3 * i - 2] = -a5 + a6

    else:
        pass  # it mean that for this node static boundaries will be applied

    if supports["bottom"] in [1, 2] or supports["left"] in [1, 2]:  # 3 equations for corner point

        p[(j - 2) * i, 0] = 0
        A[(j - 2) * i, (j - 2) * i] = 1
        A[(j - 2) * i, (j - 1) * i + 1] = -1  # after A*f=P it gives result f1-f2 = 0, so f1 = f2 for 2 fictitious nodes

        p[(j - 2) * i + 1, 0] = 0 * density ** 2  # support or forced displacement value in vertical direction
        A[(j - 2) * i + 1, (j - 3) * i + 1] = -a2 + a3
        A[(j - 2) * i + 1, (j - 3) * i + 2] = a2
        A[(j - 2) * i + 1, (j - 2) * i] = a1
        A[(j - 2) * i + 1, (j - 2) * i + 1] = -2 * a1 + a2 - 2 * a3
        A[(j - 2) * i + 1, (j - 2) * i + 2] = a1 - a2
        A[(j - 2) * i + 1, (j - 1) * i + 1] = a3

        p[(j - 1) * i + 1, 0] = 0 * density ** 2  # support or forced displacement value in horizontal direction
        A[(j - 1) * i + 1, (j - 3) * i + 1] = -a5 + a6
        A[(j - 1) * i + 1, (j - 3) * i + 2] = a5
        A[(j - 1) * i + 1, (j - 2) * i] = a4
        A[(j - 1) * i + 1, (j - 2) * i + 1] = -2 * a4 + a5 - 2 * a6
        A[(j - 1) * i + 1, (j - 2) * i + 2] = a4 - a5
        A[(j - 1) * i + 1, (j - 1) * i + 1] = a6

    else:
        pass  # it mean that for this node static boundaries will be applied

    if supports["bottom"] in [1, 2] or supports["right"] in [1, 2]:  # 3 equations for corner point

        p[(j - 2) * i + i - 1, 0] = 0
        A[(j - 2) * i + i - 1, (j - 2) * i + i - 1] = 1
        A[(j - 2) * i + i - 1, (j - 1) * i + i - 2] = -1

        p[(j - 2) * i + i - 2, 0] = 0 * density ** 2
        A[(j - 2) * i + i - 2, (j - 3) * i + i - 3] = -a2
        A[(j - 2) * i + i - 2, (j - 3) * i + i - 2] = a2 + a3
        A[(j - 2) * i + i - 2, (j - 2) * i + i - 3] = a1 + a2
        A[(j - 2) * i + i - 2, (j - 2) * i + i - 2] = -2 * a1 - a2 - 2 * a3
        A[(j - 2) * i + i - 2, (j - 2) * i + i - 1] = a1
        A[(j - 2) * i + i - 2, (j - 1) * i + i - 2] = a3

        p[(j - 1) * i + i - 2, 0] = 0 * density ** 2
        A[(j - 1) * i + i - 2, (j - 3) * i + i - 3] = -a5
        A[(j - 1) * i + i - 2, (j - 3) * i + i - 2] = a5 + a6
        A[(j - 1) * i + i - 2, (j - 2) * i + i - 3] = a4 + a5
        A[(j - 1) * i + i - 2, (j - 2) * i + i - 2] = -2 * a4 - a5 - 2 * a6
        A[(j - 1) * i + i - 2, (j - 2) * i + i - 1] = a4
        A[(j - 1) * i + i - 2, (j - 1) * i + i - 2] = a6

    else:
        pass  # it mean that for this node static boundaries will be applied

    """ 5. Setting equations for corner points (A) for statical boundary conditions """

    if supports["top"] == 0 and supports["left"] == 0:  # 3 equations for corner point

        p[1, 0] = 0
        A[1, 1] = 1
        A[1, i] = -1  # after A*f=P it gives result f1-f2 = 0, so f1 = f2 for 2 fictitious nodes

        p[i, 0] = -(0.5*load_xL + 0.5*load_xT) * density ** 3  # sig_x = 0.5*sig_x_load + 0.5*tau_xy_load # x with -
        A[i, i] = -cx1 + cx2
        A[i, 1] = -cx3 + cx4
        A[i, 2] = cx3
        A[i, i + 1] = 3 * cx1 - 2 * cx2 + 2 * cx3 - 3 * cx4
        A[i, i + 2] = -3 * cx1 + cx2 - 2 * cx3
        A[i, i + 3] = cx1
        A[i, 2 * i] = -cx2
        A[i, 2 * i + 1] = 2 * cx2 - cx3 + 3 * cx4
        A[i, 2 * i + 2] = -cx2 + cx3
        A[i, 3 * i + 1] = -cx4

        p[i + 1, 0] = (0.5*load_yL + 0.5*load_yT) * density ** 3  # sig_y = 0.5*sig_y_load + 0.5*tau_xy_load # y with +
        A[i + 1, i] = -cy1 + cy2
        A[i + 1, 1] = -cy3 + cy4
        A[i + 1, 2] = cy3
        A[i + 1, i + 1] = 3 * cy1 - 2 * cy2 + 2 * cy3 - 3 * cy4
        A[i + 1, i + 2] = -3 * cy1 + cy2 - 2 * cy3
        A[i + 1, i + 3] = cy1
        A[i + 1, 2 * i] = -cy2
        A[i + 1, 2 * i + 1] = 2 * cy2 - cy3 + 3 * cy4
        A[i + 1, 2 * i + 2] = -cy2 + cy3
        A[i + 1, 3 * i + 1] = -cy4

    else:
        pass  # it mean that for this node displacement boundaries will be applied

    if supports["top"] == 0 and supports["right"] == 0:  # 3 equations for corner point

        p[i - 2, 0] = 0
        A[i - 2, i - 2] = 1
        A[i - 2, 2 * i - 1] = -1  # after A*f=P it gives result f1-f2 = 0, so f1 = f2 for 2 fictitious nodes

        p[2 * i - 2, 0] = (0.5 * load_xT + 0.5 * load_xR) * density ** 3  # sig_x = 0.5*sig_x_load + 0.5*tau_xy_load
        A[2 * i - 2, i - 3] = -cx3
        A[2 * i - 2, i - 2] = cx3 + cx4
        A[2 * i - 2, 2 * i - 4] = -cx1
        A[2 * i - 2, 2 * i - 3] = 3 * cx1 + cx2 + 2 * cx3
        A[2 * i - 2, 2 * i - 2] = -3 * cx1 - 2 * cx2 - 2 * cx3 - 3 * cx4
        A[2 * i - 2, 2 * i - 1] = cx1 + cx2
        A[2 * i - 2, 3 * i - 3] = -cx2 - cx3
        A[2 * i - 2, 3 * i - 2] = 2 * cx2 + cx3 + 3 * cx4
        A[2 * i - 2, 3 * i - 1] = -cx2
        A[2 * i - 2, 4 * i - 2] = -cx4

        p[2 * i - 1, 0] = (0.5 * load_yT + 0.5 * load_yR) * density ** 3  # sig_y = 0.5*sig_y_load + 0.5*tau_xy_load
        A[2 * i - 1, i - 3] = -cy3
        A[2 * i - 1, i - 2] = cy3 + cy4
        A[2 * i - 1, 2 * i - 4] = -cy1
        A[2 * i - 1, 2 * i - 3] = 3 * cy1 + cy2 + 2 * cy3
        A[2 * i - 1, 2 * i - 2] = -3 * cy1 - 2 * cy2 - 2 * cy3 - 3 * cy4
        A[2 * i - 1, 2 * i - 1] = cy1 + cy2
        A[2 * i - 1, 3 * i - 3] = -cy2 - cy3
        A[2 * i - 1, 3 * i - 2] = 2 * cy2 + cy3 + 3 * cy4
        A[2 * i - 1, 3 * i - 1] = -cy2
        A[2 * i - 1, 4 * i - 2] = -cy4

    else:
        pass  # it mean that for this node displacement boundaries will be applied

    if supports["bottom"] == 0 and supports["left"] == 0:  # 3 equations for corner point

        p[(j - 2) * i, 0] = 0
        A[(j - 2) * i, (j - 2) * i] = 1
        A[(j - 2) * i, (j - 1) * i + 1] = -1

        p[(j - 2) * i + 1, 0] = -(0.5 * load_xL + 0.5 * load_xB) * density ** 3
        A[(j - 2) * i + 1, (j - 4) * i + 1] = cx4
        A[(j - 2) * i + 1, (j - 3) * i] = cx2
        A[(j - 2) * i + 1, (j - 3) * i + 1] = -2 * cx2 - cx3 - 3 * cx4
        A[(j - 2) * i + 1, (j - 3) * i + 2] = cx2 + cx3
        A[(j - 2) * i + 1, (j - 2) * i] = -cx1 - cx2
        A[(j - 2) * i + 1, (j - 2) * i + 1] = 3 * cx1 + 2 * cx2 + 2 * cx3 + 3 * cx4
        A[(j - 2) * i + 1, (j - 2) * i + 2] = -3 * cx1 - cx2 - 2 * cx3
        A[(j - 2) * i + 1, (j - 2) * i + 3] = cx1
        A[(j - 2) * i + 1, (j - 1) * i + 1] = -cx3 - cx4
        A[(j - 2) * i + 1, (j - 1) * i + 2] = cx3

        p[(j - 1) * i + 1, 0] = -(0.5 * load_yL + 0.5 * load_yB) * density ** 3
        A[(j - 1) * i + 1, (j - 4) * i + 1] = cy4
        A[(j - 1) * i + 1, (j - 3) * i] = cy2
        A[(j - 1) * i + 1, (j - 3) * i + 1] = -2 * cy2 - cy3 - 3 * cy4
        A[(j - 1) * i + 1, (j - 3) * i + 2] = cy2 + cy3
        A[(j - 1) * i + 1, (j - 2) * i] = -cy1 - cy2
        A[(j - 1) * i + 1, (j - 2) * i + 1] = 3 * cy1 + 2 * cy2 + 2 * cy3 + 3 * cy4
        A[(j - 1) * i + 1, (j - 2) * i + 2] = -3 * cy1 - cy2 - 2 * cy3
        A[(j - 1) * i + 1, (j - 2) * i + 3] = cy1
        A[(j - 1) * i + 1, (j - 1) * i + 1] = -cy3 - cy4
        A[(j - 1) * i + 1, (j - 1) * i + 2] = cy3

    else:
        pass  # it mean that for this node displacement boundaries will be applied

    if supports["bottom"] == 0 and supports["right"] == 0:  # 3 equations for corner point

        p[(j - 2) * i + i - 1, 0] = 0
        A[(j - 2) * i + i - 1, (j - 2) * i + i - 1] = 1
        A[(j - 2) * i + i - 1, (j - 1) * i + i - 2] = -1

        p[(j - 2) * i + i - 2, 0] = (0.5 * load_xB + 0.5 * load_xR) * density ** 3
        A[(j - 2) * i + i - 2, (j - 4) * i + i - 2] = cx4
        A[(j - 2) * i + i - 2, (j - 3) * i + i - 3] = cx2 - cx3
        A[(j - 2) * i + i - 2, (j - 3) * i + i - 2] = -2 * cx2 + cx3 - 3 * cx4
        A[(j - 2) * i + i - 2, (j - 3) * i + i - 1] = cx2
        A[(j - 2) * i + i - 2, (j - 2) * i + i - 4] = -cx1
        A[(j - 2) * i + i - 2, (j - 2) * i + i - 3] = 3 * cx1 - cx2 + 2 * cx3
        A[(j - 2) * i + i - 2, (j - 2) * i + i - 2] = -3 * cx1 + 2 * cx2 - 2 * cx3 + 3 * cx4
        A[(j - 2) * i + i - 2, (j - 2) * i + i - 1] = cx1 - cx2
        A[(j - 2) * i + i - 2, (j - 1) * i + i - 3] = -cx3
        A[(j - 2) * i + i - 2, (j - 1) * i + i - 2] = cx3 - cx4

        p[(j - 1) * i + i - 2, 0] = -(0.5 * load_yB + 0.5 * load_yR) * density ** 3
        A[(j - 1) * i + i - 2, (j - 4) * i + i - 2] = cy4
        A[(j - 1) * i + i - 2, (j - 3) * i + i - 3] = cy2 - cy3
        A[(j - 1) * i + i - 2, (j - 3) * i + i - 2] = -2 * cy2 + cy3 - 3 * cy4
        A[(j - 1) * i + i - 2, (j - 3) * i + i - 1] = cy2
        A[(j - 1) * i + i - 2, (j - 2) * i + i - 4] = -cy1
        A[(j - 1) * i + i - 2, (j - 2) * i + i - 3] = 3 * cy1 - cy2 + 2 * cy3
        A[(j - 1) * i + i - 2, (j - 2) * i + i - 2] = -3 * cy1 + 2 * cy2 - 2 * cy3 + 3 * cy4
        A[(j - 1) * i + i - 2, (j - 2) * i + i - 1] = cy1 - cy2
        A[(j - 1) * i + i - 2, (j - 1) * i + i - 3] = -cy3
        A[(j - 1) * i + i - 2, (j - 1) * i + i - 2] = cy3 - cy4

    else:
        pass  # it mean that for this node displacement boundaries will be applied

    """ 6. Setting equations for edge points (B) for displacement boundary conditions """

    def edge_nodes_displacement(_real_node, _fictitious_node,  n1, n2, n3, n4, n5, n6, n7, n8, n9,
                                _A=A, _p=p, _i=i, _j=j, _v=v, _density=density,
                                _a1=a1, _a2=a2, _a3=a3, _a4=a4, _a5=a5, _a6=a6):
        # 2 equations for edge points

        _p[_real_node, 0] = 0 * _density**2  # equation for u(i,j)
        _A[_real_node, n1] = -_a2/4
        _A[_real_node, n2] = _a3
        _A[_real_node, n3] = _a2/4
        _A[_real_node, n4] = _a1
        _A[_real_node, n5] = -2*_a1 - 2*_a3
        _A[_real_node, n6] = _a1
        _A[_real_node, n7] = _a2/4
        _A[_real_node, n8] = _a3
        _A[_real_node, n9] = -_a2/4

        _p[_fictitious_node, 0] = 0 * _density ** 2  # equation for v(i,j)
        _A[_fictitious_node, n1] = -_a5 / 4
        _A[_fictitious_node, n2] = _a6
        _A[_fictitious_node, n3] = _a5 / 4
        _A[_fictitious_node, n4] = _a4
        _A[_fictitious_node, n5] = -2 * _a4 - 2 * _a6
        _A[_fictitious_node, n6] = _a4
        _A[_fictitious_node, n7] = _a5 / 4
        _A[_fictitious_node, n8] = _a6
        _A[_fictitious_node, n9] = -_a5 / 4

        return [_A, _p]

    if supports["top"] in [1, 2]:
        for m in range(2, i - 2, 1):    # top
            [A, p] = edge_nodes_displacement(i + m, m, m - 1, m, m + 1, i + m - 1, i + m,
                                             i + m + 1, 2 * i + m - 1, 2 * i + m, 2 * i + m + 1)
    else:
        pass     # it mean that for this node static boundaries will be applied

    if supports["left"] in [1, 2]:
        for m in range(2 * i, (j - 2) * i, i):  # left
            [A, p] = edge_nodes_displacement(m + 1, m, -i + m, -i + m + 1, -i + m + 2, m,
                                             m + 1, m + 2, i + m, i + m + 1, i + m + 2)
    else:
        pass     # it mean that for this node static boundaries will be applied

    if supports["bottom"] in [1, 2]:
        for m in range((j - 1) * i + 2, (j - 1) * i + i - 2, 1):  # bottom
            [A, p] = edge_nodes_displacement(-i + m, m, -2 * i + m - 1, -2*i + m, -2 * i + m + 1,
                                             -i + m - 1, -i + m, -i + m + 1, m - 1, m, m + 1)
    else:
        pass     # it mean that for this node static boundaries will be applied

    if supports["right"] in [1, 2]:
        for m in range(2 * i + i - 1, (j - 2) * i + i - 1, i):  # right
            [A, p] = edge_nodes_displacement(m, m - 1, i + m - 2, i + m - 1, i + m, m - 2,
                                             m - 1, m, -i + m - 2, -i + m - 1, -i + m)
    else:
        pass     # it mean that for this node static boundaries will be applied

    """ 7. Setting equations for edge points (B) for statical boundary conditions """

        # 2 equations for edge points

    if supports["top"] == 0:
        for m in range(2, i - 2, 1):    # top
            real_node = i + m
            fictitious_node = m

            p[real_node, 0] = load_xT * 2 * density ** 3  # equation for u(i,j)
            A[real_node, m - 1] = ct2 - ct3
            A[real_node, m] = -2 * ct2 + 2 * ct4
            A[real_node, m + 1] = ct2 + ct3
            A[real_node, m + i - 1] = 2 * ct1 + 2 * ct3
            A[real_node, m + i] = -6 * ct4
            A[real_node, m + i + 1] = -2 * ct1 - 2 * ct3
            A[real_node, m + 2 * i - 1] = -ct2 - ct3
            A[real_node, m + 2 * i] = 2 * ct2 + 6 * ct4
            A[real_node, m + 2 * i + 1] = -ct2 + ct3
            A[real_node, m + i - 2] = -ct1
            A[real_node, m + i + 2] = ct1
            A[real_node, m + 3 * i] = -2 * ct4

            p[fictitious_node, 0] = load_yT * 2 * density ** 3  # equation for v(i,j)
            A[fictitious_node, m - 1] = cy2 - cy3
            A[fictitious_node, m] = -2 * cy2 + 2 * cy4
            A[fictitious_node, m + 1] = cy2 + cy3
            A[fictitious_node, m + i - 1] = 2 * cy1 + 2 * cy3
            A[fictitious_node, m + i] = -6 * cy4
            A[fictitious_node, m + i + 1] = -2 * cy1 - 2 * cy3
            A[fictitious_node, m + 2 * i - 1] = -cy2 - cy3
            A[fictitious_node, m + 2 * i] = 2 * cy2 + 6 * cy4
            A[fictitious_node, m + 2 * i + 1] = -cy2 + cy3
            A[fictitious_node, m + i - 2] = -cy1
            A[fictitious_node, m + i + 2] = cy1
            A[fictitious_node, m + 3 * i] = -2 * cy4
    else:
        pass     # it mean that for this node displacement boundaries will be applied

    if supports["left"] == 0:
        for m in range(2 * i, (j - 2) * i, i):  # left
            real_node = m + 1
            fictitious_node = m

            p[real_node, 0] = load_xL * 2 * density ** 3  # equation for u(i,j)
            A[real_node, m - i] = cx2 - cx3
            A[real_node, m - i + 1] = -2 * cx2 - 2 * cx4
            A[real_node, m - i + 2] = cx2 + cx3
            A[real_node, m] = -2 * cx1 + 2 * cx3
            A[real_node, m + 1] = 6 * cx4
            A[real_node, m + 2] = -6 * cx1 - 2 * cx3
            A[real_node, m + i] = -cx2 - cx3
            A[real_node, m + i + 1] = 2 * cx2 + 2 * cx4
            A[real_node, m + i + 2] = -cx2 + cx3
            A[real_node, m - 2 * i + 1] = cx4
            A[real_node, m + 2 * i + 1] = -cx4
            A[real_node, m + 3] = 2 * cx1

            p[fictitious_node, 0] = load_yL * 2 * density ** 3  # equation for v(i,j)
            A[fictitious_node, m - i] = ct2 - ct3
            A[fictitious_node, m - i + 1] = -2 * ct2 - 2 * ct4
            A[fictitious_node, m - i + 2] = ct2 + ct3
            A[fictitious_node, m] = -2 * ct1 + 2 * ct3
            A[fictitious_node, m + 1] = 6 * ct4
            A[fictitious_node, m + 2] = -6 * ct1 - 2 * ct3
            A[fictitious_node, m + i] = -ct2 - ct3
            A[fictitious_node, m + i + 1] = 2 * ct2 + 2 * ct4
            A[fictitious_node, m + i + 2] = -ct2 + ct3
            A[fictitious_node, m - 2 * i + 1] = ct4
            A[fictitious_node, m + 2 * i + 1] = -ct4
            A[fictitious_node, m + 3] = 2 * ct1
    else:
        pass     # it mean that for this node displacement boundaries will be applied

    if supports["bottom"] == 0:
        for m in range((j - 1) * i + 2, (j - 1) * i + i - 2, 1):  # bottom
            real_node = -i + m
            fictitious_node = m

            p[real_node, 0] = load_xB * 2 * density ** 3  # equation for u(i,j)
            A[real_node, m - 2 * i - 1] = ct2 - ct3
            A[real_node, m - 2 * i] = -2 * ct2 - 6 * ct4
            A[real_node, m - 2 * i + 1] = ct2 + ct3
            A[real_node, m - i - 1] = 2 * ct1 + 2 * ct3
            A[real_node, m - i] = 6 * ct4
            A[real_node, m - i + 1] = -2 * ct1 - 2 * ct3
            A[real_node, m - 1] = -ct2 - ct3
            A[real_node, m] = 2 * ct2 - 2 * ct4
            A[real_node, m + 1] = -ct2 + ct3
            A[real_node, m - i - 2] = -ct1
            A[real_node, m - i + 2] = ct1
            A[real_node, m - 3 * i] = 2 * ct4

            p[fictitious_node, 0] = load_yB * 2 * density ** 3  # equation for v(i,j)
            A[fictitious_node, m - 2 * i - 1] = cy2 - cy3
            A[fictitious_node, m - 2 * i] = -2 * cy2 - 6 * cy4
            A[fictitious_node, m - 2 * i + 1] = cy2 + cy3
            A[fictitious_node, m - i - 1] = 2 * cy1 + 2 * cy3
            A[fictitious_node, m - i] = 6 * cy4
            A[fictitious_node, m - i + 1] = -2 * cy1 - 2 * cy3
            A[fictitious_node, m - 1] = -cy2 - cy3
            A[fictitious_node, m] = 2 * cy2 - 2 * cy4
            A[fictitious_node, m + 1] = -cy2 + cy3
            A[fictitious_node, m - i - 2] = -cy1
            A[fictitious_node, m - i + 2] = cy1
            A[fictitious_node, m - 3 * i] = 2 * cy4
    else:
        pass     # it mean that for this node displacement boundaries will be applied

    if supports["right"] == 0:
        for m in range(2 * i + i - 1, (j - 2) * i + i - 1, i):  # right
            real_node = m - 1
            fictitious_node = m

            p[real_node, 0] = load_xR * 2 * density ** 3  # equation for u(i,j)
            A[real_node, m - i - 2] = cx2 - cx3
            A[real_node, m - i - 1] = -2 * cx2 + -2 * cx4
            A[real_node, m - i] = cx2 + cx3
            A[real_node, m - 2] = 6 * cx1 + 2 * cx3
            A[real_node, m - 1] = -6 * cx1
            A[real_node, m] = 2 * cx1 - 2 * cx3
            A[real_node, m + i - 2] = -cx2 - cx3
            A[real_node, m + i - 1] = 2 * cx2 + 2 * cx4
            A[real_node, m + i] = -cx2 + cx3
            A[real_node, m - 2 * i - 1] = cx4
            A[real_node, m + 2 * i - 1] = -cx4
            A[real_node, m - 3] = -2 * cx1

            p[fictitious_node, 0] = load_yR * 2 * density ** 3  # equation for v(i,j)
            A[fictitious_node, m - i - 2] = ct2 - ct3
            A[fictitious_node, m - i - 1] = -2 * ct2 + -2 * ct4
            A[fictitious_node, m - i] = ct2 + ct3
            A[fictitious_node, m - 2] = 6 * ct1 + 2 * ct3
            A[fictitious_node, m - 1] = -6 * ct1
            A[fictitious_node, m] = 2 * ct1 - 2 * ct3
            A[fictitious_node, m + i - 2] = -ct2 - ct3
            A[fictitious_node, m + i - 1] = 2 * ct2 + 2 * ct4
            A[fictitious_node, m + i] = -ct2 + ct3
            A[fictitious_node, m - 2 * i - 1] = ct4
            A[fictitious_node, m + 2 * i - 1] = -ct4
            A[fictitious_node, m - 3] = -2 * ct1
    else:
        pass     # it mean that for this node displacement boundaries will be applied

    """ 8. Setting equations for mid points (C) """

    def mid_nodes(node, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13,
                  _A=A, _p=p, _density=density,
                  _beta0=beta0, _beta1=beta1, _beta2=beta2, _beta3=beta3):

        _p[node, 0] = _beta0 * 0 * _density**4  # there is no external load applied to mid nodes
        _A[node, n1] = _beta3
        _A[node, n2] = _beta2
        _A[node, n3] = -4 * _beta3 - 2 * _beta2
        _A[node, n4] = _beta2
        _A[node, n5] = _beta1
        _A[node, n6] = -4 * _beta1 - 2 * _beta2
        _A[node, n7] = 6 * _beta1 + 4 * _beta2 + 6 * _beta3
        _A[node, n8] = -4 * _beta1 - 2 * _beta2
        _A[node, n9] = _beta1
        _A[node, n10] = _beta2
        _A[node, n11] = -4 * _beta3 - 2 * _beta2
        _A[node, n12] = _beta2
        _A[node, n13] = _beta3
        return [_A, _p]

    for vm in range(2, j - 2, 1):
        for m in range(2, i - 2, 1):
            [A, p] = mid_nodes(vm * i + m, (vm - 2) * i + m, (vm - 1) * i + m - 1, (vm - 1) * i + m,
                               (vm - 1) * i + m + 1, vm * i + m - 2, vm * i + m - 1, vm * i + m, vm * i + m + 1,
                               vm * i + m + 2, (vm + 1) * i + m - 1, (vm + 1) * i + m, (vm + 1) * i + m + 1,
                               (vm + 2) * i + m)

    """ 9. Calculation of Af = p equation """

    f_solved = np.linalg.solve(A, p)
    F = np.zeros((i, j))
    s = 0
    for vm in range(j):
        for m in range(i):
            F[m, vm] = round(f_solved[s, 0], 14)
            s += 1

    """ 10. Calculation of u, v, sigma x, sigma y and tau xy and membrane forces from F matrix"""

    u = np.zeros((i-2, j-2))
    for vm in range(j-2):
        for m in range(i-2):
            u[m, vm] = -a2 / 4 * F[m, vm] + a3 * F[m + 1, vm] + a2 / 4 * F[m + 2, vm] \
                       + a1 * F[m, vm + 1] + (-2 * a1 - 2 * a3) * F[m + 1, vm + 1] + a1 * F[m + 2, vm + 1] \
                       + a2 / 4 * F[m, vm + 2] + a3 * F[m + 1, vm + 2] - a2 / 4 * F[m + 2, vm + 2]
    # values at corners has to be changed due to the fact that corner points does not belong to F function domain
    u[0, 0] = (a1 * F[0, 1] + a3 * F[1, 0] + (-2 * a1 - a2 - 2 * a3) * F[1, 1] + (a1 + a2) * F[2, 1]
               + (a2 + a3) * F[1, 2] - a2 * F[2, 2]) * 1 / (density ** 2)
    u[i - 3, 0] = (a1 * F[i-1, 1] + a3 * F[i-2, 0] + (-2 * a1 + a2 - 2 * a3) * F[i-2, 1] + (a1 - a2) * F[i-3, 1]
                   + (-a2 + a3) * F[i-2, 2] + a2 * F[i-3, 2]) * 1 / (density ** 2)
    u[0, j - 3] = (a1 * F[0, j-2] + a3 * F[1, j-1] + (-2 * a1 + a2 - 2 * a3) * F[1, j-2] + (a1 - a2) * F[2, j-2]
                   + (-a2 + a3) * F[1, j-3] + a2 * F[2, j-3]) * 1 / (density ** 2)
    u[i - 3, j - 3] = (a1 * F[i-1, j-2] + a3 * F[i-2, j-1] + (-2 * a1 - a2 - 2 * a3) * F[i-2, j-2]
                       + (a1 + a2) * F[i-3, j-2] + (a2 + a3) * F[i-2, j-3] - a2 * F[i-3, j-3]) * 1 / (density ** 2)

    v = np.zeros((i-2, j-2))
    for vm in range(j-2):
        for m in range(i-2):
            v[m, vm] = -a5 / 4 * F[m, vm] + a6 * F[m + 1, vm] + a5 / 4 * F[m + 2, vm] \
                       + a4 * F[m, vm + 1] + (-2 * a4 - 2 * a6) * F[m + 1, vm + 1] + a4 * F[m + 2, vm + 1] \
                       + a5 / 4 * F[m, vm + 2] + a6 * F[m + 1, vm + 2] - a5 / 4 * F[m + 2, vm + 2]
    # values at corners has to be changed due to the fact that corner points does not belong to F function domain
    v[0, 0] = (a4 * F[0, 1] + a6 * F[1, 0] + (-2 * a4 - a5 - 2 * a6) * F[1, 1] + (a4 + a5) * F[2, 1]
               + (a5 + a6) * F[1, 2] - a5 * F[2, 2]) * 1 / (density ** 2)
    v[i - 3, 0] = (a4 * F[i-1, 1] + a6 * F[i-2, 0] + (-2 * a4 + a5 - 2 * a6) * F[i-2, 1] + (a4 - a5) * F[i-3, 1]
                   + (-a5 + a6) * F[i-2, 2] + a5 * F[i-3, 2]) * 1 / (density ** 2)
    v[0, j - 3] = (a4 * F[0, j-2] + a6 * F[1, j-1] + (-2 * a4 + a5 - 2 * a6) * F[1, j-2] + (a4 - a5) * F[2, j-2]
                   + (-a5 + a6) * F[1, j-3] + a5 * F[2, j-3]) * 1 / (density ** 2)
    v[i - 3, j - 3] = (a4 * F[i-1, j-2] + a6 * F[i-2, j-1] + (-2 * a4 - a5 - 2 * a6) * F[i-2, j-2]
                       + (a4 + a5) * F[i-3, j-2] + (a5 + a6) * F[i-2, j-3] - a5 * F[i-3, j-3]) * 1 / (density ** 2)

    sigma_x = np.zeros((i - 2, j - 2))
    for vm in range(j-3)[1:]:
        for m in range(i-3)[1:]:
            sigma_x[m, vm] = cx4 * F[m + 1, vm - 1] + (cx2 - cx3) * F[m, vm] + (-2 * cx2 - 2 * cx4) * F[m + 1, vm] \
                             + (cx2 + cx3) * F[m + 2, vm] - cx1 * F[m - 1, vm + 1] + (2 * cx1 + 2 * cx3) * F[m, vm + 1]\
                             + 0 * F[m + 1, vm + 1] + (-2 * cx1 - 2 * cx3) * F[m + 2, vm + 1] + cx1 * F[m + 3, vm + 1] \
                             + (-cx2 - cx3) * F[m, vm + 2] + (2 * cx2 + 2 * cx4) * F[m + 1, vm + 2] \
                             + (-cx2 + cx3) * F[m + 2, vm + 2] - cx4 * F[m + 1, vm + 3]
    # values at corners and edges has to be changed
    # TO BE CONTINUED

    sigma_y = np.zeros((i - 2, j - 2))
    for vm in range(j-3)[1:]:
        for m in range(i-3)[1:]:
            sigma_y[m, vm] = cy4 * F[m + 1, vm - 1] + (cy1 - cy3) * F[m, vm] + (-2 * cy2 - 2 * cy4) * F[m + 1, vm] \
                             + (cy2 + cy3) * F[m + 2, vm] - cy1 * F[m - 1, vm + 1] + (2 * cy1 + 2 * cy3) * F[m, vm + 1]\
                             + 0 * F[m + 1, vm + 1] + (-2 * cy1 - 2 * cy3) * F[m + 2, vm + 1] + cy1 * F[m + 3, vm + 1] \
                             + (-cy2 - cy3) * F[m, vm + 2] + (2 * cy2 + 2 * cy4) * F[m + 1, vm + 2] \
                             + (-cy2 + cy3) * F[m + 2, vm + 2] - cy4 * F[m + 1, vm + 3]
    # values at corners and edges has to be changed
    # TO BE CONTINUED

    tau_xy = np.zeros((i - 2, j - 2))
    for vm in range(j-3)[1:]:
        for m in range(i-3)[1:]:
            tau_xy[m, vm] = ct4 * F[m + 1, vm - 1] + (ct2 - ct3) * F[m, vm] + (-2 * ct2 - 2 * ct4) * F[m + 1, vm] \
                             + (ct2 + ct3) * F[m + 2, vm] - ct1 * F[m - 1, vm + 1] + (2 * ct1 + 2 * ct3) * F[m, vm + 1]\
                             + 0 * F[m + 1, vm + 1] + (-2 * ct1 - 2 * ct3) * F[m + 2, vm + 1] + ct1 * F[m + 3, vm + 1] \
                             + (-ct2 - ct3) * F[m, vm + 2] + (2 * ct2 + 2 * ct4) * F[m + 1, vm + 2] \
                             + (-ct2 + ct3) * F[m + 2, vm + 2] - ct4 * F[m + 1, vm + 3]
    # values at corners and edges has to be changed
    # TO BE CONTINUED

    nxx = sigma_x * thickness
    nyy = sigma_y * thickness
    nxy = tau_xy * thickness

    return [u.T, v.T, sigma_x.T, sigma_y.T, tau_xy.T, nxx.T, nyy.T, nxy.T]


def compute_shield(displacements, E, loads, supports, density, v, thickness):
    """Function combining matrices for vertical and horizontal load cases"""

    given_displacements = displacements
    given_E = E
    given_loads = loads
    given_supports = supports
    given_density = density
    given_v = v
    given_thickness = thickness
    vertical_matrices = compute_shield_one_direction(given_displacements, given_E, given_loads, given_supports,
                                                     given_density, given_v, given_thickness, "vertical")
    horizontal_matrices = compute_shield_one_direction(given_displacements, given_E, given_loads, given_supports,
                                                       given_density, given_v, given_thickness, "horizontal")
    resulting_matrices = [0, 0, 0, 0, 0, 0, 0, 0]
    for el in range(len(resulting_matrices)):
        resulting_matrices[el] = vertical_matrices[el] + horizontal_matrices[el]
    return resulting_matrices


if __name__ == '__main__':

    class TestMeshClass(object):
        def __init__(self):
            self.data = [np.zeros((25, 25)), np.zeros((25, 25)), None]


    test_class = TestMeshClass()
    test_mesh = test_class.data
    test_modulus_of_elasticity = 0.2
    test_thickness = 0.15
    test_load = {
        "x_direction": {
            "bottom": 0.0,
            "left": 0.0,
            "right": 0.0,
            "top": 0.0
        },
        "y_direction": {
            "bottom": 0.0,
            "left": 0.0,
            "right": 0.0,
            "top": 100.0
        }}
    test_supports = {           # 0 - free end  1 - hinged  2 - fixed
                    "bottom": 2,
                    "left": 0,
                    "right": 0,
                    "top": 0
                    }
    test_density = 1
    test_poisson_ratio = 0.3
    start = datetime.datetime.now()
    g = compute_shield(test_mesh, test_modulus_of_elasticity, test_load, test_supports, test_density,
                       test_poisson_ratio, test_thickness)
    duration = datetime.datetime.now() - start   # time of calculations
    print(duration)
    fig, ax = plt.subplots(1, 2)
    cmap = cm.get_cmap(name='jet', lut=40)
    norm = matplotlib.colors.Normalize()
    mappable = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    mappable.set_array(g[1])
    mappable.autoscale()
    matplotlib.pyplot.colorbar(mappable, ax[1])
    ax[0].imshow(g[1], extent=(0, 25, 0, 25), interpolation='hermite', cmap=cmap)
    mappable.changed()
    plt.show()
