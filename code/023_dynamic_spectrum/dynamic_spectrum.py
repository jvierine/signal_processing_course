#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt
import scipy.signal as s

# create dynamic spectrum
def spectrogram(x,M=1024,N=128,delta_n=100):
    """
    x = signal
    M = FFT length
    N = window function length
    delta_n = step step
    """
    max_t=int(n.floor((len(x)-N)/delta_n))
    t=n.arange(max_t)
    X=n.zeros([max_t,M],dtype=n.complex64)
    w=s.hann(N)
    xin=n.zeros(N)
    for i in range(max_t):
        # zero padded windowed FFT
        xin[0:N]=x[i*delta_n+n.arange(N)]
        X[i,:]=n.fft.fft(w*xin,M)
    return(X)

# sample rate (Hz)
fs=4096.0

# sample indices (one second of signal)
nn=n.arange(4096)
# generate a chirp signal
x=n.sin(0.15e-14*nn**5.0)

# time step
delta_n=25
M=2048
# create dynamic spectrum.
S=spectrogram(x,M=M,N=128,delta_n=delta_n)
# frequencies
freqs=n.fft.fftfreq(2048,d=1.0/fs)
# times
time=delta_n*n.arange(S.shape[0])/fs



# plot signal
plt.figure(figsize=(12,10))
plt.subplot(211)
plt.plot(nn/fs,x)
plt.title("Signal $x[n]$")
plt.xlabel("Time (s)")
plt.ylabel("Signal amplitude")
plt.subplot(212)

plt.title("Spectrogram")
plt.pcolormesh(time,freqs[0:int(M/2)],n.transpose(10.0*n.log10(n.abs(S[:,0:int(M/2)])**2.0)),vmin=0)
plt.xlim([0,n.max(time)])
plt.ylim([0,fs/2.0])
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
cb=plt.colorbar(orientation="horizontal")
cb.set_label("dB")
plt.tight_layout()
plt.savefig("dynspec.png")
plt.show()

