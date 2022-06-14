#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt

# frequency, in units of radians per sample
omhat = n.linspace(-n.pi,n.pi,num=100000)

# system function
def h(z):
    om0=2.0*n.pi*5000.0/(44.1e3)
    om1=2.0*n.pi*1500.0/(44.1e3)
    return(z**(-4)*( z**4 - 2*z**3*(n.cos(om1)+n.cos(om0))
                     + 2*z**2*(1+2*n.cos(om1)*n.cos(om0))
                     - 2*z*(n.cos(om0)+n.cos(om1)) + 1))

# magnitude response
magresp = n.abs(h(n.exp(1j*omhat)))
# plot the magnitude response in dB scale
plt.plot(omhat,10.0*n.log10(magresp**2.0))
plt.xlabel("Frequency $\hat{\omega}$ (rad/sample)")
plt.ylabel("Magnitude response $10\log_{10}(|\mathcal{H}(\hat{\omega})|^2)$ dB")
plt.show()
