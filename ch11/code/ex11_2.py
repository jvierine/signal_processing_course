import numpy as n
import matplotlib.pyplot as plt
import scipy.special as dd

# partition the interval (-pi,pi) into num points
om = n.linspace(-n.pi,n.pi,num=1000)

# use M = 11 for the Dirichlet kernel plot
M = 11

# plot the two functions in the same coordinate system
plt.plot(om,n.abs(dd.diric(om,n=M))**2,label="$|D_{11}(\hat{\omega})|^{2}$")
plt.plot(om,n.abs(n.exp(1j*om*(M-1)/2)*dd.diric(om,n=M))**2,label="$|H_{11}(\hat{\omega})|^{2}$")
plt.xlabel("$\hat{\omega}$")
plt.legend()
# call this if needed
# plt.plot()

try:
    plt.savefig("../figures/frequency_responses.png")
except:
    print("couldn't save file")