import numpy as np
import matplotlib.pyplot as plt

# A sweep of -\pi to \pi in normalized angular frequency.
omhat = np.linspace(-np.pi, np.pi, num=500)
H = 0.5*np.exp(1j*omhat)-0.5*np.exp(-1j*omhat)

plt.figure(figsize=(0.7*6, 0.7*8))
plt.subplot(211)
plt.plot(omhat, np.abs(H))
plt.title("Magnitude response")
plt.ylabel(r"$|\\mathcal{H}(\hat{\omega})|$")
plt.xlabel(r"$\hat{\omega}$")
plt.subplot(212)
plt.title("Phase response")
plt.plot(omhat, np.angle(H))
plt.xlabel(r"$\hat{\omega}$")
plt.ylabel(r"$\\angle\\mathcal{H}(\hat{\omega})$")
plt.tight_layout()
plt.savefig("bpf_fresp.png")
plt.show()
