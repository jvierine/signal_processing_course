import numpy as n
import matplotlib.pyplot as plt
# define the sample rate (Hz)
sample_rate=10000.0
# create time array 0 to 4 seconds
t=n.arange(4.0*sample_rate)/sample_rate
# initialize empty vector to hold Fourier series
sig=n.zeros(len(t),dtype=n.complex64)
N=50
T=0.5
for k in range(-N,N+1):
    sig+=(1.0/T)*n.exp(1j*(2.0*n.pi/T)*k*t)#...# complete this line
    
plt.plot(sig.real)
plt.plot(sig.imag)
plt.show()
