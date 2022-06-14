import numpy as n
import matplotlib.pyplot as plt

# Calculate the DTFT of signal x using zero-padded DFT
# at N evenly spaced points between -\pi and \pi
def dft_dtft(x,N):
    # the N parameter determines the length of the DFT
    # is N > len(x), then the signal x is zero padded
    X=n.fft.fft(x,N)
    # normalized angular frequency step
    dom=2.0*n.pi/N
    # normalizyed angular frequencies
    om_dft=n.arange(N)*dom
    return(X,om_dft)

# analytic DTFT of a causal running average filter
def he(om,L=20):
    return((1.0/L)*(1-n.exp(-1j*om*L))/(1-n.exp(-1j*om)))

# calculate using analytic formula the DTFT of the running average filter
om=n.linspace(0,2*n.pi,num=1000)

# DTFT of running average filter by evaluating using analytic formula
H=he(om,L=20)

# signal (FIR filter coefficients)
x=n.repeat(1.0/20.0,20)

X,om_dft=dft_dtft(x,256)

# zero padded signal
x_zp=n.zeros(256)
x_zp[0:20]=x
plt.stem(x_zp)
plt.show()

plt.figure(figsize=(6,4))
plt.plot(om,n.abs(H),color="C0",label="Analytic")
plt.stem(om_dft,n.abs(X),linefmt="C1-",markerfmt="C1o",basefmt="C1",label="DFT")
plt.legend()
plt.title("N=256")
plt.xlabel("$\hat{\omega}$")
plt.ylabel("$|\mathcal{H}(\hat{\omega})|$")
plt.savefig("dtft_estimate.png")
plt.show()
