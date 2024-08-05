import matplotlib.pyplot as plt
import numpy as np

# Sample indices for 10000 samples.
m = np.arange(10000)

# Sample period.
Ts = 1e-4

# Create a signal consisting of three sinusoids.
x = np.cos(2*np.pi*4000.0*Ts*m) + 2*np.cos(2*np.pi*1000.0*Ts*m) + 3*np.cos(2*np.pi*2500.0*Ts*m)

# Call fftfreq to compute the frequencies in units of hertz.
# The function takes in the first argument, which is the length of the window and second argument for the stepsize (Ts),
# use fftshift to shift the frequencies to have zero in the middle; this includes both positive and negative frequencies.
freq = np.fft.fftshift(np.fft.fftfreq(len(m), d=Ts))

# Plot the magnitude of sinusoids using fft.
plt.plot(freq, np.abs(np.fft.fft(x))/len(m))
plt.xlabel("Frequency (Hz)")
# Call this if needed.
# plt.show()

try:
    plt.tight_layout()
    plt.savefig("../figures/ex15_c.png")
except:
    print("couldn't save file")
