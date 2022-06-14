#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt

# random signal
x=n.random.randn(100000)

L=14
running_avg_h=n.repeat(1.0/float(L),L)

# Multiplication in frequency domain is convolution
# This evaluates the low pass filter using FFT:
x_lp=n.fft.irfft(n.fft.rfft(running_avg_h,len(x))*n.fft.rfft(x))

# between samples 40000 to 50000, add a sinusoidal signal with frequency 300 Hz
x[40000:50000]+=1000.0*n.cos(2.0*n.pi*300.0*n.arange(len(x[40000:50000]))/4096.0)

# between samples 40000 to 50000, add a sinusoidal signal with frequency 300 Hz
x[60000:70000]+=n.cos(2.0*n.pi*650.0*n.arange(len(x[60000:70000]))/4096.0)


plt.specgram(x,NFFT=1024,Fs=4096.0,scale="dB")
plt.colorbar()
plt.show()
