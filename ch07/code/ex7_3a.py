import numpy as n
import matplotlib.pyplot as plt

T = 1                   # period
sample_rate = 1000.0    # sample rate
N = 101                 # number of terms 

# partition the t-axis
t = n.arange(int(sample_rate*T))/sample_rate

# allocate an array for the signal
xn = n.zeros(len(t),dtype=n.complex64)

# function for the Fourier coefficients
def ck(k):
    if k == 0:
        return 1/10
    else:
        return 1/(n.pi*k)*n.exp(-1j*n.pi*k/10)*n.sin(n.pi*k/10)

# loop through the indices and add the signal terms
for i in range(-N,N+1):
    xn += ck(i)*n.exp(1j*2*n.pi*i*t/T)

# plot the result
plt.plot(t,xn.real,color="blue")
plt.plot(t,xn.imag,color="red")
plt.xlabel("Time (t)")
plt.ylabel("$x_{N}(t)$")
# if needed
# plt.plot()