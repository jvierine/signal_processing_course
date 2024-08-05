import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hann


def spectrogram(x, M=1024, N=128, delta_n=100):
    """
    x = signal
    M = FFT length
    N = window function length
    delta_n = step step
    """

    max_t = int(np.floor((len(x)-N)/delta_n))
    X = np.zeros([max_t, M], dtype=np.complex64)
    w = hann(N)
    xin = np.zeros(N)

    for i in range(max_t):
        # Zero padded windowed FFT.
        xin[0:N] = x[i*delta_n + np.arange(N)]
        X[i, :] = np.fft.fft(w*xin, M)

    return (X)


# Sample rate (Hz).
fs = 4096.0

# Sample indices (one second of signal).
n = np.arange(4096)
# Generate a chirp signal.
x = np.sin(0.15e-14*n**5.0)

# Time step.
delta_n = 25
M = 2048
# Create dynamic spectrum.
S = spectrogram(x, M=M, N=128, delta_n=delta_n)

freqs = np.fft.fftfreq(2048, d=1.0/fs)
time = delta_n*np.arange(S.shape[0])/fs

plt.figure(figsize=(12, 10))
plt.subplot(211)
plt.plot(n/fs, x)
plt.title("Signal $x[n]$")
plt.xlabel("Time (s)")
plt.ylabel("Signal amplitude")
plt.subplot(212)

plt.title("Spectrogram")
plt.pcolormesh(time, freqs[:int(M/2)], np.transpose(10.0*np.log10(np.abs(S[:, :int(M/2)])**2.0)), vmin=0)
plt.xlim([0, np.max(time)])
plt.ylim([0, fs/2.0])
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
cb = plt.colorbar(orientation="horizontal")
cb.set_label("dB")
plt.tight_layout()
plt.savefig("dynspec.png")
plt.show()
