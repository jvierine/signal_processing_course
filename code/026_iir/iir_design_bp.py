#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as n
import scipy.signal as s

import plot_h

def simple_hpf(signal):
    # Implement IIR filter:
    # y[n] = #-0.9*y[n-1] + x[n] - 0.5*y[n-1] + 1.08201933e-05*x[n] - 1.84771565e-05*x[n-1] + 1.08201933e-05*x[n-2]
    # y[n[ = 1.99837606*y[n-1] - 0.99838053*y[n-2] + 
    # y[n] = 
    out=n.zeros(len(signal))
    for i in range(len(signal)):
        if i > 2:
            out[i] = 1.9964457*out[i-1] - 0.996452*out[i-2] + 1.57633449e-06*signal[i] + 3.15266898e-06*signal[i-1] + 1.57633449e-06*signal[i-2]
#            out[i]=signal[i]-0.9*out[i-1]-0.5*signal[i-1]
    return(out)


# Design an IIR band-pass filter with:
# sample-rate = 1000 Hz
# pass band = 100 to 300 Hz
# maximum pass band ripple 1 dB
# minimum attenuation of signals out of band = 100 dB
sample_rate=25e6
zeros,poles,k=s.iirfilter(5,Wn=10e3, rp=3.0, rs=100, ftype='cheby1', btype="lowpass", output="zpk",fs=sample_rate)
b,a=s.iirfilter(5,Wn=10e3, rp=3.0, rs=100, ftype='cheby1', btype="lowpass", output="ba",fs=sample_rate)




print(b)
print(a)
print(poles)
# create a white noise signal
signal = n.random.randn(1000000)

# filter signal with the IIR filter specified with
# coefficients b and a
#filtered_signal=s.lfilter(b,a,signal)
filtered_signal = simple_hpf(signal)
plt.plot(filtered_signal)
plt.show()
# plot the power spectrum estimate
plt.psd(filtered_signal,NFFT=1024,Fs=sample_rate)
plt.savefig("ex_pdf_lp.png")
plt.show()

# Plot the system function and the magnitude response of the IIR filter.
plot_h.plot_hmag("ex_design_lp.png",zeros=zeros,poles=poles,vmin=-150,fs=sample_rate)
