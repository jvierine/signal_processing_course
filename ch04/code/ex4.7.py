import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as sio

# Amplifier gain.
alpha = 10.0


def amplify(x: np.ndarray, alpha: float) -> np.ndarray:
    """A function to compress signal x (signal processing system)."""
    return (alpha*x)

# guitar_clean.wav copyright
# Original author: LG downloaded from freesound.org,
# Original file name: Guitar clean rif.wav


# The read function returns two arguments, these being the sample rate and the actual data.
wav = sio.read("guitar_clean.wav")
# Read only one stereo channel.
sample_rate = wav[0]
# Returned is a 2-dimensional NumPy array corresponding to the left and right channel.
x = wav[1][:, 0]

# Create time vector (independent variable).
time_vec = np.arange(len(x)) / float(sample_rate)

# Plot original and amplified.
plt.plot(time_vec, amplify(x, alpha), label="Amplified")
plt.plot(time_vec, x, label="Original")
plt.legend()
plt.xlabel("Time $t$")
plt.ylabel("Relative air pressure $y(t)$")
# Call this if needed.
# plt.show()

# Amplify the signal.
out = amplify(x, alpha)

# Scale maximum absolute amplitude to 0.9, because 1.0 is the maximum allowed
# by the file format.
out = 0.9*out / np.max(np.abs(out))

# Write compressed output to wav file.
sio.write("guitar_amp.wav", sample_rate, np.array(out, dtype=np.float32))

try:
    plt.savefig("../figures/ex7_plot.png")
except:
    print("couldn't save file")
