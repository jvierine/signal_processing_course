#!/usr/bin/env python3

import numpy as n
import matplotlib.pyplot as plt




chirp=n.fromfile("chirp.bin",dtype=n.float32)
m=n.fromfile("sonar_meas.bin",dtype=n.float32)

interpulse_period=10000
N_ipps=int(n.floor(len(m)/interpulse_period))
P=n.zeros([N_ipps,interpulse_period])
deconvolution_filter=chirp[::-1]
for i in range(N_ipps):
    echo=m[(i*interpulse_period):(i*interpulse_period+interpulse_period)]
    deconvolved=n.convolve(echo,deconvolution_filter,mode="same")
    P[i,:]=n.abs(deconvolved)**2.0

group_velocity=343.0 # m/s
sample_rate=44.1e3
# a)
distance_per_sample = group_velocity/sample_rate
print("a) %1.2f (m)"%(distance_per_sample))
tx_pulse_length = 1000.0/sample_rate
print("b) %1.2f (s)"%(tx_pulse_length))
meas_length=len(m)/sample_rate
print("c) %1.2f (s)"%(meas_length))
print("d) %d (pulses)"%(N_ipps))
print("e) In order to deconvolve the transmit pulse from the impulse response of the room.")

acf=n.convolve(chirp,chirp[::-1])
print("f).")
plt.plot(acf)
plt.xlabel("Time (samples)")
plt.ylabel("$x[n]*x[-n-n_0]$")
plt.title("f) Autocorrelation function")
plt.xlim([975,1025])
plt.show()

print("g) Fairly close, but not exactly \delta[n]. There are significant non-zero values only up to +/- 3 samples around the peak of the autocorrelation function. This will affect the range resolution at which the measurement can be made, as ranges +/- 3 samples around a certain range will still be mixed up and seen as artefacts in the measurement. This is a smearing of echo power as a function of range over around 6 samples. This is still better than 1000 ranges being smeared together, which we would have without the deconvolution operation.")

print("h) plotting.")
total_range=group_velocity*n.arange(interpulse_period)/sample_rate
time=n.arange(N_ipps)*interpulse_period/sample_rate
    
plt.pcolormesh(time,total_range,10.0*n.log10(n.transpose(P)),vmin=-30,vmax=30)
plt.xlabel("Time (s)")
plt.ylabel("Total propagation distance (m)")
plt.title("g) Scattered power as a function of time and range")
plt.ylim([0,10])
cb=plt.colorbar()
cb.set_label("Scattered power (dB) arbitrary reference")
plt.show()
