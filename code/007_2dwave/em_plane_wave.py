#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt
import scipy.constants as c

f = 2.4e9
wavelength = c.c/f

t=n.linspace(0,2/f,num=1000)
x=n.linspace(0,2*wavelength,num=1000)

ct,cx=n.meshgrid(t,x)

plt.pcolormesh(ct,cx,n.real(n.exp(-1j*2.0*n.pi*cx/wavelength)*n.exp(1j*2.0*n.pi*f*ct)),vmin=-1,vmax=1)
cb=plt.colorbar()
cb.set_label("Electric field (V/m)")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.tight_layout()
plt.savefig("em_plane_wave.png")
plt.show()
