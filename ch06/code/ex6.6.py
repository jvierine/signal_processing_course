import numpy as n
import matplotlib.pyplot as plt
import sys

# time vector 0 to 1 seconds, 1000 Hz sample rate
t = n.arange(1000)/1000.0

# frequency of 10 Hz
om0 = 2.0*n.pi*10.0

# frequency of 32 Hz
om1 = 2.0*n.pi*32.0

# create complex sinusoidal signal
z = n.exp(1j*om0*t)

# shift z in frequency by multiplying with another 
# complex sinusoidal signal of frequency om1
# the result has a frequency of 42.0 Hz = 10.0 Hz + 32.0 Hz
z_shifted = z*n.exp(1j*om1*t)

# plot the signals
plt.subplot(211)
plt.plot(t,z.real,label="Real")
plt.plot(t,z.imag,label="Imag")
plt.title("Original signal")
plt.xlabel("Time (s)")
plt.legend()
plt.subplot(212)
plt.plot(t,z_shifted.real,label="Real")
plt.plot(t,z_shifted.imag,label="Imag")
plt.title("New signal")
plt.xlabel("Time (s)")
plt.legend()
plt.savefig("../figures/ex6a.png")

if len(sys.argv) == 1:
    plt.show()