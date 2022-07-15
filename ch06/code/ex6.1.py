import numpy as n
import matplotlib.pyplot as plt

N = 1000    # number of sample points
om = 2.6    # angular frequency
phi = 3.1   # phase
m = 0       # integer
# compute the phase needed to cancel the signal
phi_cancel = n.pi - phi + 2*n.pi*m    

# partition the t axis with a range 
# from 0 to 4pi with N samples
t = n.linspace(start=0, stop=4*n.pi,num=N)

# original signal
x = n.cos(om * t + phi)

# noise canceling signal
y = n.cos(om * t + phi_cancel)

# plot the signals
plt.plot(t,x)
plt.plot(t,y)
# call this if needed
# plt.show()