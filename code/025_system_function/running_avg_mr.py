#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as n

# define system function
def h(z,N=5):
    M=2*N+1
    zeros=n.exp(1j*2.0*n.pi*n.arange(1,M)/M)
    H=1.0
    for i in range(len(zeros)):
        H=H*(1.0-zeros[i]*z**(-1))    
    return(z**(N)*H/M)

omhat=n.linspace(-n.pi,n.pi,num=1000)
H=h(n.exp(1j*omhat))

plt.figure(figsize=(5,5))
plt.subplot(211)
plt.plot(omhat,n.abs(H))
plt.ylabel("$|\\mathcal{H}(\\hat{\\omega})|$")
plt.xlabel("$\hat{\omega}$")
plt.subplot(212)
plt.plot(omhat,n.angle(H*n.exp(-1j*0.01)))
plt.ylabel("$\\angle \\mathcal{H}(\\hat{\\omega})$")
plt.xlabel("$\\hat{\\omega}$")
plt.tight_layout()
plt.savefig("rma_magresp.png")
plt.show()


xx=n.linspace(-3,3,num=1000)
yy=n.linspace(-3,3,num=1000)
x,y=n.meshgrid(xx,yy)

fig, axs = plt.subplots(2,1,figsize=(5,10))#plt.subplot(121)

# plot magnitude of system function

c=axs[0].pcolormesh(xx,yy,10.0*n.log10(n.abs(h(x+1j*y))**2.0),vmin=-50,vmax=20,cmap="jet")
fig.colorbar(c,ax=axs[0])
om=n.linspace(0,2.0*n.pi,num=1000)
axs[0].plot(n.cos(om),n.sin(om),color="white")
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

axs[1].set_title("$\\angle\\mathcal{H}(z)$  (rad)")

om=n.linspace(0,2.0*n.pi,num=1000)
axs[1].plot(n.cos(om),n.sin(om),color="white")
plt.tight_layout()
plt.savefig("z_mag_angle_rm.png")
plt.show()
