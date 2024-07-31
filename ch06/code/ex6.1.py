import matplotlib.pyplot as plt
import numpy as np

N = 1000    # Number of sample points.
om = 2.6    # Angular frequency.
phi = 3.1   # Phase.
m = 0       # Integer.
# Compute the phase needed to cancel the signal.
phi_cancel = np.pi - phi + 2*np.pi*m

# Partition the t axis with a range from
# 0 to 4pi with N samples.
t = np.linspace(start=0, stop=4*np.pi, num=N)

# Original signal.
x = np.cos(om * t + phi)

# Noise canceling signal.
y = np.cos(om * t + phi_cancel)

plt.plot(t, x)
plt.plot(t, y)
# Call this if needed.
# plt.show()
