import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hann

# Using windowed DFT for spectral analysis of signals. 
# Demonstrate that a window function allows weak 
# signals to be found better, due to less spectral 
# leakage than if a rectangular window is used.

N = 4096
n = np.arange(N)

freq1 = 0.01*np.pi
freq2 = 0.1*np.pi

# Strong low-frequency signal signal.
strong_signal = 1e6*np.cos(freq1*n)

# Weak signal at higher frequency.
weak_signal = np.cos(freq2*n)

y = strong_signal + weak_signal

plt.subplot(311)
plt.plot(n, strong_signal)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x_1[n]$")
plt.title(r"Strong signal $\hat{\omega}=%1.2f$" % (freq1))
plt.subplot(312)
plt.plot(n, weak_signal)
plt.xlabel("Sample ($n$)")
plt.ylabel("$x_2[n]$")
plt.title(r"Weak signal $\hat{\omega}=%1.2f$" % (freq2))
plt.subplot(313)
# Weak signal is impossible to see, 
# because it has a 1e6 smaller amplitude.
plt.plot(n, y)
plt.xlabel("Sample ($n$)")
plt.ylabel("$y[n]=x_1[n]+x_2[n]$")
plt.title("Total signal")
plt.tight_layout()
plt.savefig("windowed_signals.png")
plt.show()

# Analyze spectrum zero padded DFT to be of length 2*N.
Y = np.fft.fft(y, 2*N)
# Windowed zero-padded DFT.
w = hann(N)
# Zero padded DFT to be of length 2*N.
WY = np.fft.fft(w*y, 2*N)
# Frequencies in radians per sample.
om = np.fft.fftfreq(len(Y), d=1)*2.0*np.pi
# Reorder frequencies so that we go from -pi to pi instead of 0 to 2\pi.
om = np.fft.fftshift(om)
Y = np.fft.fftshift(Y)
WY = np.fft.fftshift(WY)

plt.plot(om, 10.0*np.log10(np.abs(Y)**2.0), label="DFT")
plt.plot(om, 10.0*np.log10(np.abs(WY)**2.0), label="Windowed DFT")
plt.ylabel("Spectral power (dB)")
plt.xlabel("Frequency (rad/s)")
plt.title("Power spectrum")
plt.legend()
plt.tight_layout()
plt.savefig("windowed_spec.png")
plt.show()
