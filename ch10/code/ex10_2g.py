import numpy as n
import matplotlib.pyplot as plt

L = 4
h = n.repeat(1/L,L)              # add 1/L into an array L times

h2 = n.convolve(h,h,mode="full") # compute the convolution

plt.stem(h2)
plt.xlabel("Samples $(n)$")
plt.ylabel("$h_{2}[n]$")
plt.title("Impulse response")
# call this if needed
# plt.plot()

try:
    plt.savefig("../figures/h2.png")
except:
    print("couldn't save figure")