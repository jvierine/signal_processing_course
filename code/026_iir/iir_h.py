#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as n

# define system function
def h(z,poles=[-0.9],zeros=[0.5]):
    H=1.0
    for i in range(len(poles)):
        H=H/(z-poles[i])
    for i in range(len(zeros)):
        H=H*(z-zeros[i])
    return(H)

xx=n.linspace(-3,3,num=1000)
yy=n.linspace(-3,3,num=1000)
x,y=n.meshgrid(xx,yy)

fig, axs = plt.subplots(2,1,figsize=(3,6))#plt.subplot(121)

poles=[-0.9]
zeros=[0.5]
# plot magnitude of system function
c=axs[0].pcolormesh(xx,yy,10.0*n.log10(n.abs(h(x+1j*y))**2.0),vmin=-20,vmax=20,cmap="jet")
fig.colorbar(c,ax=axs[0])
om=n.linspace(0,2.0*n.pi,num=1000)
axs[0].plot(n.cos(om),n.sin(om),color="black",zorder=1)

axs[0].scatter(n.real(poles),n.imag(poles),facecolors='white',marker='x',edgecolors='white',s=80,zorder=2)
axs[0].scatter(n.real(zeros),n.imag(zeros),facecolors='none',marker='o',edgecolors='white',s=80,zorder=2)
    

axs[0].set_aspect('equal')
axs[0].set_ylabel("Imaginary part of z")
axs[0].set_xlabel("Real part of z")
axs[0].set_xlim([-1.5,1.5])
axs[0].set_ylim([-1.5,1.5])
axs[0].set_title("$|\\mathcal{H}(z)|^2$ (dB)")

# plot phase angle of system function
c=axs[1].pcolormesh(xx,yy,n.angle(h(x+1j*y)),cmap="jet")
fig.colorbar(c,ax=axs[1])
axs[1].set_aspect('equal')
axs[1].set_ylabel("Imaginary part of z")
axs[1].set_xlabel("Real part of z")
axs[1].set_xlim([-1.5,1.5])
axs[1].set_ylim([-1.5,1.5])

om=n.linspace(-n.pi,n.pi,num=1000)
axs[1].plot(n.cos(om),n.sin(om),color="black",zorder=1)

axs[1].set_title("$\\angle\\mathcal{H}(z)$")
axs[1].scatter(n.real(poles),n.imag(poles),facecolors='white',marker='x',edgecolors='white',s=80,zorder=2)
axs[1].scatter(n.real(zeros),n.imag(zeros),facecolors='none',marker='o',edgecolors='white',s=80,zorder=2)

plt.tight_layout()
plt.savefig("z_mag_angle_iir.png")
plt.show()

plt.figure(figsize=(3,6))
plt.subplot(211)

plt.plot(om,n.abs(h(n.exp(1j*om),poles=poles,zeros=zeros)))
plt.title("Magnitude response")
plt.xlabel("$\\hat{\\omega}$")
plt.ylabel("|$\\mathcal{H}(\\hat{\\omega})|$")
plt.subplot(212)
plt.plot(om,n.angle(h(n.exp(1j*om),poles=poles,zeros=zeros)))
plt.title("Phase response")
plt.xlabel("$\\hat{\\omega}$")
plt.ylabel("$\\angle\\mathcal{H}(\\hat{\\omega})$")
plt.tight_layout()
plt.savefig("z_mag_angle_iir2.png")
plt.show()
