#!/usr/bin/env python
#
# Represent an audio signal with only a small number of
# spectral components (basic idea behind audio compression)
# Juha Vierinen, 2020
# 
import scipy.io.wavfile as sw
import numpy as n
import matplotlib.pyplot as plt


# compress and decompress audio file
# compression_ratio=0.95 means that 95%
# of the smallest amplitude spectral
# components are thrown away
cr=0.99

# read wav file
ts=sw.read("7na.wav")
sr=ts[0]     # sample rate
clip=ts[1]   # extract audio file as numpy data vector
if len(clip.shape)==2: # if stereo, only use one channel
    print("converting to mono")
    clip=ts[1][:,0]+ts[1][:,1]

# if clip is too long, make it shorter (1 million samples)
if len(clip)>1000000:
    clip=clip[0:1000000]

# Fourier transform to obtain the phase and amplitude of each spectral component
F = n.fft.fft(clip)
# Make a copy of the original for plotting purposes
F_orig=n.copy(F)

# what is the absolute value (amplitude) of each spectral component
mag=n.abs(F)

# sort by amplitude
idx=n.argsort(mag)

# figure out what is the smallest component that we'll include
smallest_comp=mag[idx[int(cr*len(idx))]]

# remove spectral components with magnitude less than smallest_comp
F[mag < smallest_comp]=0.0

# inverse Fourier transform to obtain signal composed of just a few spectral components
compressed=n.real(n.fft.ifft(F))

# plot the absolute values of the original and sparse spectral representation
freq_vec=n.fft.fftshift(n.fft.fftfreq(len(F),d=1/float(sr)))
plt.plot(freq_vec/1e3,n.fft.fftshift(10.0*n.log10(n.abs(F_orig)**2.0)),label="Original")
plt.xlim([0,float(sr)/1e3/2.0])
plt.plot(freq_vec/1e3,n.fft.fftshift(10.0*n.log10(n.abs(F)**2.0)),label="Compressed")
plt.legend()
plt.xlabel("Frequency (kHz)")
plt.ylabel("Power (dB)")
plt.title("Spectrum")
plt.show()

# plot the first 10000 samples of the time-domain audio signal
time_vec=n.arange(len(clip))/float(sr)
plt.title("Waveform")
plt.plot(time_vec[0:100000]*1e3,clip[0:100000],label="Original")
plt.plot(time_vec[0:100000]*1e3,compressed[0:100000],label="Compressed")
plt.legend()
plt.xlabel("Time (ms)")
plt.ylabel("Audio waveform")
plt.show()

# Save result as wav file so that we can easily listen to the audio
# quality after decompression of the compressed signal.

# scale numbers to 0..0.95 scale
compressed = 0.95*compressed/n.max(compressed)
print("Saving spectrally sparse signal to file compressed_signal.wav")
sw.write("compressed_signal.wav",44100,n.array(20e3*compressed,dtype=n.int16))
