import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile as sw
import scipy.signal as ss

# read the noisy signal
ts = sw.read("crappy.wav")
sr = ts[0]      # get sample-rate
crap = ts[1]    # some files might be stereo

# filter length
N = 4000

# frequencies of noise (units of Hz)
f0 = 3e3
f1 = 5e3

# choose a window function
w = ...
# ^ see the scipy.signal documentation for a list of window functions

# implement the filter and apply it here
uncrap = ... # complete this

# scale to 0.9, because 1.0 is the maximum allowed by the .wav file format
uncrap = 0.9*uncrap/n.max(n.abs(uncrap))

# save the filtered audio file
sw.write("test_uncrappy.wav",sr,n.array(uncrap,dtype=n.float32))