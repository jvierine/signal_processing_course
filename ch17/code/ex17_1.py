import numpy as n
import matplotlib.pyplot as plt
import sys

N = 16384
nn = n.arange(N)
freqs = [0.0003,0.012,0.055,0.102,0.85] # x1[n] frequencies
A = [1e5,5e5,1e3,1e4,0.5e4]             # x1[n] amplitudes
x1 = n.zeros(N)

# create the first signal
for i,f in enumerate(freqs):
    x1 += A[i]*n.cos(n.pi*freqs[i]*nn + n.random.randn(1))

# create the second signal (the weak signal)
x2 = n.zeros(N)
x2[int(N/2)] = 10.0
x2[int(N/2)+1000] = -5.0
x2[int(N/2)-1000] = 1.0

x = x1 + x2

# plot the signals
plt.plot(nn,x)
plt.xlabel("Samples")
plt.ylabel("$x[n]$")
plt.savefig("../figures/ex17_1.png")

if len(sys.argv) == 1:
    plt.show()