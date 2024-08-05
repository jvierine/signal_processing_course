import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile

audio = scipy.io.wavfile.read("b.wav")
sample_rate = audio[0]

# Read only one channel of the stereo signal.
signal = audio[1][:, 0]

# The sample rate is:
print(sample_rate)  # output is 44100 Hz.

# Partition the interval such that the 
# units become seconds.
t = np.arange(len(signal))/(sample_rate)

plt.plot(t, signal)
plt.xlabel("Time (s)")
# Call this if needed.
# plt.show()
try:
    plt.savefig("../figures/audio.png")
except:
    print("couldn't save file")
