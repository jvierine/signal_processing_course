import numpy as n
import matplotlib.pyplot as plt

# sample indices for 10000 samples
m = n.arange(10000)

# sample period
Ts = 1e-4

# create a signal consisting of three sinusoids
x = n.cos(2*n.pi*4000.0*Ts*m) + 2*n.cos(2*n.pi*1000.0*Ts*m) + 3*n.cos(2*n.pi*2500.0*Ts*m)

# call fftfreq to compute the frequencies in units of hertz
# the function takes in the first argument, which is the length of the window and second argument for the stepsize (Ts)
# use fftshift to shift the frequencies to have zero in the middle; this includes both positive and negative frequencies
freq = n.fft.fftshift(n.fft.fftfreq(len(m),d=Ts))

# plot the magnitude of sinusoids using fft
plt.plot(freq,n.abs(n.fft.fft(x))/len(m))
# call this if needed
# plt.show()

try:
    plt.tight_layout()
    plt.savefig("../figures/ex15_c.png")
except:
    print("couldn't save file")