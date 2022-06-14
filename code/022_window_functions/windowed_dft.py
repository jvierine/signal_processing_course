import numpy as n
import matplotlib.pyplot as plt
import scipy.signal as s
# Using windowed DFT for spectral analysis of
#signals Demonstrate that a window function allows weak signals to be
#found better, due to less spectral leakage than if a rectangular
#window is used.  import numpy as n import matplotlib.pyplot as plt
#import scipy.signal as s from matplotlib import rc rc('text',
#usetex=True)

N=4096
# sample indices
nn=n.arange(N)

freq1=0.01*n.pi
freq2=0.1*n.pi

# strong low-frequency signal signal
strong_signal=1e6*n.cos(freq1*nn)

# weak signal at higher frequency
weak_signal=n.cos(freq2*nn)

# sum strong and weak signal together
y=strong_signal+weak_signal

# plot signals
plt.subplot(311)
plt.plot(nn,strong_signal)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x_1[n]$")
plt.title("Strong signal $\hat{\omega}=%1.2f$"%(freq1))
plt.subplot(312)
plt.plot(nn,weak_signal)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x_2[n]$")
plt.title("Weak signal $\hat{\omega}=%1.2f$"%(freq2))
plt.subplot(313)
# weak signal is impossible to see, because it has a 1e6 smaller amplitude
plt.plot(nn,y)
plt.xlabel("Sample ($n$)")
plt.ylabel("$y[n]=x_1[n]+x_2[n]$")
plt.title("Total signal")
plt.tight_layout()
plt.savefig("windowed_signals.png")
plt.show()

# analyze spectrum
# zero padded DFT to be of length 2*N
Y=n.fft.fft(y,2*N)
# windowed zero-padded DFT
w=s.hann(N)
# zero padded DFT to be of length 2*N
WY=n.fft.fft(w*y,2*N)
# frequencies in radians per sample
om=n.fft.fftfreq(len(Y),d=1)*2.0*n.pi
# reorder frequencies so that we go from -pi to pi instead of 0 to 2\pi
om=n.fft.fftshift(om)
Y=n.fft.fftshift(Y)
WY=n.fft.fftshift(WY)

plt.plot(om,10.0*n.log10(n.abs(Y)**2.0),label="DFT")
plt.plot(om,10.0*n.log10(n.abs(WY)**2.0),label="Windowed DFT")
plt.ylabel("Spectral power (dB)")
plt.xlabel("Frequency (rad/s)")
plt.title("Power spectrum")
plt.legend()
plt.tight_layout()
plt.savefig("windowed_spec.png")
plt.show()
