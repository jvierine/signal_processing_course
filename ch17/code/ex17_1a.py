import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hann


def convert_to_decibel(x: np.ndarray) -> np.ndarray:
    """Function to convert to dB."""
    return 10*np.log10(np.abs(x)**2)


N = 16384
nn = np.arange(N)
freqs = [0.0003, 0.012, 0.055, 0.102, 0.85]  # x1[n] frequencies
A = [1e5, 5e5, 1e3, 1e4, 0.5e4]              # x1[n] amplitudes
x1 = np.zeros(N)

# Create the first signal.
for i, f in enumerate(freqs):
    x1 += A[i]*np.cos(np.pi*freqs[i]*nn + np.random.randn(1))

# Create the second signal (the weak signal).
x2 = np.zeros(N)
x2[N//2] = 10.0
x2[N//2 + 1000] = -5.0
x2[N//2 - 1000] = 1.0

x = x1 + x2

# Hann window to reduce spectral leakage.
w = hann(N)

xw = np.fft.rfft(w*x, 2*N)    # Use FFT to compute the spectrum.
om_freqs = np.linspace(0, np.pi, num=len(xw))  # Partition the interval (0,pi).

plt.plot(om_freqs, convert_to_decibel(xw))
plt.xlabel(r"$\hat{\omega}$ (rad / sample)")
plt.ylabel(r"$|\hat{x}_{w}[k]|^{2}$ (dB)")
plt.title("Spectrum of $x[n]$")
# Call this if needed:
# plt.show()

try:
    plt.savefig("../figures/ex17_1a.png")
except:
    print("couldn't save file")
