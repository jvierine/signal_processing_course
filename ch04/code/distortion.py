import numpy as n
import scipy.io.wavfile as sio
import matplotlib.pyplot as plt

# amplifier gain
alpha=20.0

# the clipping amplitude of the amplifier
beta=0.9

# a function to compress signal x (signal processing system)
def comp(x,alpha=1.0,beta=1e3):
    return(n.sign(x)*n.minimum(n.abs(alpha*x),beta))

# read wav file (read only one stereo channel)
# download from: http://kaira.uit.no/fys2006/guitar_clean.wav
# Original author: LG downloaded from freesound.org,
# Original file name: Guitar clean rif.wav
wav=sio.read("7na.wav")
sample_rate=wav[0]
# read only one stereo channel
x=wav[1]
# scale to near unity
x=0.9*x/n.max(n.abs(x))

# create time vector (independent variable)
time_vec=n.arange(len(x))/float(sample_rate)

# plot original and compressed signal
plt.plot(time_vec,comp(x,alpha,beta),label="Compressed")
plt.plot(time_vec,x,label="Original")
plt.legend()
plt.xlabel("Time $t$")
plt.ylabel("Relative air pressure $y(t)$")
plt.show()

# filter the signal
out=comp(x,alpha,beta)

# scale maximum absolute amplitude to 0.9, because 1.0 is the maximum allowed
# by the file format
out=0.9*out/n.max(n.abs(out))

# write compressed output to wav file. 
sio.write("guitar_comp.wav",sample_rate,n.array(out,dtype=n.float32))

