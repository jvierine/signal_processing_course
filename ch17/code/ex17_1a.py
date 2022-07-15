import numpy as n
import matplotlib.pyplot as plt
import scipy.signal as ss

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

plt.plot(om_freqs,convert_to_decibel(xw))
plt.xlabel("$\hat{\omega}$ (rad / sample)")
plt.ylabel("$|\hat{x}_{w}[k]|^{2}$ (dB)")
plt.title("Spectrum of $x[n]$")
# call this if needed
# plt.show()

try:
    plt.savefig("../figures/ex17_1a.png")
except:
    print("couldn't save file")