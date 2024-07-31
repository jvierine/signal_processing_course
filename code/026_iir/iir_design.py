import matplotlib.pyplot as plt
import numpy as np
# You'll find this on:
# github.com/jvierine/signal_processing/026_iir/plot_h.py
import plot_h
import scipy.signal as s

# Design an IIR band-pass filter with:
# Sample rate = 1000 Hz.
# Pass-band = 100 to 200 Hz.
# Maximum pass band ripple 1 dB.
# Minimum attenuation of signals out of band = 100 dB.
sample_rate = 1000.0
# Return zeros and poles of the filter.
zeros, poles, k = s.iirdesign(100, 200, gpass=3.0, gstop=100,
                              ftype='ellip', output="zpk", fs=sample_rate)
# Same filter, but return filter coefficients.
b, a = s.iirdesign(100, 200, gpass=3.0, gstop=100,
                   ftype='ellip', output="ba", fs=sample_rate)

# Create a white noise signal.
signal = np.random.randn(100000)

# Filter signal with the IIR filter specified with
# coefficients b and a.
filtered_signal = s.lfilter(b, a, signal)
plt.plot(filtered_signal)
plt.show()

# Plot the power spectrum estimate.
plt.psd(filtered_signal, NFFT=1024, Fs=sample_rate)
plt.savefig("ex_psd_lpf.png")
plt.show()

# Plot the system function and the magnitude response of the IIR filter.
plot_h.plot_hmag("ex_design_lpf.png",
                 zeros=zeros, poles=poles, vmin=-150,
                 fs=sample_rate)
