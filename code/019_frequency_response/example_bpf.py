import numpy as n
import matplotlib.pyplot as plt

# a sweep of -\pi to \pi in normalized angular frequency
omhat = n.linspace(-n.pi,n.pi,num=500)
H=0.5*n.exp(1j*omhat)-0.5*n.exp(-1j*omhat)

plt.figure(figsize=(0.7*6,0.7*8))
plt.subplot(211)
plt.plot(omhat,n.abs(H))
plt.title("Magnitude response")
plt.ylabel("$|\\mathcal{H}(\hat{\omega})|$")
plt.xlabel("$\hat{\omega}$")
plt.subplot(212)
plt.title("Phase response")
plt.plot(omhat,n.angle(H))
plt.xlabel("$\hat{\omega}$")
plt.ylabel("$\\angle\\mathcal{H}(\hat{\omega})$")
plt.tight_layout()
plt.savefig("bpf_fresp.png")
plt.show()
