import matplotlib.pyplot as plt
import numpy as np

# Sample values we want to plot on.
nn = np.array([-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Values for the impulse response function.
h = np.array([0, 1, 1, 3, -0.5, 0, 0, 0, 0, 0, 0, 0, 4])

# Plot as a stem plot to emphasize the
# discrete nature of the function.
plt.stem(nn, h)
plt.xlabel("samples [n]")
plt.ylabel("$h[n]$")
plt.title("Impulse response")
# Call this if needed:
# plt.show()

try:
    plt.savefig("../figures/18_2.png")
except:
    print("couldn't save file")
