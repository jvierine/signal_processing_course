#!/usr/bin/env python
#
# Reverb effect for sound
#
import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile as sw
import scipy.signal as ss

# read audio file (wav format)
ts=sw.read("7na.wav")
sr=ts[0]     # sample rate
clip=ts[1]  # extract audio file as numpy data vector
if len(clip.shape)==2: # if stereo, only use one channel
    print("using only one stereo channel. read on")
    clip=ts[1][:,0]

# make sure the clip is float32
clip=n.array(clip[0:1000000],dtype=n.float32)

# fourier transform
# 0..2\pi -> -\pi .. to \pi
# add a tapering window
#w=ss.chebwin(len(clip),150.0)
#clip_f=n.fft.fftshift(n.fft.fft(w*clip))

fftlen=1024
n_window=int(n.floor((len(clip)-fftlen)/(fftlen/2.0)))
w=ss.hann(fftlen)
S=n.zeros([n_window,fftlen])
time_vec=n.zeros(n_window)
for i in range(n_window):
    S[i,:]=n.fft.fftshift(n.abs(n.fft.fft(w*clip[i*(int(fftlen/2))+n.arange(fftlen)]))**2.0)
    time_vec[i]=(i*fftlen/2.0)/sr
    
fvec=n.fft.fftshift(n.fft.fftfreq(fftlen,d=1.0/sr))

plt.pcolormesh(time_vec,fvec,n.transpose(10.0*n.log10(S)))
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.colorbar()
plt.show()

