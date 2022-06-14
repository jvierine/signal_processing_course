import matplotlib.pyplot as plt
import numpy as n
import scipy.signal as s

def simple_hpf(signal):
    # Implement IIR filter:
    # y[n] = -0.9*y[n-1] + x[n] - 0.5*x[n-1]
    out=n.zeros(len(signal))
    for i in range(len(signal)):
        if i > 1:
            out[i]=signal[i]-0.9*out[i-1]-0.5*signal[i-1]
    return(out)

# Implement this system function
#         1 - 0.5 z^{-1}
# H(z) =  --------------
#         1 + 0.9 z^{-1}
b=[1.0,-0.5]
a=[1,0.9] 

# create a white noise signal, which has a flat power
# spectrum
signal = n.random.randn(100000)

# filter the noise signal
iir_filtered=s.lfilter(b,a,signal)
# the same, but using a slower direct routine 
iir_filtered_slow=simple_hpf(signal)

sample_rate=1000.0
# plot the power spectrum estimate
plt.psd(iir_filtered,NFFT=1024,Fs=sample_rate)
plt.savefig("ex_psd_hpf.png")
plt.show()

