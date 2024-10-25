import numpy as n
import matplotlib.pyplot as plt

#
# Causal running average filter frequency response and
# power spectral response
#

# solution strategy 1, brute force
#
# calculate frequency response for some value of L

# sample-rate (sample/s)
f_s=4096.0
# sample duration (s/sample)
T_s=1.0/f_s

# sweep of discrete-time normalized frequencies (radians/sample)
omhat = n.linspace(-n.pi,n.pi,num=10000)
# convert radian/sample frequency to 1/s (i.e., hertz) frequency
f_hertz = omhat/(2.0*n.pi*T_s)

# calculate frequency response
N_freqs=len(omhat)
# frequency response 
freq_resp = n.zeros(N_freqs,dtype=n.complex64)

# let's use
# L is length of filter
L=16
for k in range(0,L):
    print(k)
    freq_resp = freq_resp + (1.0/L)*n.exp(-1j*omhat*k)

# plot frequency response in power with decibel scale
P_dB=10.0*n.log10(n.abs(freq_resp)**2.0)


# closed form solution
P_dB2 = 10.0*n.log10(n.abs( (1.0/L)*(1-n.exp(-1j*omhat*L))/(1-n.exp(-1j*omhat)) )**2.0)

plt.plot(f_hertz,P_dB)
plt.plot(f_hertz,P_dB2)
# annotate the 300 Hz point on the x-axis
plt.axvline(300.0,color="red")
# annotate the -6 dB point on the y-axis
plt.axhline(-6,color="red")

# label axes
plt.xlabel("Frequency (hertz)")
plt.ylabel("Power (dB)")
plt.title("Power spectral response of the running average filter with $L=%d$"%(L))
plt.show()
