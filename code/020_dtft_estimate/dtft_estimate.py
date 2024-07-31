import matplotlib.pyplot as plt
import numpy as np


# Calculate the DTFT of signal x using zero-padded DFT
# at N evenly spaced points between -\pi and \pi.
def dft_dtft(x, N):
    # The N parameter determines the length of the DFT.
    # Is N > len(x), then the signal x is zero padded.
    X = np.fft.fft(x, N)
    # Normalized angular frequency step.
    dom = 2.0*np.pi/N
    # Normalized angular frequencies.
    om_dft = np.arange(N)*dom
    return (X, om_dft)


def he(om, L=20):
    # Analytic DTFT of a causal running average filter.
    return ((1.0/L)*(1 - np.exp(-1j*om*L))/(1 - np.exp(-1j*om)))


# Calculate using analytic formula the DTFT of the running average filter.
om = np.linspace(0, 2*np.pi, num=1000)

# DTFT of running average filter by evaluating using analytic formula
H = he(om, L=20)

# Signal (FIR filter coefficients).
x = np.repeat(1.0/20.0, 20)

X, om_dft = dft_dtft(x, 256)

# Zero padded signal.
x_zp = np.zeros(256)
x_zp[:20] = x
plt.stem(x_zp)
plt.show()

plt.figure(figsize=(6, 4))
plt.plot(om, np.abs(H), color="C0", label="Analytic")
plt.stem(om_dft, np.abs(X), linefmt="C1-", markerfmt="C1o", basefmt="C1", label="DFT")
plt.legend()
plt.title("N=256")
plt.xlabel(r"$\hat{\omega}$")
plt.ylabel(r"$|\mathcal{H}(\hat{\omega})|$")
plt.savefig("dtft_estimate.png")
plt.show()
