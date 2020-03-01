"""This part of program is responsible for applying appropriate boundary conditions and computing values of displacement
    in each node of regular mesh using finite differences method for shield objects"""

import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors


def compute_shield(displacements, E, loads, supports, density, v):
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

    # first for vertical direction of load #

    a1 = alpha1v
    a2 = alpha2v
    a3 = alpha3v
    a4 = alpha4v
    a5 = alpha5v
    a6 = alpha6v

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

    """ 7. Setting equations for edge points (B) for statical boundary conditions """

    """ 8. Setting equations for mid points (C) """

    """ 9. Calculation of Af = p equation """

    """ 10. Calculation of u and v from F matrix"""

    #    for load in X direction:
    #    for load in Y direction:

    """ 11. Overall displacement calculation from superposition of displacements from X and Y loaded cases"""
