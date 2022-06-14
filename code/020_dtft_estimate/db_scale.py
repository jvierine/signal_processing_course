import numpy as n
import matplotlib.pyplot as plt

# Calculate the DTFT of signal x using zero-padded FFT
# at N evenly spaced points between -\pi and \pi
def dft_dtft(x,N,sample_rate=1e3):
    # fftshift shifts the frequencies so that we obtain
    # normalized angular frequency between -\pi to \pi
    # instead of 0 to 2\pi.
    X=n.fft.fftshift(n.fft.fft(x,N))
    # normalized angular frequency step
    dom=2.0*n.pi/N
    # normalized angular frequencies
    freqs=n.fft.fftshift(n.fft.fftfreq(N,d=1.0/sample_rate))
    return(X,freqs)

# signal (FIR filter coefficients)
h=n.repeat(1.0/100.0,100)
sample_rate=10e3
H,freqs=dft_dtft(h,501,sample_rate)

plt.figure(figsize=(6,6))
plt.subplot(211)
plt.plot(freqs/1e3,n.abs(H)**2.0)
plt.title("Linear scale")
plt.ylabel("$|\mathcal{H}(\hat{\omega})|^2$")
plt.xlabel("Frequency (kHz)")
plt.subplot(212)
plt.plot(freqs/1e3,10.0*n.log10(n.abs(H)**2.0))
plt.title("Decibel scale")
plt.ylabel("$10 \log_{10}|\mathcal{H}(\hat{\omega})|^2$")
plt.xlabel("Frequency (kHz)")
plt.tight_layout()
plt.savefig("db_scale.png")
plt.show()
