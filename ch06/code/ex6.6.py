import numpy as np
import matplotlib.pyplot as plt

# Time vector 0 to 1 seconds, 1000 Hz sample rate.
t = np.arange(1000)/1000.0

# Frequency of 10.0 Hz and 32.0 Hz.
om0 = 2.0*np.pi*10.0
om1 = 2.0*np.pi*32.0

# Create complex sinusoidal signal.
z = np.exp(1j*om0*t)

# Shift z in frequency by multiplying with another
# complex sinusoidal signal of frequency om1,
# the result has a frequency of 42.0 Hz = 10.0 Hz + 32.0 Hz.
z_shifted = z*np.exp(1j*om1*t)

plt.subplot(211)
plt.plot(t, z.real, label="Real", color="darkviolet")
plt.plot(t, z.imag, label="Imag", color="lime")
plt.title("Original signal")
plt.xlabel("Time (s)")
plt.legend()
plt.subplot(212)
plt.plot(t, z_shifted.real, label="Real", color="darkviolet")
plt.plot(t, z_shifted.imag, label="Imag", color="lime")
plt.title("New signal")
plt.xlabel("Time (s)")
plt.legend()
plt.tight_layout()
# Call this if needed.
# plt.show()

try:
    plt.savefig("../figures/ex6a.png")
except:
    print("couldn't save figure")
