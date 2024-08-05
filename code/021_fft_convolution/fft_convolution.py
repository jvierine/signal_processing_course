# Use of FFT to implement a linear convolution
# zero-padding used to avoid periodicity.
import matplotlib.pyplot as plt
import numpy as np

# Input signals to be convolved.
a = np.flip(np.arange(10))
b = np.ones(20)

# Zero-padded FFT (10 + 20 = 30)
A = np.fft.fft(a, 30)
B = np.fft.fft(b, 30)
ab = np.fft.ifft(A*B)
# This function also does the same as the three lines
# above ab = s.fftconvolve(a,b)
plt.figure(figsize=(4, 6))
plt.subplot(311)
plt.stem(a)
plt.ylim([0, 12])
plt.xlim([0, 30])
plt.title("$a[n]$")
plt.subplot(312)
plt.stem(b)
plt.ylim([0, 1.2])
plt.xlim([0, 30])
plt.title("$b[n]$")
plt.subplot(313)
plt.title("$a[n]*b[n]$")
plt.stem(ab)
plt.ylim([0, 50])
plt.tight_layout()
plt.savefig("convolution.png")
plt.show()
