import matplotlib.pyplot as plt
import numpy as np

# Frequency, in units of radians per sample.
omhat = np.linspace(-np.pi, np.pi, num=100000)

def h(z):
    # System function.
    om0 = 2.0*np.pi*5000.0/(44.1e3)
    om1 = 2.0*np.pi*1500.0/(44.1e3)
    return (z**(-4)*(z**4 - 2*z**3*(np.cos(om1)+np.cos(om0))
                     + 2*z**2*(1+2*np.cos(om1)*np.cos(om0))
                     - 2*z*(np.cos(om0)+np.cos(om1)) + 1))


# Magnitude response.
magresp = np.abs(h(np.exp(1j*omhat)))
# Plot the magnitude response in dB scale.
plt.plot(omhat, 10.0*np.log10(magresp**2.0))
plt.xlabel(r"Frequency $\hat{\omega}$ (rad/sample)")
plt.ylabel(r"Magnitude response $10\log_{10}(|\mathcal{H}(\hat{\omega})|^2)$ dB")
plt.show()
