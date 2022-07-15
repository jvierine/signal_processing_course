import numpy as n
import matplotlib.pyplot as plt

# partition the range (-pi,pi)
omhat = n.linspace(-n.pi,n.pi,num=100000)

# roots/poles of diagram a) and b)
alpha1 = (2*n.sqrt(2))**(-1) + (2*n.sqrt(2))**(-1)*1j
alpha2 = (2*n.sqrt(2))**(-1) - (2*n.sqrt(2))**(-1)*1j

# roots of diagram c)
beta1 = -(2*n.sqrt(2))**(-1) + (2*n.sqrt(2))**(-1)*1j
beta2 = -(2*n.sqrt(2))**(-1) - (2*n.sqrt(2))**(-1)*1j

# system functions
def Ha(z):
    return (z - 1)*(z - alpha1*z)*(z - alpha2)/(z**3)

def Hb(z):
    return (z)/(z - 1)*(z - alpha1)*(z - alpha2)

def Hc(z):
    return (z + 1)*(z - beta1)*(z - beta2)/(z**3)

# function to convert the system function to the magnitude response function
def magn_resp(func):
    function = n.abs(func(n.exp(1j*omhat)))
    return function

fig, axs = plt.subplots(3)
fig.suptitle("Magnitude response")
axs[0].plot(omhat,magn_resp(Ha),label="a)",color="blue")
axs[1].plot(omhat,magn_resp(Hb),label="b)",color="red")
axs[1].set_ylim(0,10)   # limit diagram b) as it is unstable
axs[2].plot(omhat,magn_resp(Hc),label="c)",color="orange")
fig.legend()

# set the labels
for i in range(len(axs)):
    axs[i].set_xlabel("$\hat{\omega}$")
    axs[i].set_ylabel("$|\mathcal{H}(\hat{\omega})|$")

plt.tight_layout()
# call this if needed
# plt.show()

try:
    plt.savefig("../figures/magn_resp_diag")
except:
    print("couldn't save file")