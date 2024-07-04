import numpy as np
import matplotlib.pyplot as plt
import scipy.special as dd

# Partition the interval (-pi,pi) into num points.
om = np.linspace(-np.pi, np.pi, num=1000)

# Use M = 11 for the Dirichlet kernel plot.
M = 11

# Plot the two functions in the same coordinate system.
plt.plot(om, np.abs(dd.diric(om, n=M))**2, label=r"$|D_{11}(\hat{\omega})|^{2}$")
plt.plot(om, np.abs(np.exp(1j*om*(M-1)/2)*dd.diric(om, n=M))**2, label=r"$|H_{11}(\hat{\omega})|^{2}$")
plt.xlabel(r"$\hat{\omega}$")
plt.legend()
# Call this if needed.
# plt.plot()

try:
    plt.savefig("../figures/frequency_responses.png")
except:
    print("couldn't save file")
