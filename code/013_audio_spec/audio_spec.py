import numpy as n
import scipy.io.wavfile as sio
import matplotlib.pyplot as plt

# read .wav format audio file
wav=sio.read("guitar_clean.wav")
# figure out what the sample-rate is
sample_rate=wav[0]
# read the signal for only one stereo channel
# select samples inside the file
x=wav[1][50000:60000,0]

# how many samples to plot and analyse
N_samples=1024

# calculate spectral components using FFT
# (discrete-time Fourier series)
c_k=n.fft.fft(x[0:N_samples])

# time in seconds
time_vec = n.arange(N_samples)/float(sample_rate)

# create a vector with frequencies in kHz
freq_vec=n.fft.fftshift(n.fft.fftfreq(N_samples,d=1.0/sample_rate))/1e3
# what is magnitude squared of each spectral component in dB
power_dB=n.fft.fftshift(10.0*n.log10(n.abs(c_k)**2.0))

# plot time domain signal
plt.figure(figsize=(8,4))
plt.subplot(121)
plt.plot(1e3*time_vec,x[0:1024])
plt.xlabel("Time (ms)")
plt.ylabel("Relative air pressure (unitless)")
plt.title("Time domain signal")

# plot frequency domain signal
plt.subplot(122)
plt.plot(freq_vec,power_dB)
plt.title("Spectral components")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Power (dB)")
plt.tight_layout()
plt.savefig("audio_spec.png")
plt.show()
