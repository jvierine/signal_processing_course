import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as sio

wav = sio.read("guitar_clean.wav")
# Figure out what the sample-rate is.
sample_rate = wav[0]
# Read the signal for only one stereo channel,
# select samples inside the file.
x = wav[1][50000:60000, 0]

# How many samples to plot and analyse.
N_samples = 1024

# Calculate spectral components using FFT
# (discrete-time Fourier series.)
c_k = np.fft.fft(x[:N_samples])

# Time in seconds.
time_vec = np.arange(N_samples)/float(sample_rate)

# Create a vector with frequencies in kHz.
freq_vec = np.fft.fftshift(np.fft.fftfreq(N_samples, d=1.0/sample_rate))/1e3
# What is magnitude squared of each spectral component in dB.
power_dB = np.fft.fftshift(10.0*np.log10(np.abs(c_k)**2.0))

# Plot time domain signal.
plt.figure(figsize=(8, 4))
plt.subplot(121)
plt.plot(1e3*time_vec, x[:1024])
plt.xlabel("Time (ms)")
plt.ylabel("Relative air pressure (unitless)")
plt.title("Time domain signal")

# Plot frequency domain signal.
plt.subplot(122)
plt.plot(freq_vec, power_dB)
plt.title("Spectral components")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Power (dB)")
plt.tight_layout()
plt.savefig("audio_spec.png")
plt.show()
