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

def plot_hmag(fname,poles,zeros):
    xx=n.linspace(-3,3,num=1000)
    yy=n.linspace(-3,3,num=1000)
    x,y=n.meshgrid(xx,yy)

    fig, axs = plt.subplots(2,1,figsize=(4,6))#plt.subplot(121)

    # plot magnitude of system function
    c=axs[0].pcolormesh(xx,yy,10.0*n.log10(n.abs(h(x+1j*y,poles=poles,zeros=zeros))**2.0),vmin=-20,vmax=20,cmap="jet")
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
    om=n.linspace(-n.pi,n.pi,num=1000)
    axs[1].plot(om,n.abs(h(n.exp(1j*om),poles=poles,zeros=zeros)))
    axs[1].set_xlabel("$\\hat{\\omega}$")
    axs[1].set_ylabel("|$\\mathcal{H}(\\hat{\\omega})|$")
    axs[1].set_title("Magnitude response")
    plt.tight_layout()
    plt.savefig(fname)
    plt.show()

plot_hmag("ex8.png",poles=[0.98*n.exp(1j*0.8*n.pi),0.98*n.exp(-1j*0.8*n.pi)],zeros=[1,1j,-1j,-1])
plot_hmag("ex7.png",poles=[0.95*n.exp(1j*0.5*n.pi/2.0)],zeros=[0.0,1,-1,1j,-1j])
plot_hmag("ex6.png",poles=[0.95*n.exp(1j*0.5*n.pi/2.0),0.95*n.exp(-1j*0.5*n.pi/2.0)],zeros=[0.0,1,-1,1j,-1j])

plot_hmag("ex5.png",poles=[0.95*n.exp(1j*n.pi/2.0),0.95*n.exp(-1j*n.pi/2.0)],zeros=[-1,0.5j+0.5,-0.5j+0.5,0.5j-0.5,-0.5j-0.5,1])

plot_hmag("ex4.png",poles=[0.95],zeros=[-1])

plot_hmag("ex3.png",poles=[0.5j,-0.5j],zeros=[1,-1])
plot_hmag("ex1.png",poles=[0.5,-0.5],zeros=[1j,-1j])
plot_hmag("ex2.png",poles=[0.5],zeros=[1j,-1j])

