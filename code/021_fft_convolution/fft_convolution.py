#
# Use of FFT to implement a linear convolution
# zero-padding used to avoid periodicity.
# 
import numpy as n
import matplotlib.pyplot as plt
import scipy.signal as s
# input signals to be convolved
a=n.arange(10)
b=n.ones(20)

# zero-padded FFT (10+20=30)
A=n.fft.fft(a,30)
B=n.fft.fft(b,30)
ab=n.fft.ifft(A*B)
# this function also does the same as the three lines above
# ab=s.fftconvolve(a,b)
plt.figure(figsize=(4,6))
plt.subplot(311)
plt.stem(a)
plt.ylim([0,12])
plt.xlim([0,30])
plt.title("$a[n]$")
plt.subplot(312)
plt.stem(b)
plt.ylim([0,1.2])
plt.xlim([0,30])
plt.title("$b[n]$")
plt.subplot(313)
plt.title("$a[n]*b[n]$")
plt.stem(ab)
plt.ylim([0,50])
plt.tight_layout()
plt.savefig("convolution.png")
plt.show()
