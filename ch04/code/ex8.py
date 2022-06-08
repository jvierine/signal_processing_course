import numpy as n
import scipy.io.wavfile as sio
import matplotlib.pyplot as plt

# amplifier gain
alpha = 10.0

# a function to compress signal x (signal processing system)
def amplify(x,alpha):
    return(alpha*x)

# read wav file (read only one stereo channel)
#
# guitar_clean.wav copyright
# Original author: LG downloaded from freesound.org,
# Original file name: Guitar clean rif.wav

# the read function returns two arguments, these being the sample rate and the actual data
wav = sio.read("guitar_clean.wav")  
# read only one stereo channel
sample_rate = wav[0]      
# returned is a 2-dimensional NumPy array corresponding to the left and right channel
x = wav[1][:,0]

# create time vector (independent variable)
time_vec = n.arange(len(x)) / float(sample_rate)

# plot original and amplified
plt.plot(time_vec,amplify(x,alpha),label="Amplified")
plt.plot(time_vec,x,label="Original")
plt.legend()
plt.xlabel("Time $t$")
plt.ylabel("Relative air pressure $y(t)$")
plt.show()

out = amplify(x,alpha)

# scale maximum absolute amplitude to 0.9, because 1.0 is the maximum allowed
# by the file format
out = 0.9*out / n.max(n.abs(out)) 
# write compressed output to wav file

# patch from Jostein and Adrian (cast to 32 bit float)
sio.write("guitar_amp.wav",sample_rate,n.array(out,dtype=n.float32))

