import numpy as np
import matplotlib.pyplot as plt
import scipy.special as s


def frequency_response(h, n_value, omhat):
    H = np.zeros(len(omhat), dtype=np.complex64)
    for idx in range(len(h)):
        H += h[idx]*np.exp(-1j*n_value[idx]*omhat)
    return (H)


# Impulse response of an averaging filter.
# M = 2N + 1
h = np.repeat(1.0/21.0, 21)
print(len(h))
omhat = np.linspace(-np.pi, np.pi, num=1000)
# Integers -N to N.
H = frequency_response(h, np.arange(-10, 10+1), omhat)

# Alternative way using the dirichlet kernel:
# D_21(\omega)
D = s.diric(omhat, 21)

plt.figure(figsize=(0.8*6, 0.8*8))
plt.subplot(211)
plt.plot(omhat, np.abs(D))
plt.plot(omhat, np.abs(H))
plt.title("Magnitude response")
plt.ylabel(r"$|\\mathcal{H}(\hat{\omega})|$")
plt.xlabel(r"$\hat{\omega}$")
plt.subplot(212)
plt.title("Phase response")
plt.plot(omhat, np.angle(D))
plt.xlabel(r"$\hat{\omega}$")
plt.ylabel(r"$\\angle\\mathcal{H}(\hat{\omega})$")
plt.tight_layout()
plt.savefig("dirichlet21.png")
plt.show()
