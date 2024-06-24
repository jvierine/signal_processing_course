import numpy as np
import matplotlib.pyplot as plt

T = 1                   # Period.
sample_rate = 1000.0    # Sample rate.
N = 101                 # Number of terms.
tau = 0.0               # Delay.

# Partition the t-axis.
t = np.arange(int(sample_rate*T))/sample_rate

# Allocate an array for the signal.
xn = np.zeros(len(t), dtype=np.complex64)


def ck(k: int) -> float:
    """Function for the Fourier coefficients."""
    if k == 0:
        return 1/10
    else:
        return 1/(np.pi*k)*np.exp(-1j*np.pi*k/10)*np.sin(np.pi*k/10)


# Derivative signal.
for i in range(-N, N+1):
    xn += (1j*2*np.pi*i/T)*ck(i)*np.exp(1j*2*np.pi*i*(t-tau)/T)

# Plot the result.
plt.plot(t, xn.real, color="blue")
plt.plot(t, xn.imag, color="red")
plt.xlabel("Time (t)")
plt.ylabel("$y_{N}(t)$")
# If needed.
# plt.plot()
