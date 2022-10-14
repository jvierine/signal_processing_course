import numpy as n
import matplotlib.pyplot as plt
plt.figure(figsize=(6*0.7,4*0.7))

# sample indices for 10000 samples
m=n.arange(10000)
# sample period 
Ts=1e-4
# create a signal consisting of three sinusoids
x=n.cos(2.0*n.pi*4000.0*Ts*m)+2*n.cos(2.0*n.pi*1000.0*Ts*m)+3*n.cos(2.0*n.pi*2500.0*Ts*m)
# plot the magnitude of sinusoids using fft
plt.plot(n.abs(n.fft.fft(x))/len(m))
# call this if needed
# plt.show()

try:
    plt.tight_layout()
    plt.savefig("../figures/ex15_2.png")
except:
    print("couldn't save file")

