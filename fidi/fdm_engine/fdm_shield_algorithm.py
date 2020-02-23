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

    xB = loads["x_direction"]["bottom"]
    xT = loads["x_direction"]["top"]
    xL = loads["x_direction"]["left"]
    xR = loads["x_direction"]["right"]
    yB = loads["y_direction"]["bottom"]
    yT = loads["y_direction"]["top"]
    yL = loads["y_direction"]["left"]
    yR = loads["y_direction"]["right"]

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
    A[0, 0] = 1 # after A*f=P it gives result 1*f(top-left) = 0
    p[i - 1, 0] = 0
    A[i - 1, i - 1] = 1 # after A*f=P it gives result 1*f(top-right) = 0
    p[(j - 1) * i, 0] = 0
    A[(j - 1) * i, (j - 1) * i] = 1 # after A*f=P it gives result 1*f(bottom-left) = 0
    p[(j - 1) * i + i - 1, 0] = 0
    A[(j - 1) * i + i - 1, (j - 1) * i + i - 1] = 1 # after A*f=P it gives result 1*f(bottom-right) = 0

    ### first for vertical direction of load ###

    a1 = alpha1v
    a2 = alpha2v
    a3 = alpha3v
    a4 = alpha4v
    a5 = alpha5v
    a6 = alpha6v

    """ 4. Setting equations for corner points (A) for displacement boundary conditions """

        if supports["top"] in [1, 2] or supports["left"] in [1, 2]: # 3 equations for corner point

            p[1, 0] = 0
            A[1, 1] = 1
            A[1, i] = -1 # after A*f=P it gives result f1-f2 = 0, so f1 = f2 for 2 fictitious nodes

            p[i, 0] = 0 * density**2 # support or forced displacement value in vertical direction
            A[i, i] = a1
            A[i, 1] = a3
            A[i, i+1] = -2*a1 - a2 - 2*a3
            A[i, i+2] = a1 + a2
            A[i, 2*i+1] = a2 + a3
            A[i, 2*i+2] = -a2

            p[i, 0] = 0 * density ** 2  # support or forced displacement value in horizontal direction
            A[i, i] = a4
            A[i, 1] = a6
            A[i, i + 1] = -2 * a4 - a5 - 2 * a6
            A[i, i + 2] = a4 + a5
            A[i, 2 * i + 1] = a5 + a6
            A[i, 2 * i + 2] = -a5

        else:
            pass # it mean that for this node static boundaries will be applied



    """ 5. Setting equations for corner points (A) for statical boundary conditions """

    """ 6. Setting equations for edge points (B) for displacement boundary conditions """

    """ 7. Setting equations for edge points (B) for statical boundary conditions """

    """ 8. Setting equations for mid points (C) """

    """ 9. Calculation of Af = p equation """

    """ 10. Calculation of u and v from F matrix"""

    #    for load in X direction:
    #    for load in Y direction:

    """ 11. Overall displacement calculation from superposition of displacements from X and Y loaded cases"""
