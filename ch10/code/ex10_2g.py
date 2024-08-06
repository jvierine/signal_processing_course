import matplotlib.pyplot as plt
import numpy as np

L = 4
h = np.repeat(1/L, L)  # Add 1/L into an array L times.

# Compute the convolution.
h2 = np.convolve(h, h, mode="full")

plt.stem(h2)
plt.xlabel("Samples $(n)$")
plt.ylabel("$h_{2}[n]$")
plt.title("Impulse response")
# Call this if needed.
# plt.plot()

try:
    plt.savefig("../figures/h2.png")
except:
    print("couldn't save figure")
