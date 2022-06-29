import numpy as n
import matplotlib.pyplot as plt
import sys

L = 4
h = n.repeat(1/L,L)              # add 1/L into an array L times

h2 = n.convolve(h,h,mode="full") # compute the convolution

plt.stem(h2)
plt.xlabel("Samples $(n)$")
plt.ylabel("$h_{2}[n]$")
plt.title("Impulse response")
plt.savefig("../figures/h2.png")
if len(sys.argv) == 1:
    plt.show()