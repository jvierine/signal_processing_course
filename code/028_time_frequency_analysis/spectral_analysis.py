#!/usr/bin/env python
#
# Guitar reverb effect
#
import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile as sw
import scipy.signal as s

# read audio file (wav format)
ts=sw.read("ts2.wav")

sr=ts[0]     # sample rate
clip=ts[1]  # extract audio file as numpy data vector
if len(clip.shape)==2: # if stereo, only use one channel
    print("using only one stereo channel. read on")
    clip=ts[1][:,0]

# make sure the clip is float32
clip=n.array(clip,dtype=n.float32)

N_fft=2048

M = 1000

# fftfreq gives frequency in Hz
# fftshift orders frequencies correctly
frequencies = n.fft.fftshift(n.fft.fftfreq(N_fft,d=1.0/sr))

N_time=1000
#N_time = int((len(clip)-N_fft)/M)-1
#print(N_time)
wfun=s.hann(N_fft)
S=n.zeros([N_fft,N_time],dtype=n.float32)

for i in range(N_time):
    signal = clip[(i*M):(i*M+N_fft)]
    S[:,i]=n.fft.fftshift(n.abs(n.fft.fft(wfun*signal))**2.0)

time_vector=n.arange(N_time)*M/sr

plt.pcolormesh(time_vector,frequencies,10.0*n.log10(S))
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
cb=plt.colorbar()
cb.set_label("Power (dB)")
plt.show()


    
