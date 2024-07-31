import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as c

print("Hello World!")
# Test numpy and scipy.
print(np.pi)
print(c.pi)

sample_rate = 44100.0  # 44100 samples per second.
t = np.arange(100)/sample_rate
csin = np.exp(1j*2.0*np.pi*440.0*t)  # A 440 Hz signal.

plt.plot(t*1e3, csin.real, color="blue", label=r"$\mathrm{Re}\{z(t)\}$")
plt.plot(t*1e3, csin.imag, color="red", label=r"$\mathrm{Im}\{z(t)\}$")

plt.xlabel("Time (ms)")
plt.ylabel(r"$z(t)=e^{i\omega t}$")
plt.legend()
plt.show()
