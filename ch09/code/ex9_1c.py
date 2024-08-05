import matplotlib.pyplot as plt
import numpy as np

fs = 100  # Sample rate in Hz.
om0 = 2*np.pi*10042

def omk(k):
    """Function to compute the different aliases."""
    return om0/fs + 2*np.pi*k

# Plot on the interval (-3*np.pi, 3*np.pi).
om = np.linspace(-3*np.pi, 3*np.pi, num=1000)

# Plot the components.
plt.vlines(omk(-100), ymin=0, ymax=1, color="blue", label="Principal value")
plt.vlines(omk(-99), ymin=0, ymax=1, color="red", label="Alias")
plt.vlines(omk(-101), ymin=0, ymax=1, color="red")
plt.vlines(-3*np.pi, ymin=0, ymax=1, color="green", label=r"$(-3\pi,3\pi)$")
plt.vlines(3*np.pi, ymin=0, ymax=1, color="green")
plt.xlabel(r"$\hat{\omega}$")
plt.ylabel(r"$\hat{x}(\omega)$")
plt.grid(True)
plt.legend()
plt.show()
