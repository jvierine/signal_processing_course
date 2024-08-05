import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hann


def convert_to_decibel(x: np.ndarray) -> np.ndarray:
    """Function to convert to dB."""
    return 10*np.log10(np.abs(x)**2)


N = 16384
n = np.arange(N)
freqs = [0.0003, 0.012, 0.055, 0.102, 0.85]  # x1[n] frequencies
A = [1e5, 5e5, 1e3, 1e4, 0.5e4]              # x1[n] amplitudes
x1 = np.zeros(N)

# Create the first signal.
for i, f in enumerate(freqs):
    x1 += A[i]*np.cos(np.pi*f*n + np.random.randn(1))

# Create the second signal (the weak signal).
x2 = np.zeros(N)
x2[N//2] = 10.0
x2[N//2 + 1000] = -5.0
x2[N//2 - 1000] = 1.0

x = x1 + x2

# Hann window to reduce spectral leakage.
w = hann(N)

xw = np.fft.rfft(w*x, 2*N)                     # Use FFT to compute the spectrum.
om_freqs = np.linspace(0, np.pi, num=len(xw))  # Partition the interval (0, pi).

# Define a filter to reduce strong spectral components.
h = np.ones(len(xw))  # Initialize each entry to 1.

# Lower the strong spectral components.
# Look at the previous exercise output plot to determine the intervals
# alternatively, plot the spectrum with samples on x-axis instead of \hat{\omega}.
h[:1050] = 1.0/np.abs(xw[:1050])
h[1500:1860] = 1.0/np.abs(xw[1500:1860])
h[13500:14200] = 1.0/np.abs(xw[13500:14200])

# Plot the spectral power to compare the two signals.
plt.plot(om_freqs, convert_to_decibel(xw), label="Original spectrum")
plt.plot(om_freqs, convert_to_decibel(xw*h), label="Windowed spectrum")
plt.xlabel(r"$\hat{\omega}$ (rad / sample)")
plt.ylabel("Power of spectrum (dB)")
plt.legend()
# Call this if needed:
# plt.show()

# Finally, inverse DFT to obtain the filtered signal.
filter_signal = np.fft.irfft(h*xw)
plt.plot(filter_signal)
plt.xlabel("Samples")
plt.title("Filtered signal")
# Call this if needed:
# plt.show()

# Solution manual figure saving:
plt.clf()   # Clear figures.
plt.plot(om_freqs, convert_to_decibel(xw), label="Original spectrum")
plt.plot(om_freqs, convert_to_decibel(xw*h), label="Windowed spectrum")
plt.xlabel(r"$\hat{\omega}$ (rad / sample)")
plt.ylabel("Power of spectrum (dB)")
plt.legend()
plt.savefig("../figures/spectral_pw.png")

plt.clf()
filter_signal = np.fft.irfft(h*xw)
plt.plot(filter_signal)
plt.xlabel("Samples")
plt.title("Filtered signal")
plt.savefig("../figures/filtered_signal.png")
