import numpy as n
import matplotlib.pyplot as plt
import scipy.signal as ss
import sys

# function to convert to dB
def convert_to_decibel(x):
    return 10*n.log10(n.abs(x)**2)

N = 16384
nn = n.arange(N)
freqs = [0.0003,0.012,0.055,0.102,0.85] # x1[n] frequencies
A = [1e5,5e5,1e3,1e4,0.5e4]             # x1[n] amplitudes
x1 = n.zeros(N)

# create the first signal
for i,f in enumerate(freqs):
    x1 += A[i]*n.cos(n.pi*freqs[i]*nn + n.random.randn(1))

# create the second signal (the weak signal)
x2 = n.zeros(N)
x2[int(N/2)] = 10.0
x2[int(N/2)+1000] = -5.0
x2[int(N/2)-1000] = 1.0

x = x1 + x2

w = ss.hann(N)  # Hann window to reduce spectral leakage

xw = n.fft.rfft(w*x,2*N)    # use FFT to compute the spectrum
om_freqs = n.linspace(0,n.pi,num=len(xw)) # partition the interval (0,pi)

# define a filter to reduce strong spectral components
h = n.ones(len(xw)) # initialize each entry to 1

# lower the strong spectral components
# look at the previous exercise output plot to determine the intervals
# alternatively, plot the spectrum with samples on x-axis instead of \hat{\omega}
h[0:1050] = 1.0/n.abs(xw[0:1050])
h[1500:1860] = 1.0/n.abs(xw[1500:1860])
h[13500:14200] = 1.0/n.abs(xw[13500:14200])

# plot the spectral power to compare the two signals
plt.plot(om_freqs,convert_to_decibel(xw),label="Original spectrum")
plt.plot(om_freqs,convert_to_decibel(xw*h),label="Windowed spectrum")
plt.xlabel("$\hat{\omega}$ (rad / sample)")
plt.ylabel("Power of spectrum (dB)")
plt.legend()
plt.savefig("../figures/spectral_pw.png")
if len(sys.argv) == 1:
    plt.show()

# finally, inverse DFT to obtain the filtered signal
filter_signal = n.fft.irfft(h*xw)
plt.plot(filter_signal)
plt.xlabel("Samples")
plt.title("Filtered signal")
plt.savefig("../figures/filtered_signal.png")
if len(sys.argv) == 1:
    plt.show()