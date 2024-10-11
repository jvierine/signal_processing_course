#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt

# how many samples are there between transmit pulse leading edges
interpulse_period=10000
# how many samples long is the transmit pulse
pulse_length=1000
# what is the sample rate
sr=44100.0

# how many seconds long is the transmit pulse
dt=float(pulse_length)/sr

# time vector in seconds
tm=n.arange(pulse_length)#/sr

tmr=-1*n.arange(pulse_length)[::-1]#/sr
Ts=1/sr

#t = n*Ts

# pulse and silence after pulse
chirp_ipp=n.zeros(interpulse_period,dtype=n.float32)

m = n.arange(pulse_length)

# chirp rate = (22.1/dt) kHz/s
chirp=n.array(0.8*(n.sin(n.pi*m/pulse_length)**2.0)*n.sin(n.mod(2.0*n.pi*(0.5*22.05e3/dt)*(tm*Ts)**2.0,2.0*n.pi)),dtype=n.float32)

deco=n.array(0.8*(n.sin(-n.pi*m/pulse_length)**2.0)*n.sin(n.mod(2.0*n.pi*(0.5*22.05e3/dt)*(tmr*Ts)**2.0,2.0*n.pi)),dtype=n.float32)

chirp_ipp[0:pulse_length]=chirp
plt.plot(chirp)
plt.xlabel("Time (samples)")
plt.ylabel("Transmit pulse amplitude $x[n]$")
plt.show()
plt.plot(chirp_ipp)
plt.xlabel("Time (samples)")
plt.ylabel("Transmit pulse amplitude $x[n]$")
plt.show()

# plot the autocorrelation function
acf=n.convolve(chirp,chirp[::-1])
acft=n.arange(len(acf)) - len(acf)/2.0
plt.plot(acft,acf,label="$x[n]*x[-n]$")
plt.xlim([-50,50])
plt.xlabel("Time (samples)")
plt.ylabel("Autocorrelation function ($x[n]*x[-n]$)")
plt.show()

chirp.tofile("chirp.bin")
chirp_ipp.tofile("chirp_ipp.bin")
