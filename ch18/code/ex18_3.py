import numpy as n
import matplotlib.pyplot as plt

# partition the interval (-pi,pi)
om = n.linspace(-n.pi,n.pi,num=100)

# definition of the system function, H(z):
def system_function(z):
    return (1 - n.exp(1j*n.pi/4)*z**(-1))*(1 - n.exp(-1j*n.pi)*z**(-1))

# frequency response
def frequency_response(om):
    return system_function(n.exp(1j*om))

# marking the zeros on the graph
x_markers = [n.pi/4,-n.pi]
y_markers = [n.abs(frequency_response(n.pi/4)),n.abs(frequency_response(-n.pi))]

# plot the system function with the zeros marked
plt.plot(om,n.abs(frequency_response(om)))
plt.plot(x_markers,y_markers,'rx',label="zeros")
plt.xlabel("$\hat{\omega}$ (rad / sample)")
plt.ylabel("$|\mathcal{H}(\hat{\omega})|$")
plt.title("Magnitude response plot")
plt.legend()
# call this if needed
# plt.show()

try:
    plt.savefig("../figures/magnituderes.png")
except:
    print("couldn't save file")