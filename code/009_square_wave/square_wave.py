#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt


P=0.1
T=1.0

sample_rate=1000.0
t=n.arange(int(sample_rate*T))/sample_rate

zn = n.zeros(len(t),dtype=n.complex64)

N=101

ks=n.arange(-N,N+1)
cks=n.zeros(2*N+1,dtype=n.complex64)
ki=0
for k in range(-N,N+1):
    if k == 0:
        zn += P/T
        cks[ki]=P/T
    else:
        k2=float(k)
        ck=(1.0/(n.pi*k2))*(n.exp(-1j*(n.pi/T)*k2*P))*n.sin(n.pi*k2*P/T)
        cks[ki]=ck
        zn+= ck*n.exp(1j*(2.0*n.pi/T)*k2*t)
    ki+=1

# Plot the absolute values of the Fourier series coefficients
plt.plot(2.0*n.pi*ks/T,n.abs(cks))
plt.show()

# create a square wave signal
square_wave=n.zeros(len(t),dtype=n.float64)
square_wave[(0<t)&(t<P)]=1.0

plt.figure(figsize=(0.8*6,0.8*4))
plt.plot(t,square_wave,label="Square wave",color="black")
plt.plot(t,zn.real,label="Fourier series approximation (Real)",color="blue")
plt.plot(t,zn.imag,label="Fourier series approximation (Imag)",color="red")
plt.legend()
plt.xlabel("Time (t)")
plt.ylabel("s(t)")
plt.tight_layout()
plt.savefig("square_wave.png")
plt.show()
