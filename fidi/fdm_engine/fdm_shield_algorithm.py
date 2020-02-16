"""This part of program is responsible for applying appropriate boundary conditions and computing values of displacement
    in each node of regular mesh using finite differences method for shield objects"""

import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors


def compute_shield(displacements, Ds, loads, supports, density, v):
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

            f vector is flattened version of F matrix, for i,j shape matrix :
            f[0] element is equal to F[0, 0],
            f[0*i + i-1] is equal to F[0, i-1]  
            f[1 * i] is equal to F[1, 0]
            f[(j-1)*i] is equal to F[j-1, 0]
            f[(j-1)*i + i-1] is equal  to F[j-1, i-1]

            while assembling A matrix in A[a,b] a is a number of node in w vector for which equation is formed and b is
            a number of node in w vector for which coefficient is applied according to FDM scheme.
    """

    #    A - assembled matrix of FDM scheme equations, f - vector of Airy function F values, p - vector of load

    A = np.zeros((n, n))
    p = np.ones((n, 1))

    """ 3. Calculation of all coefficients """

    """ 4. Setting equations for corner points (A) for displacement boundary conditions """

    """ 5. Setting equations for corner points (A) for statical boundary conditions """

    """ 6. Setting equations for edge points (B) for displacement boundary conditions """

    """ 7. Setting equations for edge points (B) for statical boundary conditions """

    """ 8. Setting equations for mid points (C) """

    """ 9. Calculation of Af = p equation """

    """ 10. Calculation of u and v from F matrix"""

    #    for load in X direction:
    #    for load in Y direction:

    """ 11. Overall displacement calculation from superposition of displacements from X and Y loaded cases"""
