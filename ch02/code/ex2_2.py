import numpy as n
import scipy.constants as c
import matplotlib.pyplot as plt
import sys  # <-- you can remove this 

print("Hello World!")
# test numpy and scipy
print(n.pi)
print(c.pi)

sample_rate = 44100.0 # 44100 samples per second
t = n.arange(101)/sample_rate # <-- added 101 to obtain the full circle

csin = n.exp(1j*2.0*n.pi*440.0*t) # A 440 Hz signal

# plot a circle using the real and imaginary part of e^(i*2*pi*440*t)
plt.plot(csin.real,csin.imag,color="blue",label="Unit circle")

plt.xlabel("$\cos(2\pi440t)$")
plt.ylabel("$\sin(2\pi440t)$")
plt.legend()
plt.savefig("../figures/circle_plot.png") # remove this

if len(sys.argv) == 1: # <-- remove this line if you want
    plt.show()         # also remove the indentation, if you remove the previous line

