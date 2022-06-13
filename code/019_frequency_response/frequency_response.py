#!/usr/bin/env python


import numpy as n
import matplotlib.pyplot as plt
import scipy.special as s
def frequency_response(h,n_value,omhat):
    H=n.zeros(len(omhat),dtype=n.complex64)
    for idx in range(len(h)):
        H+=h[idx]*n.exp(-1j*n_value[idx]*omhat)
    return(H)
        
# impulse response of an averaging filter
# M = 2N+1
h=n.repeat(1.0/21.0, 21)
print(len(h))
omhat = n.linspace(-n.pi,n.pi,num=1000)
# integers -N to N
H=frequency_response(h,n.arange(-10,10+1),omhat)

# alternative way using the dirichlet kernel
# D_21(\omega)
D=s.diric(omhat,21)

plt.figure(figsize=(0.8*6,0.8*8))
plt.subplot(211)
plt.plot(omhat,D)
plt.plot(omhat,n.real(H))
plt.title("Magnitude response")
plt.ylabel("$|\\mathcal{H}(\hat{\omega})|$")
plt.xlabel("$\hat{\omega}$")
plt.subplot(212)
plt.title("Phase response")
plt.plot(omhat,n.angle(D))
plt.xlabel("$\hat{\omega}$")
plt.ylabel("$\\angle\\mathcal{H}(\hat{\omega})$")
plt.tight_layout()
plt.savefig("dirichlet21.png")
plt.show()
