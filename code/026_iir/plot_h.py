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

def plot_hmag(fname,poles,zeros,vmin=-50,vmax=10,fs=1000.0):
    xx=n.linspace(-3,3,num=1000)
    yy=n.linspace(-3,3,num=1000)
    x,y=n.meshgrid(xx,yy)

    fig, axs = plt.subplots(2,1,figsize=(4,6))#plt.subplot(121)

    # plot magnitude of system function
    pwr=n.abs(h(x+1j*y,poles=poles,zeros=zeros))**2.0
    pwr=pwr/n.nanmax(pwr)
    c=axs[0].pcolormesh(xx,yy,10.0*n.log10(pwr),vmin=vmin,vmax=vmax,cmap="jet")
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
    pwr=n.abs(h(n.exp(1j*om),poles=poles,zeros=zeros))**2.0
    pwr=pwr/n.nanmax(pwr)
    dB=10.0*n.log10(pwr)
    axs[1].plot(fs*om/n.pi/2.0,dB)
    axs[1].set_xlabel("Frequency (Hz)")
    axs[1].set_ylabel("|$\\mathcal{H}(f)|^2$ (dB)")
    axs[1].set_title("Magnitude response")
    axs[1].set_ylim([vmin,vmax])
    plt.tight_layout()
    plt.savefig(fname)
    plt.show()
