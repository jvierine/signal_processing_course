import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile as sw
import scipy.signal as ss

# function to convert to decibel
def convert_to_decibel(x):
    return 10*n.log10(n.abs(x)**2)

# read audio file (wav format)
ts = sw.read("test.wav")
sr = ts[0]        # sample rate
clip = ts[1]      # extract audio file as numpy data vector

if len(clip.shape)==2: # if stereo, only use one channel
    print("using only one stereo channel. read on")
    clip = ts[1][:,0]

# frequency range to filter out
# set these accordingly
f0 = 0
f1 = 1

# time-frequency uncertainty; to get the length of the filter
N = int(100.0*sr*(1.0/(f1 - f0)))

# initialize the impulse response as empty
h = n.zeros(N,dtype=n.float32)
res = n.zeros(len(clip),dtype=n.float32)

# implement the tapered impulse response here ...

# do some plotting of the impulse response
plt.subplot(121)
plt.plot(h)
plt.subplot(122)
plt.plot(n.fft.fftshift(n.fft.fftfreq(len(h),d=1.0/sr))/1e3,convert_to_decibel(h))
plt.show()

# apply the filter to the audio signal here ...

# normalize to unity
res = res/(n.max(n.abs(res)))

# plot the filtered signal and the frequency 
# domain representation of the signal
plt.plot(res)
plt.show()

plt.plot(n.fft.fftshift(n.fft.fftfreq(len(res),d=1.0/sr))/1e3,convert_to_decibel(res))
plt.show()

print("Saving filtered.wav")
# save as .wav file with 44.1 kHz sample rate
sw.write("filtered.wav",sr,n.array(res,dtype=n.float32))