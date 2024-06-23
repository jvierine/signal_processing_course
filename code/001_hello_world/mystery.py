#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as c

x = np.linspace(-2.5, 1.5, num=2000, dtype=np.float32)
y = np.linspace(-2, 2, num=2000, dtype=np.float32)
cx, cy = np.meshgrid(x, y)
c = cx + 1j*cy

# Figure out what is the datatype of variable c
# to make sure it's complex64.
print(c.dtype)

z = np.zeros(c.shape, dtype=np.complex64)

for _ in range(12):
    z = z**2 + c

z[np.isnan(z)] = 0.0
z[np.isinf(z)] = 0.0

plt.imshow(np.angle(z), extent=[-2.5, 1.5, -2, 2], cmap="hsv")
plt.colorbar()
plt.xlabel(r"$\mathrm{Re}\{c\}$")
plt.ylabel(r"$\mathrm{Im}\{c\}$")
plt.show()
