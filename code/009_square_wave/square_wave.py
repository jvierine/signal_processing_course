import matplotlib.pyplot as plt
import numpy as np

P = 0.1
T = 1.0

sample_rate = 1000.0
t = np.arange(int(sample_rate*T))/sample_rate

zn = np.zeros(len(t), dtype=np.complex64)

N = 101

ks = np.arange(-N, N+1)
cks = np.zeros(2*N+1, dtype=np.complex64)
ki = 0

for k in range(-N, N+1):
    if k == 0:
        zn += P/T
        cks[ki] = P/T
    else:
        k2 = float(k)
        ck = (1.0/(np.pi*k2))*(np.exp(-1j*(np.pi/T)*k2*P))*np.sin(np.pi*k2*P/T)
        cks[ki] = ck
        zn += ck*np.exp(1j*(2.0*np.pi/T)*k2*t)
    ki += 1

# Plot the absolute values of the Fourier series coefficients.
plt.plot(2.0*np.pi*ks/T, np.abs(cks))
plt.show()

# Create a square wave signal.
square_wave = np.zeros(len(t), dtype=np.float64)
square_wave[(0 < t) & (t < P)] = 1.0

plt.figure(figsize=(0.8*6, 0.8*4))
plt.plot(t, square_wave, label="Square wave", color="black")
plt.plot(t, zn.real, label="Fourier series approximation (Real)", color="blue")
plt.plot(t, zn.imag, label="Fourier series approximation (Imag)", color="red")
plt.legend()
plt.xlabel("Time (t)")
plt.ylabel("s(t)")
plt.tight_layout()
plt.savefig("square_wave.png")
plt.show()
