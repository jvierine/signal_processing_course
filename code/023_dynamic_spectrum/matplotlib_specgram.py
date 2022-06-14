#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt

# sample rate (Hz)
fs=4096.0

# sample indices (one second of signal)
nn=n.arange(4096)
# generate a chirp signal
x=n.sin(0.15e-14*nn**5.0)

# alternatively, you can use the matplotlib
# implementation
mspec,mfreq,mt,mim=plt.specgram(x,NFFT=128,pad_to=2000,noverlap=100,Fs=fs,scale="dB",vmin=-50,vmax=-20)
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.colorbar()
plt.show()
