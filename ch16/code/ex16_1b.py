import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile
import sys

audio = scipy.io.wavfile.read("../../code/023_dynamic_spectrum/b.wav")
sample_rate = audio[0]
# read only one channel of the stereo signal
signal = audio[1][:,0]

# the sample rate is
print(sample_rate)

# output is 44100 Hz

# partition the interval such that the units become seconds
t = n.arange(len(signal))/(sample_rate)

plt.plot(t,signal)
plt.xlabel("Time (s)")
plt.savefig("../figures/audio.png")
if len(sys.argv) == 1:
    plt.show()