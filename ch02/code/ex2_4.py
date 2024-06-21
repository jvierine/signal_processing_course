# Import some libraries.
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as c

# Partition the interval (-2.5, 1.5) or (-2, 2) into 2000 numbers.
# Separated by the same distance, store these numbers as 32-bit floating point numbers.
x = np.linspace(-2.5, 1.5, num=2000, dtype=np.float32)
y = np.linspace(-2, 2, num=2000, dtype=np.float32)

# Create a grid using x and y as the x- and y-axis.
cx, cy = np.meshgrid(x, y)
# ^cx is a copy of x stored as a matrix with y number of rows,
# same is true for cy, but opposite, there is a copy of y and there is x number of rows.

# Create a complex plane grid using cx and cy.
c = cx + 1j*cy

# Figure out what is the datatype of variable c
# to make sure it is complex64.
print(c.dtype)

# Create a matrix of zeros having the same dimension as c.
z = np.zeros(c.shape, dtype=np.complex64)

# Compute the sequence z_{n+1} = z_{n}^2 + c for n = 0,...,11.
for _ in range(12):
    z = z**2 + c

# Set infinities and NaN (not a number) to 0.0.
z[np.isnan(z)] = 0.0
z[np.isinf(z)] = 0.0

# Plot the result using a color gradient.
plt.imshow(np.angle(z), extent=[-2.5, 1.5, -2, 2], cmap="hsv")
plt.colorbar()
plt.xlabel(r"$\mathrm{Re}\{c\}$")
plt.ylabel(r"$\mathrm{Im}\{c\}$")
plt.show()