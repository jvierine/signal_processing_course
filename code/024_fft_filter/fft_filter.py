#
# Using DFT to create a filter that
# attenuate spectral components to allow
# weak signals buried under the strong but
# spectrally narrow signals to be found.
#
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hann

N = 4096*2*2
n = np.arange(N)
freqs = [0.0012, 0.0021, 0.0032, 0.1, 0.9]
A = [1e5, 0.5e5, 1e3, 1e4, 0.5e4]
strong_signal = np.zeros(N)

for i, f in enumerate(freqs):
    strong_signal += A[i]*np.cos(np.pi*f*n + np.random.randn(1))

# Weak signal at the middle of the signal.
weak_signal = np.zeros(N)
weak_signal[int(N/2)] = 10.0
weak_signal[int(N/2)+1000] = -5.0
weak_signal[int(N/2)-1000] = 1.0

x = strong_signal+weak_signal

plt.subplot(311)
plt.plot(n, strong_signal)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x_1[n]$")
plt.title("Strong signal")
plt.subplot(312)
plt.plot(n, weak_signal)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x_2[n]$")
plt.title("Weak signal")
plt.subplot(313)
plt.plot(n, x)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x[n]=x_1[n]+x_2[n]$")
plt.title("Total signal")
plt.tight_layout()
plt.savefig("filter_signals.png")
plt.show()

# Windowed zero-padded DFT.
w = hann(N)
WX = np.fft.rfft(w*x, 2*N)

# Create a filter than filters out strong spectral components the signal.
WH = np.zeros(len(WX))
WH[:] = 1.0  # Pass all frequencies.
WH[0:400] = 1.0/np.abs(WX[0:400])  # Attenuate strong frequencies.
WH[1400:1800] = 1.0/np.abs(WX[1400:1800])  # Attenuate strong frequencies.
WH[14000:15000] = 1.0/np.abs(WX[14000:15000])  # Attenuate strong frequencies.

plt.semilogy(np.abs(WX), label=r"$|\hat{x}[k]|$")
plt.semilogy(np.abs(WX*WH), label=r"$|\hat{y}[k]|$")
plt.legend()
plt.title("Original and filtered spectrum")
plt.tight_layout()
plt.savefig("filter_spec.png")
plt.show()

# Apply filter in frequency domain.
wy = np.fft.irfft(WH*WX)[0:N]

# Plot filtered signal and compare with original weak
# signal buried under stronger signals
plt.subplot(211)
plt.plot(n, wy)
plt.title("Filtered signal")
plt.xlabel("$n$")
plt.ylabel("$y[n]$")

plt.subplot(212)
plt.plot(n, weak_signal)
plt.title("Original weak signal")
plt.xlabel("$n$")
plt.ylabel("$x_2[n]$")
plt.tight_layout()
plt.savefig("filter_filtered.png")
plt.show()
