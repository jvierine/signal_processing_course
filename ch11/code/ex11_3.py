import numpy as n
import matplotlib.pyplot as plt

# plot in the principal spectrum (-pi,pi)
om = n.linspace(-n.pi,n.pi,num=1000)

# for simplicity take Ts as 1
Ts = 1

# definition of the frequency response function
def freq_resp(om):
    return 2/(Ts**2)*(n.cos(om)-1)

# plot the frequency response function over (-pi,pi)
plt.plot(om,n.abs(freq_resp(om)),label="$\mathcal{H}(\hat{\omega})$")
plt.legend()
# call this if needed
# plt.plot()

try:
    plt.savefig("../figures/freq13.png")
except:
    print("couldn't save file")