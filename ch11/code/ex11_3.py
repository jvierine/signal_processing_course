import numpy as np
import matplotlib.pyplot as plt

# Plot in the principal spectrum (-pi, pi).
om = np.linspace(-np.pi, np.pi, num=1000)

# For simplicity take Ts as 1.
Ts = 1

def freq_resp(om: np.ndarray) -> np.ndarray:
    """Definition of the frequency response function."""
    return 2/(Ts**2)*(np.cos(om)-1)


# Plot the frequency response function over (-pi, pi).
plt.plot(om, np.abs(freq_resp(om)), label=r"$\mathcal{H}(\hat{\omega})$")
plt.legend()
# Call this if needed.
# plt.plot()

try:
    plt.savefig("../figures/freq13.png")
except:
    print("couldn't save file")
