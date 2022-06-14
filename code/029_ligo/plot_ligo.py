import h5py
import matplotlib.pyplot as plt
from os.path import dirname, join
import numpy as n
import scipy.signal as s

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
    
#plt.plot(h1_strain)
#plt.plot(l1_strain)
#plt.show()

# zero-padded FFT or DFT
x_hat= n.fft.fftshift(n.fft.fft(s.hann(len(h1_strain))*h1_strain))

plt.plot(10.0*n.log10(n.abs(x_hat)**2.0))
plt.show()
