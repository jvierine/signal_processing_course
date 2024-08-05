import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(6*0.7, 4*0.7))

# Sample indices for 10000 samples.
m = np.arange(10000)

# Sample period.
Ts = 1e-4

# Create a signal consisting of three sinusoids.
x = np.cos(2.0*np.pi*4000.0*Ts*m) + 2*np.cos(2.0*np.pi*1000.0*Ts*m) + 3*np.cos(2.0*np.pi*2500.0*Ts*m)

# Plot the magnitude of sinusoids using fft.
plt.plot(np.abs(np.fft.fft(x))/len(m))
# Call this if needed.
# plt.show()

try:
    plt.tight_layout()
    plt.savefig("../figures/ex15_2.png")
except:
    print("couldn't save file")
