#!/usr/bin/env python3
import numpy as n
import scipy.constants as c
import matplotlib.pyplot as plt

x=n.linspace(-2.5,1.5,num=2000,dtype=n.float32)
y=n.linspace(-2,2,num=2000,dtype=n.float32)
cx,cy=n.meshgrid(x,y)
c=cx+1j*cy

# figure out what is the datatype of variable c
# to make sure it's complex64
print(c.dtype)

z=n.zeros(c.shape,dtype=n.complex64)

for iteration in range(12):
    z=z**2+c
z[n.isnan(z)]=0.0
z[n.isinf(z)]=0.0

plt.imshow(n.angle(z),extent=[-2.5,1.5,-2,2],cmap="hsv")
plt.colorbar()
plt.xlabel("$\mathrm{Re}\{c\}$")
plt.ylabel("$\mathrm{Im}\{c\}$")
plt.show()
