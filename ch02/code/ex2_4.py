# import some libaries (called modules in Python)
import numpy as n
import scipy.constants as c
import matplotlib.pyplot as plt

# partition the interval (-2.5,1.5) or (-2,2) into 2000 numbers
# separated by the same distance, store these numbers as 32-bit floating point numbers
x = n.linspace(-2.5, 1.5, num=2000, dtype=n.float32)
y = n.linspace(-2, 2, num=2000, dtype=n.float32)

# create a grid using x and y as the x- and y-axis
cx, cy = n.meshgrid(x,y)
# ^cx is a copy of x stored as a matrix with y number of rows
# same is true for cy, but opposite, there is a copy of y and there is x number of rows

# create a complex plane grid using cx and cy
c = cx + 1j*cy

# figure out what is the datatype of variable c
# to make sure it is complex64
print(c.dtype)

# create a matrix of zeros having the same dimension as c
z = n.zeros(c.shape,dtype=n.complex64)

# compute the sequence z_{n+1} = z_{n}^2 + c for n = 0,...,11
for iteration in range(12):
    z = z**2 + c

# set infinities and nan (not a number) to 0.0
z[n.isnan(z)] = 0.0
z[n.isinf(z)] = 0.0

# plot the result using a color gradient
plt.imshow(n.angle(z),extent = [-2.5,1.5,-2,2],cmap="hsv")
plt.colorbar()
plt.xlabel("$\mathrm{Re}\{c\}$")
plt.ylabel("$\mathrm{Im}\{c\}$")
plt.show()