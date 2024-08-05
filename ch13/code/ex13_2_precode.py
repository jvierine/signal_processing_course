import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as sw
import scipy.signal as ss

# Read the noisy signal.
ts = sw.read("crappy.wav")
sr, crap = ts

# Filter length.
N = 4000

# Frequencies of noise (units of Hz).
f0 = 3e3
f1 = 5e3

# Choose a window function.
w = ...
# ^ See the scipy.signal documentation for a list of window functions.

# Implement the filter and apply it here.
uncrap = ...  # Complete this.

# Scale to 0.9, because 1.0 is the maximum allowed by the .wav file format.
uncrap = 0.9*uncrap/np.max(np.abs(uncrap))

# Save the filtered audio file.
sw.write("test_uncrappy.wav", sr, np.array(uncrap, dtype=np.float32))
