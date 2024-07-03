import numpy as np
import matplotlib.pyplot as plt

N_avg = 15

# Signal length.
N = 500
t = np.arange(N)

# Signal with a rectangular pulse in the middle.
# Create a random-walk signal.
signal = np.cumsum(np.random.randn(N+1))

# Filter signal using an averaging filter.
filtered_signal = np.convolve(np.repeat(1.0/N_avg, N_avg), signal, mode="same")

plt.figure(figsize=(8, 4))
plt.plot(signal, label="Signal")
plt.plot(filtered_signal, label="Running average")
plt.xlabel("Time index $n$")
plt.ylabel("Signal amplitude")
plt.legend()
plt.tight_layout()
plt.savefig("smoothing.png")
plt.show()
