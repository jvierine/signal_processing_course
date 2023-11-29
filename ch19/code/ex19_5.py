from typing import Callable

import matplotlib.pyplot as plt
import numpy as np

# Partition the range (-pi, pi).
omhat = np.linspace(-np.pi, np.pi, num=100000)

# Roots/poles of diagram a) and b).
alpha1 = (2*np.sqrt(2))**(-1) + (2*np.sqrt(2))**(-1)*1j
alpha2 = (2*np.sqrt(2))**(-1) - (2*np.sqrt(2))**(-1)*1j

# Roots of diagram c).
beta1 = -(2*np.sqrt(2))**(-1) + (2*np.sqrt(2))**(-1)*1j
beta2 = -(2*np.sqrt(2))**(-1) - (2*np.sqrt(2))**(-1)*1j


def Ha(z: np.ndarray) -> np.ndarray:
    return (z - 1)*(z - alpha1*z)*(z - alpha2)/(z**3)


def Hb(z: np.ndarray) -> np.ndarray:
    return (z)/(z - 1)*(z - alpha1)*(z - alpha2)


def Hc(z: np.ndarray) -> np.ndarray:
    return (z + 1)*(z - beta1)*(z - beta2)/(z**3)


def magn_resp(func: Callable) -> np.ndarray:
    """Function to convert the system function to the magnitude response function."""
    return np.abs(func(np.exp(1j*omhat)))


fig, axs = plt.subplots(3)
fig.suptitle("Magnitude response")
axs[0].plot(omhat, magn_resp(Ha), label="a)", color="blue")
axs[1].plot(omhat, magn_resp(Hb), label="b)", color="red")
axs[1].set_ylim(0, 10)   # Limit diagram b) as it is unstable.
axs[2].plot(omhat, magn_resp(Hc), label="c)", color="orange")
fig.legend()

# Set the labels.
for ax in axs:
    ax.set_xlabel(r"$\hat{\omega}$")
    ax.set_ylabel(r"$|\mathcal{H}(\hat{\omega})|$")

plt.tight_layout()
# Call this if needed.
# plt.show()

try:
    plt.savefig("../figures/magn_resp_diag")
except:
    print("couldn't save file")
