import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as c

print("Hello World!")
# Test NumPy and SciPy.
print(np.pi)
print(c.pi)

sample_rate = 44100.0  # 44100 samples per second.
t = np.arange(101)/sample_rate  # <-- Added 101 to obtain the full circle.

csin = np.exp(1j*2.0*np.pi*440.0*t)  # A 440 Hz signal.

# Make axis aspect ratio equal for visually pleasing output.
plt.axes().set_aspect('equal')

# Plot a circle using the real and imaginary part of e^(i*2*pi*440*t).
plt.plot(csin.real, csin.imag, color="blue", label="Unit circle")

plt.xlabel(r"$\cos(2\pi440t)$")
plt.ylabel(r"$\sin(2\pi440t)$")
plt.legend()
# Call this if needed.
# plt.show()
try:
    plt.savefig("../figures/circle_plot.png")  # Remove this.
except:
    print("couldn't save file")
