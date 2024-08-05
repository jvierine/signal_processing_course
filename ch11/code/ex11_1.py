import matplotlib.pyplot as plt
import numpy as np

# Partition the interval -7pi to 7pi.
om = np.linspace(-7*np.pi, 7*np.pi, num=1000)


def freq_resp(om: np.ndarray) -> np.ndarray:
    """Function for the frequency response."""
    return 42*(np.heaviside(om+5.5*np.pi, 0) - np.heaviside(om-5.5*np.pi, 0))


plt.plot(om, np.abs(freq_resp(om)), color="green")

# Plot each line in red from -7 to 7.
for k in range(-7, 8):
    plt.vlines(k*np.pi, ymin=0, ymax=42, color="red")

plt.title("Dirac comb")
plt.xlabel(r"$\omega$")
# Call this if needed.
# plt.plot()

try:
    plt.savefig("../figures/diractrain.png")
except:
    print("couldn't save figure")
