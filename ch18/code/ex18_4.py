import numpy as n
import matplotlib.pyplot as plt

# function to convert to dB
def convert_to_decibel(x):
    return 10*n.log10(n.abs(x)**2)

# partition the interval (-pi,pi)
om = n.linspace(-n.pi,n.pi,num=10000)

# definition of the system function, H(z):
def system_function(z):
    return (1 - n.exp(1j*100*n.pi/441)*z**(-1))*(1 - n.exp(-1j*100*n.pi/441)*z**(-1))*(1 - n.exp(20*1j*n.pi/441)*z**(-1))*(1 - n.exp(-20*1j*n.pi/441)*z**(-1))*z**4

# frequency response
def frequency_response(om):
    return system_function(n.exp(1j*om))

# plot the system function with the zeros marked
plt.plot(om,convert_to_decibel(frequency_response(om)),label="$\mathcal{H}(\hat{\omega})$")
plt.xlabel("$\hat{\omega}$ (rad / sample)")
plt.ylabel("$|\mathcal{H}(\hat{\omega})|$")
plt.title("Magnitude response plot")
plt.legend()
# call this if needed
# plt.show()

try:
    plt.savefig("../figures/mag2.png")
except:
    print("couldn't save file")