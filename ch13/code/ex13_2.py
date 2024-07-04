import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as sw
from scipy.signal.windows import hann

# Read the noisy signal.
ts = sw.read("crappy.wav")
sr = ts[0]
crap = ts[1]

# Filter length.
N = 4000

# Frequencies of noise (units of Hz).
f0 = 3e3
f1 = 5e3

# Make the band a bit wider to hopefully remove some boundary effects.
sf0 = f0 - 0.2e3
sf1 = f1 + 0.2e3

# Calculate the discrete-time frequencies (units of rad / sample).
om0 = 2.0*np.pi*sf0/sr
om1 = 2.0*np.pi*sf1/sr

# Declare the filter as 0.
h = np.zeros(N)

# Use a Hann window.
w = hann(N)


# The band-stop filter we found in a) with a Hann window function.
for i in range(N):
    if i == N // 2:   # Careful to avoid the 0/0 problem.
        h[i] = (1 + (om0 - om1)/(np.pi))*w[i]
    else:
        h[i] = (np.sin(om0 * (i - N // 2)) / ((i - N // 2) * np.pi) - np.sin(om1 * (i - N // 2)) / ((i - N // 2) * np.pi)) * w[i]

# In frequency domain, we multiply the filter with the spectral representation.
# Multiplication in frequency domain correspond to convolution in time domain
# therefore, convolve the band-stop filter and the signal.
uncrap = np.convolve(crap, h, mode="valid")
# ^ mode = valid will remove some boundary effects.

# Scale to 0.9, because 1.0 is the maximum allowed by the .wav file format.
uncrap = 0.9*uncrap/np.max(np.abs(uncrap))

# Save the filtered audio file.
sw.write("test_uncrappy.wav", sr, np.array(uncrap, dtype=np.float32))


def convert_to_decibel(x: np.ndarray) -> np.ndarray:
    return 10*np.log10(np.abs(x)**2)


plt.subplot(121)
plt.plot(h)
plt.title("Impulse response")
plt.xlabel("Samples [n]")
plt.ylabel("$h[n]$")
plt.xlim(N//2-100, N//2+100)
plt.subplot(122)
plt.plot(np.fft.fftshift(np.fft.fftfreq(len(h), d=1.0/sr))/1e3, convert_to_decibel(np.fft.fftshift(np.fft.fft(h))))
plt.title("Frequency response")
plt.xlabel("Frequency (kHz)")
plt.ylabel(r"$|\mathcal{H}(f)|^{2}$ (dB)")
plt.tight_layout()
plt.savefig("../figures/impulse_response.png")
# plt.show()

plt.clf()
plt.plot(np.fft.fftshift(np.fft.fftfreq(len(uncrap), d=1.0/sr))/1e3, convert_to_decibel(np.fft.fftshift(np.fft.fft(uncrap))), color="red")
plt.title("Spectrum of the filtered signal")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Power (dB)")
plt.savefig("../figures/freq_spec_filter.png")
# plt.show()
