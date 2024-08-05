import matplotlib.pyplot as plt
import numpy as np

N = 16384
n = np.arange(N)
freqs = [0.0003, 0.012, 0.055, 0.102, 0.85]  # x1[n] frequencies
A = [1e5, 5e5, 1e3, 1e4, 0.5e4]              # x1[n] amplitudes
x1 = np.zeros(N)

# Create the first signal.
for i, f in enumerate(freqs):
    x1 += A[i]*np.cos(np.pi*f*n + np.random.randn(1))

# Create the second signal (the weak signal).
x2 = np.zeros(N)
x2[N//2] = 10.0
x2[N//2 + 1000] = -5.0
x2[N//2 - 1000] = 1.0

x = x1 + x2

# Plot the signals.
plt.plot(n, x)
plt.xlabel("Samples")
plt.ylabel("$x[n]$")
# Call this if needed:
# plt.show()

try:
    plt.savefig("../figures/ex17_1.png")
except:
    print("couldn't save file")
