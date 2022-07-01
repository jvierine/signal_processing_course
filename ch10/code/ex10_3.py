import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile as sw
import scipy.signal as ss
import sys

def reverb_model(room_length_std=30.0,  # room wall to wall distance standard deviation in meters
                 echo_magnitude=0.5,    # how much is reflected from a wall
                 n_echoes=10,           # number of echoes
                 n_walls=10,            # number of scattering surfaces 
                 sr=44100,              # sample-rate
                 c_sound=340.0):        # speed of sound (m/s)
    """
    Simplified model of the acoustics of a room.
    Model the reflections from reverbations between surfaces in a room.
    """
    echo_len = int(sr*2*room_length_std*n_echoes/c_sound)
    h = n.zeros(echo_len,dtype=n.float32)
    h[0] = 1.0

    for wi in range(n_walls):
        wall_dist = n.abs(n.random.randn(1)*room_length_std)
        for i in range(n_echoes):
            idx = int(sr*(i+1)*wall_dist/c_sound)
            if idx < echo_len:
                h[idx] = n.random.randn(1)*echo_magnitude**(i + 1.0)
    return h

# implements a simply running average filter
def average_running_filter(M):
    h = n.repeat(1/M,M) # M is the number of terms to average

    return h

# read audio file (wav format)
ts = sw.read("../../elysium.wav")
sr = ts[0]     # sample rate
clip = ts[1]   # extract audio file as numpy data vector
if len(clip.shape)==2: # if stereo, only use one channel
    print("using only one stereo channel. read on")
    clip = ts[1][:,0]

# make sure the clip is float32
clip = n.array(clip,dtype=n.float32)

# this is the impulse response that determines the
# acoustics of a room
h = reverb_model(room_length_std=15.0,n_walls=100,echo_magnitude=0.5)

# h = reverb_model(room_length_std=1000.0,n_walls=1,echo_magnitude=0.5,sr=44100,c_sound=343.0)
# ^implements h[n] = delta[n] + 0.5delta[n - n0]

# h = average_running_filter(100)
# ^average running filter using 100 terms

omhat = n.linspace(-n.pi,n.pi,num=10000)
H = n.zeros(len(omhat),dtype=n.complex64)
for i in range(len(h)):
    H += h[i]*n.exp(1j*omhat*float(i))

plt.plot(omhat,n.abs(H)**2.0)
if len(sys.argv) == 1:
    plt.show()

# plot the impulse response
# if the impulse response is short, use stem plot
# otherwise use normal plot (it is much faster)
time_vec = n.arange(len(h))/float(sr)

plt.xlim([-0.1*n.max(time_vec),1.1*n.max(time_vec)])
plt.title("Impulse response")
plt.xlabel("Time (s)")
plt.ylabel("h[n]")
plt.savefig("../figures/reverb_impulse.png") 
if len(sys.argv) == 1:
    plt.show() # <-- impulse response is plotted here

# plot the audio
time_vec = n.arange(len(clip))
tidx = n.arange(0,int(n.min([44100,len(clip)])))
plt.subplot(211)
plt.plot(time_vec[tidx],clip[tidx])
plt.title("Original audio")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# convolve the clip with the impulse response
# scipy.signal.convolve
echo_clip = ss.convolve(clip,h,mode="full") # <-- convolution happens here

# plot the audio
plt.subplot(212)
plt.title("Convolution output")
# scale numbers to 0..1 scale
plt.plot(time_vec[tidx],echo_clip[tidx])
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.tight_layout()
if len(sys.argv) == 1:
    plt.show()

# normalize to unity
echo_clip = echo_clip/(n.max(n.abs(echo_clip)))

print("Saving reverb.wav")
# save as .wav file with 44.1 kHz sample rate
sw.write("reverb.wav",44100,n.array(20e3*echo_clip,dtype=n.int16))