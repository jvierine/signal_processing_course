#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as n

m=n.arange(41)

theta=2.0*n.pi/10.0

z=0.92*n.exp(1j*theta)
#plt.style.use('dark_background')

plt.plot(n.real(z**m),n.imag(z**m),"-",label="$0.9^n \mathrm{exp}\left(i \\frac{2\pi}{20}\\right)^n$",color="blue")
plt.scatter(n.real(z**m),n.imag(z**m),c=m,zorder=3,cmap="viridis",s=20)


z=1.1*n.exp(1j*theta)
#plt.plot(n.real(z**m),n.imag(z**m),"-",label="$1.1^n \mathrm{exp}\left(i \\frac{2\pi}{20}\\right)^n$",color="red")
#plt.scatter(n.real(z**m),n.imag(z**m),c=m,zorder=3,cmap="viridis",s=20)
cb=plt.colorbar()
cb.set_label("$n$")
plt.plot(n.cos(n.linspace(0,2*n.pi,num=1000)),n.sin(n.linspace(0,2*n.pi,num=1000)),color="grey",label="Unit circle $e^{i\\theta}$")
#plt.legend()
plt.xlabel("Real axis")
plt.ylabel("Imaginary axis")
plt.axes().set_aspect('equal')
plt.tight_layout()
plt.savefig("spiral.png")
plt.show()

