import matplotlib.pyplot as plt
import numpy as np


# Function to convert to dB.
def convert_to_decibel(x):
    return 10*np.log10(np.abs(x)**2)


# Partition the interval (-pi, pi).
om = np.linspace(-np.pi, np.pi, num=10000)


def system_function(z):
    return (1 - np.exp(1j*100*np.pi/441)*z**(-1))*(1 - np.exp(-1j*100*np.pi/441)*z**(-1))*(1 - np.exp(20*1j*np.pi/441)*z**(-1))*(1 - np.exp(-20*1j*np.pi/441)*z**(-1))*z**4


def frequency_response(om):
    return system_function(np.exp(1j*om))


# Plot the system function with the zeros marked.
plt.plot(om, convert_to_decibel(frequency_response(om)), label=r"$\mathcal{H}(\hat{\omega})$")
plt.xlabel(r"$\hat{\omega}$ (rad / sample)")
plt.ylabel(r"$|\mathcal{H}(\hat{\omega})|$")
plt.title("Magnitude response plot")
plt.legend()
# Call this if needed:
# plt.show()

try:
    plt.savefig("../figures/mag2.png")
except:
    print("couldn't save file")
