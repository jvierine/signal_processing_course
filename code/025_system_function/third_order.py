import matplotlib.pyplot as plt
import numpy as np


# Define system function.
def h(z):
    return ((1-z**(-1))*(1-np.exp(1j*np.pi/3.0)*z**(-1))*(1-np.exp(-1j*(np.pi/3))*z**(-1)))


xx = np.linspace(-3, 3, num=1000)
yy = np.linspace(-3, 3, num=1000)
x, y = np.meshgrid(xx, yy)

fig, axs = plt.subplots(2, 1, figsize=(3, 6))

# Plot magnitude of system function.
c = axs[0].pcolormesh(xx, yy, 10.0*np.log10(np.abs(h(x+1j*y))**2.0), vmin=-20, vmax=20, cmap="jet")
fig.colorbar(c, ax=axs[0])
om = np.linspace(0, 2.0*np.pi, num=1000)
axs[0].plot(np.cos(om), np.sin(om), color="white")
axs[0].set_aspect('equal')
axs[0].set_ylabel("Imaginary part of z")
axs[0].set_xlabel("Real part of z")
axs[0].set_xlim([-1.5, 1.5])
axs[0].set_ylim([-1.5, 1.5])
axs[0].set_title("$|\\mathcal{H}(z)|^2$ (dB)")

# Plot phase angle of system function.
c = axs[1].pcolormesh(xx, yy, np.angle(h(x+1j*y)), cmap="jet")
fig.colorbar(c, ax=axs[1])
axs[1].set_aspect('equal')
axs[1].set_ylabel("Imaginary part of z")
axs[1].set_xlabel("Real part of z")
axs[1].set_xlim([-1.5, 1.5])
axs[1].set_ylim([-1.5, 1.5])

axs[1].set_title("$\\angle\\mathcal{H}(z)$")

om = np.linspace(0, 2.0*np.pi, num=1000)
axs[1].plot(np.cos(om), np.sin(om), color="white")
plt.tight_layout()
plt.savefig("z_mag_angle.png")
plt.show()
