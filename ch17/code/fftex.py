import numpy as np

N = 16384
n = np.arange(N)
freqs = [0.0003, 0.012, 0.055, 0.102, 0.85]
A = [1e5, 0.5e5, 1e3, 1e4, 0.5e4]
x1 = np.zeros(N)

for i, f in enumerate(freqs):
    x1 += A[i]*np.cos(np.pi*f*n + np.random.randn(1))

# Weak signal at the middle of the signal.
x2 = np.zeros(N)
x2[int(N/2)] = 10.0
x2[int(N/2)+1000] = -5.0
x2[int(N/2)-1000] = 1.0

x = x1 + x2
