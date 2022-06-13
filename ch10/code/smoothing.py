#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt

N_avg=15

# signal length
N=500
t=n.arange(N)

# signal with a rectangular pulse in the middle
# Create a random-walk signal
signal=n.cumsum(n.random.randn(N+1))

# filter signal using an averaging filter
filtered_signal=n.convolve(n.repeat(1.0/N_avg,N_avg),signal,mode="same")

plt.figure(figsize=(8,4))
plt.plot(signal,label="Signal")
plt.plot(filtered_signal,label="Running average")
plt.xlabel("Time index $n$")
plt.ylabel("Signal amplitude")
plt.legend()
plt.tight_layout()
plt.savefig("smoothing.png")
plt.show()


