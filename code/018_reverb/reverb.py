# Reverb effect for sound
#
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as sw
import scipy.signal as ss


def reverb_model(room_length_std=30.0,  # Room wall to wall distance standard deviation in meters.
                 echo_magnitude=0.5,    # How much is reflected from a wall.
                 n_echoes=10,           # Number of echoes.
                 n_walls=10,            # Number of scattering surfaces.
                 sr=44100,              # Sample-rate.
                 c_sound=340.0):        # Speed of sound (m/s).
    """
    Simplified model of the acoustics of a room.
    Model the reflections from reverberations between surfaces in a room.
    """
    echo_len = int(sr*2*room_length_std*n_echoes/c_sound)
    h = np.zeros(echo_len, dtype=np.float32)
    h[0] = 1.0

    for _ in range(n_walls):
        wall_dist = np.abs(np.random.rand()*room_length_std)
        for i in range(n_echoes):
            idx = int(sr*(i+1)*wall_dist/c_sound)
            if idx < echo_len:
                h[idx] = np.random.rand()*echo_magnitude**(i+1.0)

    return h


# Read audio file (.wav format).
ts = sw.read("7na.wav")
sr, clip = ts
if len(clip.shape) == 2:  # If stereo, only use one channel.
    print("Using only one stereo channel. Read on.")
    clip = clip[:, 0]

# Make sure the clip is float32.
clip = np.array(clip, dtype=np.float32)

# This is the impulse response that determines 
# the acoustics of a room.
h = reverb_model(room_length_std=15.0, n_walls=100, echo_magnitude=0.5)


omhat = np.linspace(-np.pi, np.pi, num=10000)
H = np.zeros(len(omhat), dtype=np.complex64)

for i in range(len(h)):
    H += h[i]*np.exp(1j*omhat*i)

plt.plot(omhat, np.abs(H)**2.0)
plt.show()


# Plot the impulse response
# if the impulse response is short, use stem plot
# otherwise use normal plot (it is much faster).
time_vec = np.arange(len(h))/float(sr)

if len(h) < 100:
    plt.stem(time_vec, h)
else:
    plt.plot(time_vec, h)

plt.xlim([-0.1*np.max(time_vec), 1.1*np.max(time_vec)])
plt.title("Impulse response")
plt.xlabel("Time (s)")
plt.ylabel("h[n]")
plt.show()

# Plot the audio.
time_vec = np.arange(len(clip))
tidx = np.arange(0, int(np.min([44100, len(clip)])))
plt.subplot(211)
plt.plot(time_vec[tidx], clip[tidx])
plt.title("Original audio")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# Convolve the clip with the impulse response
# scipy.signal.convolve.
echo_clip = ss.convolve(clip, h, mode="full")

# Plot the audio.
plt.subplot(212)
plt.title("Convolution output")
# Scale numbers to 0..1 scale.
plt.plot(time_vec[tidx], echo_clip[tidx])
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.tight_layout()
plt.show()

# Normalize to unity.
echo_clip = echo_clip/(np.max(np.abs(echo_clip)))

print("Saving reverb.wav")
# Save as .wav file with 44.1 kHz sample rate.
sw.write("reverb.wav", sr, np.array(20e3*echo_clip, dtype=np.int16))
