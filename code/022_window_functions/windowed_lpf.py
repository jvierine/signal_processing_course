#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt
import scipy.signal as s

# vector of frequencies
om=n.linspace(-n.pi,n.pi,num=1000)
# low pass filter cutoff frequency
omc=0.1*n.pi
# sample indices for filter impulse response
nn=n.arange(-100,100)

# Ideal low-pass filter impulse response with cutoff at omc
sinc=n.sin(omc*nn)/(n.pi*nn)
# Use L'Hopital's rule to determine value at nn=0
sinc[nn==0]=omc/n.pi

# window function
wf=n.zeros(len(nn))
# window function length
wl=100
# Hann window
W=s.hann(wl)
# Center window function around 0
wf[int(len(wf)/2)-int(wl/2)+n.arange(wl)]=W

# Use a zero-padded DFT to approximate the frequency response
# of the windowed low-pass filter
WX=n.fft.fftshift(n.fft.fft(wf*sinc,4096))
# vector of frequencies for DFT 
omw=n.linspace(-n.pi,n.pi,num=len(WX))

# Ideal frequency response (boxcar)
X=n.zeros(len(om))
X[:]=1e-120 # very small number to avoid taking a log of 0
X[n.abs(om)<omc]=1.0

# plot power spectral response in dB scale for
# ideal and windowed filters
plt.figure(figsize=(10,8))
plt.subplot(212)
plt.plot(om,10.0*n.log10(n.abs(X)**2.0),label="Ideal",color="blue")
plt.plot(omw,10.0*n.log10(n.abs(WX)**2.0),label="Windowed",color="green")
plt.ylim([-130,3])
plt.legend()
plt.xlabel("$\hat{\omega}$")
plt.ylabel("$10\log_{10}|H(\hat{\omega})|^2$")
plt.title("Magnitude response")

# plot the impulse response of ideal and windowed filter.
plt.subplot(211)
plt.stem(nn,sinc,"b",markerfmt="bo",label="Ideal")
plt.plot(nn,n.max(sinc)*wf,label="Window",color="green")
plt.stem(nn,wf*sinc,"g",markerfmt="go",label="Windowed")
plt.legend()
plt.xlabel("$n$")
plt.ylabel("$h[n]$")
plt.title("Impulse response")
plt.tight_layout()
plt.savefig("windowed_lpf.png")
plt.show()
