import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as sio

wav = sio.read("guitar_clean.wav")
sample_rate = wav[0]  # Sample rate.
x = wav[1][:, 0]      # Read only one stereo channel.

# Create time vector (independent variable).
time_vec = np.arange(len(x))/float(sample_rate)

# Multiply the signal with a cosine wave 
# with frequency f = 5.0 Hz.
out = x*np.cos(2.0*np.pi*time_vec*5.0)

# Plot original and modified.
plt.plot(time_vec, out, label="Output 5.0 Hz", color="darkviolet")
plt.plot(time_vec, x, label="Original", color="lime")
plt.legend()
plt.xlabel("Time $t$")
plt.ylabel("Relative air pressure $y(t)$")
# Call this if needed.
# plt.show()

try:
    plt.savefig("../figures/ex6b.png")
except:
    print("couldn't save figure")
