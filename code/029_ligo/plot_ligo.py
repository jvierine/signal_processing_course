import h5py
import matplotlib.pyplot as plt
from os.path import dirname, join
import numpy as n
import scipy.signal.windows as s

path = dirname(__file__)

def read_data(fname):
    h=h5py.File(fname,"r")
    detector_name=h["meta/Detector"][()]
    start_time = h["meta/UTCstart"][()]
    strain=h["strain/Strain"][()]
    print("Reading %s data starting at %s"%(str(detector_name),str(start_time)))
    h.close()
    return(detector_name,start_time,strain)

# read hanford measurement
h1_name,h1_start_time,h1_strain=read_data(join(path, "H-H1_LOSC_4_V2-1126259446-32.hdf5"))

# read livingston measurement
l1_name,l1_start_time,l1_strain=read_data(join(path, "L-L1_LOSC_4_V2-1126259446-32.hdf5"))

# Here is some example code that you might find useful
# 
# Plot the amplitude of the Hanford and Livingston data.
# The variable t contains the time of each sample
# Ts=1/4096.0
# t=n.arange(len(h1_strain))*Ts
# plt.plot(t,h1_strain)
# plt.plot(t,l1_strain)
# plt.show()

# This example code snippet calculates a Hann windowed FFT of the Hanford data.
# fftshift is also used here to correct the frequency range to be 
# between -pi..pi (rad/sample) instead of 0..2pi (rad/sample) as it comes out of numpy.fft.fft
# 
# x_hat= n.fft.fftshift(n.fft.fft(s.hann(len(h1_strain))*h1_strain))
# 
# Plot power in units of decibel. Note that you will need to figure out how to 
# add the correct frequency to the plot. 
# plt.plot(10.0*n.log10(n.abs(x_hat)**2.0))
# plt.show()
#
