import numpy as n
import scipy.io.wavfile as sio
import matplotlib.pyplot as plt
import sys

wav = sio.read("../../code/003_guitar/guitar_clean.wav")
sample_rate = wav[0] # sample rate
x = wav[1][:,0]      # read only one stereo channel

# create time vector (independent variable)
time_vec = n.arange(len(x))/float(sample_rate)

# multiply the signal with a cosine wave with frequency f = 5.0 Hz
out = x*n.cos(2.0*n.pi*time_vec*5.0)

# plot original and modified
plt.plot(time_vec,out,label="Output 5.0 Hz")
plt.plot(time_vec,x,label="Original")
plt.legend()
plt.xlabel("Time $t$")
plt.ylabel("Relative air pressure $y(t)$")
plt.savefig("../figures/ex6b.png")
if len(sys.argv) == 1:
    plt.show()