import numpy as n
import scipy.io.wavfile as sio
import matplotlib.pyplot as plt

# read wav file (read only one stereo channel)
wav=sio.read("guitar_clean.wav")
#wav=sio.read("7na.wav")
sample_rate=wav[0]
# read only one stereo channel

# mono audio
if len(wav[1].shape) == 1:
    print("Mono audio")
    x=wav[1][:]
else:
    print("Stereo audio is converted to mono audio.")    
    # stereo to mono conversion
    x=0.5*(wav[1][:,0]+wav[1][:,1])

    
# scale to near unity
x=0.9*x/n.max(n.abs(x))

# create time vector (independent variable)
time_vec=n.arange(len(x))/float(sample_rate)

# plot original and compressed signal
#plt.plot(time_vec,comp(x),label="Compressed")
plt.plot(time_vec,x,label="Original")
plt.legend()
plt.xlabel("Time t (seconds)")
plt.ylabel("Relative sound pressure $y(t)$")
plt.savefig("guitar_mod.png")
plt.show()

# multiply with sinusoid
x_mod=x*n.cos(2.0*n.pi*time_vec*5.0)

plt.plot(time_vec,x_mod)
plt.title("5 Hz modulation")
plt.show()
# write compressed output to wav file. 
sio.write("guitar_mod_5Hz.wav",sample_rate,n.array(x_mod,dtype=n.float32))

# multiply with sinusoid of 2.5 Hz
x_mod3=x*n.cos(2.0*n.pi*time_vec*2.5)
plt.plot(time_vec,x_mod3)
plt.title("2.5 Hz modulation")
plt.show()

# write compressed output to wav file. 
sio.write("guitar_mod_2.5Hz.wav",sample_rate,n.array(x_mod3,dtype=n.float32))


# listen to guitar_comp.wav and guitar_clean.wav and compare.
