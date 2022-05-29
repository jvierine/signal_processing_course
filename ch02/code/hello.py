#!/usr/bin/env python3
import numpy as n
import scipy.constants as c
import matplotlib.pyplot as plt
# test some print statements
print("Hello World!")
print(n.pi)     # numpy version of pi
print(c.pi)     # scipy version of pi
# declare some variables
sample_rate = 44100.0             # 44100 samples per second
t = n.arange(100)/sample_rate     # sampling time array
csin = n.exp(1j*2.0*n.pi*440.0*t) # complex 440 Hz signal
# plot the complex 440Hz sinusoidal signal
plt.plot(t*1e3, csin.real,color="blue",
         label="$\mathrm{Re}\{z(t)\}$")
plt.plot(t*1e3, csin.imag,color="red",
         label="$\mathrm{Im}\{z(t)\}$")
plt.xlabel("Time (ms)")
plt.ylabel("$z(t)=e^{i\omega t}$")
plt.legend(); plt.tight_layout(); plt.grid()
plt.show()