import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hann

om = np.linspace(-np.pi, np.pi, num=1000)

# Low pass filter cutoff frequency.
omc = 0.1*np.pi

# Sample indices for filter impulse response.
nn = np.arange(-100, 100)

# Ideal low-pass filter impulse response with cutoff at omc.
sinc = np.sin(omc*nn)/(np.pi*nn)
# Use L'Hopital's rule to determine value at nn=0.
sinc[nn == 0] = omc/np.pi

# Window function and length.
wf = np.zeros(len(nn))
wl = 100

# Hann window.
W = hann(wl)
# Center window function around 0.

wf[int(len(wf)/2) - int(wl/2) + np.arange(wl)] = W

# Use a zero-padded DFT to approximate the frequency response
# of the windowed low-pass filter.
WX = np.fft.fftshift(np.fft.fft(wf*sinc, 4096))
# Vector of frequencies for DFT.
omw = np.linspace(-np.pi, np.pi, num=len(WX))

# Ideal frequency response (boxcar).
X = np.zeros(len(om))
X[:] = 1e-120  # Very small number to avoid taking a log of 0.
X[np.abs(om) < omc] = 1.0

# Plot power spectral response in dB scale for
# ideal and windowed filters.
plt.figure(figsize=(10, 8))
plt.subplot(212)
plt.plot(om, 10.0*np.log10(np.abs(X)**2.0), label="Ideal", color="blue")
plt.plot(omw, 10.0*np.log10(np.abs(WX)**2.0), label="Windowed", color="green")
plt.ylim([-130, 3])
plt.legend()
plt.xlabel(r"$\hat{\omega}$")
plt.ylabel(r"$10\log_{10}|H(\hat{\omega})|^2$")
plt.title("Magnitude response")

# Plot the impulse response of ideal and windowed filter.
plt.subplot(211)
plt.stem(nn, sinc, "b", markerfmt="bo", label="Ideal")
plt.plot(nn, np.max(sinc)*wf, label="Window", color="green")
plt.stem(nn, wf*sinc, "g", markerfmt="go", label="Windowed")
plt.legend()
plt.xlabel("$n$")
plt.ylabel("$h[n]$")
plt.title("Impulse response")
plt.tight_layout()
plt.savefig("windowed_lpf.png")
plt.show()
