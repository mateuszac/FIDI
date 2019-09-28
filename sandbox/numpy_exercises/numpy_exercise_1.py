"""Find coordinates of a node in rectangular mesh (Nx x Ny), for which the value of scalar field given
by function f(x) = x^2 - 2y is maximal"""

import numpy as np

Nx = 5
Ny = 8
fun = lambda x, y: x**2 - 2*y

A = np.zeros((Nx, Ny))
for i in range(Nx):
    for j in range(Ny):
        A[i,j] = fun(i,j)

for i in range(Nx):
    for j in range(Ny):
        if A[i,j] == np.amax(A):
            b = i+1
            a = j+1 # +1 because python is counting from 0, not 1
            break
        else:
            continue

print("Maximal value of f is reached in point {}, {}".format(a, b))
print(A)