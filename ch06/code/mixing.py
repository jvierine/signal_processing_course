import numpy as n
import matplotlib.pyplot as plt

# Time vector 0 to 1 seconds, 1000 Hz sampler rate
t=n.arange(1000)/1000.0
# Frequency of 10 Hz
om0=2.0*n.pi*10.0
# Frequency of 5 Hz
om1=2.0*n.pi*5.0
# Create complex sinusoidal signal
z=n.exp(1j*om0*t)
# Shift z in frequency by multiplying with another complex sinusoidal signal of frequency om1. 
z_shifted=z*n.exp(1j*om1*t)

# Plot signals
plt.subplot(211)
plt.plot(t,z.real,label="Real")
plt.plot(t,z.imag,label="Imag")
plt.title("Original signal")
plt.xlabel("Time (s)")
plt.legend()
plt.subplot(212)
plt.plot(t,z_shifted.real,label="Real")
plt.plot(t,z_shifted.imag,label="Imag")
plt.title("Frequency shifted signal")
plt.legend()
plt.xlabel("Time (s)")
plt.show()
