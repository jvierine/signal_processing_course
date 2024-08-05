import matplotlib.pyplot as plt
import numpy as np


def H1(omega: np.ndarray) -> np.ndarray:
    """Frequency response for the Hann window with T = 1."""
    return (np.sin(omega/2)/omega + (1/2)*np.sin(np.pi - (1/2)*omega)/(2*np.pi - omega) + (1/2)*np.sin(np.pi + (1/2)*omega)/(2*np.pi + omega))*np.exp(-1j*1/2*omega)


def H2(omega: np.ndarray) -> np.ndarray:
    """Frequency response for the rectangular window with T = 1."""
    return 2*np.sin(omega/2)/omega*np.exp(-1j*1/2*omega)


def convert_to_decibel(x: np.ndarray) -> np.ndarray:
    return 10*np.log10(np.power(np.abs(x), 2))


# Partition the interval (-10pi, 10pi) into 1000 equally spaced points.
x = np.linspace(-10*np.pi, 10*np.pi, num=1000)

# Plot the window functions to compare
# radians per sample on the x-axis and dB on the y-axis.
plt.plot(x, convert_to_decibel(H1(x)), label="Hann window")
plt.plot(x, convert_to_decibel(H2(x)), label="Rectangular window")
plt.xlabel(r"$\hat{\omega}$")
plt.ylim(-120, 10)   # Limit the y-axis to (-120,10).
plt.legend()
# Call this if needed.
# plt.show()

try:
    plt.savefig("../figures/filters.png")
except:
    print("couldn't save file")
