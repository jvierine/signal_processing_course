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
weak_signal[int(N/2)-1000]=1.0

x=strong_signal+weak_signal

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
plt.ylabel("$x[n]=x_1[n]+x_2[n]$")
plt.title("Total signal")
plt.tight_layout()
plt.savefig("filter_signals.png")
plt.show()

# windowed zero-padded DFT
w=s.hann(N)
WX=n.fft.rfft(w*x,2*N)

# create a filter than filters out strong spectral components the signal
WH=n.zeros(len(WX))
WH[:]=1.0 # pass all frequencies
WH[0:400]=1.0/n.abs(WX[0:400]) # attenuate strong frequencies
WH[1400:1800]=1.0/n.abs(WX[1400:1800])  # attenuate strong frequencies
WH[14000:15000]=1.0/n.abs(WX[14000:15000])  # attenuate strong frequencies

plt.semilogy(n.abs(WX),label="$|\hat{x}[k]|$")
plt.semilogy(n.abs(WX*WH),label="$|\hat{y}[k]|$")
plt.legend()
plt.title("Original and filtered spectrum")
plt.tight_layout()
plt.savefig("filter_spec.png")
plt.show()

# apply filter in frequency domain
wy=n.fft.irfft(WH*WX)[0:N]

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
plt.savefig("filter_filtered.png")
plt.show()
