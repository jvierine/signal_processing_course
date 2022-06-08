#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt


P=0.5
T=2.0

sample_rate=1000.0
t=n.arange(int(sample_rate*T))/sample_rate

zn = n.zeros(len(t),dtype=n.float64)

N=21
zn[:] = P/T
for k in range(1,N):
    zn+=(2.0*n.sin(k*P*n.pi/T)/(n.pi*k))*n.cos(2.0*n.pi*k*t/T - k*P*n.pi/T)

square_wave=n.zeros(len(t),dtype=n.float64)
square_wave[(0<t)&(t<P)]=1.0

plt.figure(figsize=(0.8*6,0.8*4))
plt.plot(t,square_wave,label="Square wave",color="black")
plt.plot(t,zn,label="Fourier series approximation",color="blue")
plt.legend()
plt.xlabel("Time (t)")
plt.ylabel("s(t)")
plt.tight_layout()
plt.savefig("square_wave.png")
plt.show()
