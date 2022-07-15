import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile

audio = scipy.io.wavfile.read("b.wav")
sample_rate = audio[0]
# read only one channel of the stereo signal
signal = audio[1][:,0]

# the sample rate is
print(sample_rate)  # output is 44100 Hz

# partition the interval such that the units become seconds
t = n.arange(len(signal))/(sample_rate)

plt.plot(t,signal)
plt.xlabel("Time (s)")
# call this if needed
# plt.show()
try:
    plt.savefig("../figures/audio.png")
except:
    print("couldn't save file")
