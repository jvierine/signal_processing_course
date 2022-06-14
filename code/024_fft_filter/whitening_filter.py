#
# Using DFT to create a filter that
# attenuate spectral components to allow 
# weak signals burried under the strong but
# spectrally narrow signals to be found.
#
import numpy as n
import matplotlib.pyplot as plt
import scipy.signal as s

N=4096*2*2
nn=n.arange(N)
freqs=[0.0012,0.0021,0.0032,0.1,0.9]
A=[1e5,0.5e5,1e3,1e4,0.5e4]
strong_signal=n.zeros(N)
for i,f in enumerate(freqs):
    strong_signal+=A[i]*n.cos(n.pi*freqs[i]*nn+n.random.randn(1))

# weak signal at the middle of the signal
weak_signal=n.zeros(N)
weak_signal[int(N/2)]=10.0
weak_signal[int(N/2)+1000]=-5.0
weak_signal[int(N/2)-1000]=2.0

# add noise
noise=n.random.randn(N)*0.2
x=strong_signal+weak_signal+noise

plt.subplot(311)
plt.plot(nn,strong_signal)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x_1[n]$")
plt.title("Strong signal")
plt.subplot(312)
plt.plot(nn,weak_signal)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x_2[n]$")
plt.title("Weak signal")
plt.subplot(313)
plt.plot(nn,x)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x[n]=x_1[n]+x_2[n]+\\xi[n]$")
plt.title("Total signal")
plt.tight_layout()
plt.savefig("whiten_signals.png")
plt.show()

# windowed zero-padded DFT
w=s.hann(N)
WX=n.fft.rfft(w*x,2*N)

# create a filter than sets filters all spectral components to unity magnitude
H=1.0/n.abs(WX)

plt.semilogy(n.abs(WX),label="$|\hat{x}[k]|$")
plt.semilogy(n.abs(H*WX),label="$|\hat{y}[k]|$")
plt.legend()
plt.xlabel("$k$")
plt.title("Spectra")
plt.tight_layout()
plt.savefig("whiten_spec.png")
plt.show()

# apply filter in frequency domain and
# IFFT the signal into time domain.
wy=n.fft.irfft(H*WX)[0:N]

# plot filtered signal and compare with original weak signal buried under
# stronger signals
plt.subplot(211)
plt.plot(nn,wy)
plt.title("Filtered signal")
plt.xlabel("$n$")
plt.ylabel("$y[n]$")

plt.subplot(212)
plt.plot(nn,weak_signal)
plt.title("Original weak signal")
plt.xlabel("$n$")
plt.ylabel("$x_2[n]$")
plt.tight_layout()
plt.savefig("whiten_filtered.png")
plt.show()
