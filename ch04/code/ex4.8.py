import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as sio

alpha = 2.0  # Amplifier gain.
beta = 0.08  # Cut off.


def distortion(x: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    """A function to apply distortion to a signal x."""
    y = np.zeros(x.size)

    print(x.dtype)

    # Create masks based on the conditions.
    mask1 = alpha*x < -beta
    mask2 = np.abs(alpha*x) <= beta
    mask3 = alpha*x > beta

    # The masks are arrays that are True/False, assign values based on the True/False value.
    y[mask1] = -beta
    y[mask2] = alpha*x[mask2]
    y[mask3] = beta

    return y


# Read wav file (read only one stereo channel).
wav = sio.read("guitar_clean.wav")
sample_rate = wav[0]
# Read only one stereo channel.
x = wav[1][:, 0]

# Create time vector (independent variable).
time_vec = np.arange(x.size)/float(sample_rate)

# Apply distortion to the signal.
out = distortion(x, alpha, beta)

# Plot original and amplified.
plt.plot(time_vec, out, label="Distorted")
plt.plot(time_vec, x, label="Original")
plt.legend()
plt.xlabel("Time $t$")
plt.ylabel("Relative air pressure $y(t)$")
# Call this if needed.
# plt.plot()

# Scale maximum absolute amplitude to 0.9, because 1.0 is the
# maximum allowed by the file format.
out = 0.9*out/np.max(np.abs(out))
# Write compressed output to wav file.
sio.write("guitar_dist.wav", sample_rate, np.array(out, dtype=np.float32))

try:
    plt.savefig("../figures/ex9_plot.png")
except:
    print("couldn't save file")