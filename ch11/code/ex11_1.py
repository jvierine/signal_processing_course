import numpy as n
import matplotlib.pyplot as plt
import sys

om = n.linspace(-7*n.pi,7*n.pi,num=1000)

def freq_resp(om):
    return 42*(n.heaviside(om+5.5*n.pi,0)-n.heaviside(om-5.5*n.pi,0))

plt.plot(om,n.abs(freq_resp(om)),color="green")
plt.vlines(-7*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(-6*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(-5*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(-4*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(-3*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(-2*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(-n.pi,ymin=0,ymax=42,color="red")
plt.vlines(0,ymin=0,ymax=42,color="red")
plt.vlines(n.pi,ymin=0,ymax=42,color="red")
plt.vlines(2*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(3*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(4*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(5*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(6*n.pi,ymin=0,ymax=42,color="red")
plt.vlines(7*n.pi,ymin=0,ymax=42,color="red")

plt.title("Dirac comb")
plt.xlabel("$\omega$")
plt.savefig("../figures/diractrain.png")

if len(sys.argv) == 1:
    plt.show()