#!/usr/bin/env python3
import numpy as n
import scipy.constants as c
import matplotlib.pyplot as plt

print("Hello World!")
# test numpy and scipy
print(n.pi)
print(c.pi)

sample_rate = 44100.0 # 44100 samples per second
t = n.arange(100)/sample_rate 
csin = n.exp(1j*2.0*n.pi*440.0*t) # A 440 Hz signal
plt.plot(t*1e3, csin.real,color="blue",
         label="$\mathrm{Re}\{z(t)\}$")
plt.plot(t*1e3, csin.imag,color="red",
         label="$\mathrm{Im}\{z(t)\}$")
plt.xlabel("Time (ms)")
plt.ylabel("$z(t)=e^{i\omega t}$")
plt.legend()
plt.show()

