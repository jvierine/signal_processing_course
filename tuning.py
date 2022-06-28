import numpy as np
import scipy.io.wavfile as sio
import matplotlib.pyplot as plt

def convert_to_decibel(x):
    return 10*np.log10(np.abs(x)**2)

sample_rate = 44100 # sample rate
f0 = 196            # Hz
f1 = 2*f0
f2 = 5*f0

N  = 10000

# create time vector (independent variable)
t = np.arange(0,10*np.pi,step=1/sample_rate)

# test signal
x = np.cos(2*np.pi*f0*t) + np.cos(2*np.pi*f1*t) + np.cos(2*np.pi*f2*t)

signal_freq = np.fft.fft(x)
freq = np.fft.fftfreq(len(t),d=1/sample_rate)
plt.plot(freq,convert_to_decibel(signal_freq))
plt.show()

# y = 2*np.real(y)
# z = np.cos(2*np.pi*f1*t)

x = 0.9*x/np.max(np.abs(x))
# y = 0.9*y/np.max(np.abs(y))
# z = 0.9*z/np.max(np.abs(z))

# write compressed output to wav file
sio.write("test.wav",sample_rate,np.array(x,dtype=np.float32))
#sio.write("new.wav" ,sample_rate,np.array(y,dtype=np.float32))
#sio.write("Asharp.wav",sample_rate,np.array(z,dtype=np.float32))