import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as sio

# Amplifier gain.
alpha = 10.0

# A function to compress signal x (signal processing system.)
def amplify(x, alpha):
    return alpha*x

# Read wav file (read only one stereo channel.)
#
# Guitar_clean.wav copyright
# Original author: LG downloaded from freesound.org,
# Original file name: Guitar clean rif.wav
wav = sio.read("guitar_clean.wav")
sample_rate = wav[0]
# Read only one stereo channel.
x = wav[1][:, 0]

# Create time vector (independent variable.)
time_vec = np.arange(len(x))/float(sample_rate)

# Plot original and amplified.
plt.plot(time_vec, amplify(x, alpha), label="Amplified")
plt.plot(time_vec, x, label="Original")
plt.legend()
plt.xlabel("Time $t$")
plt.ylabel("Relative air pressure $y(t)$")
plt.show()

out = amplify(x, alpha)

# Scale maximum absolute amplitude to 0.9, 
# because 1.0 is the maximum allowed by the file .wav file format.
# Note that this will not allow you to hear the audio signal
# amplitude increasing.
out = 0.9*out/np.max(np.abs(out))
# Write compressed output to wav file.

# Patch from Jostein and Adrian (cast to 32 bit float.)
sio.write("guitar_amp.wav", sample_rate, np.array(out, dtype=np.float32))
