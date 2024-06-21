import matplotlib.pyplot as plt
import numpy as np

# Partition the interval (-pi, pi).
om = np.linspace(-np.pi, np.pi, num=100)


def system_function(z):
    return (1 - np.exp(1j*np.pi/4)*z**(-1))*(1 - np.exp(-1j*np.pi)*z**(-1))


def frequency_response(om):
    return system_function(np.exp(1j*om))


# Marking the zeros on the graph.
x_markers = [np.pi/4, -np.pi]
y_markers = [np.abs(frequency_response(np.pi/4)), np.abs(frequency_response(-np.pi))]

# Plot the system function with the zeros marked.
plt.plot(om, np.abs(frequency_response(om)))
plt.plot(x_markers, y_markers, "rx", label="zeros")
plt.xlabel(r"$\hat{\omega}$ (rad / sample)")
plt.ylabel(r"$|\mathcal{H}(\hat{\omega})|$")
plt.title("Magnitude response plot")
plt.legend()
# Call this if needed.
# plt.show()

try:
    plt.savefig("../figures/magnituderes.png")
except:
    print("couldn't save file")
