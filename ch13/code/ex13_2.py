import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile as sw
import scipy.signal as ss

# read the noisy signal
ts = sw.read("crappy.wav")
sr = ts[0]
crap = ts[1]

# filter length
N = 4000

# frequencies of noise (units of Hz)
f0 = 3e3
f1 = 5e3

# make the band a bit wider to hopefully remove some boundary effects
sf0 = f0 - 0.2e3
sf1 = f1 + 0.2e3

# calculate the discrete-time frequencies (units of rad / sample)
om0 = 2.0*n.pi*sf0/sr
om1 = 2.0*n.pi*sf1/sr

# declare the filter as 0
h = n.zeros(N)

# use a Hann window
w = ss.hann(N)

# the band-stop filter we found in a) with a Hann window function
for i in range(N):
    if i == int(N/2):   # careful to avoid the 0/0 problem
        h[i] = (1 + (om0 - om1)/(n.pi))*w[i]
    else:
        h[i] = (n.sin(om0*(i - int(N/2))) / ((i - int(N/2))*n.pi) - n.sin(om1*(i - int(N/2))) / ((i - int(N/2))*n.pi))*w[i]

# in frequency domain we multiply the filter with the spectral representation
# multiplication in frequency domain correspond to convolution in time domain
# therefore, convolve the band-stop filter and the signal
uncrap = n.convolve(crap, h, mode="valid")
# ^ mode = valid will remove some boundary effects

# scale to 0.9, because 1.0 is the maximum allowed by the .wav file format
uncrap = 0.9*uncrap/n.max(n.abs(uncrap))

# save the filtered audio file
sw.write("test_uncrappy.wav",sr,n.array(uncrap,dtype=n.float32))

def convert_to_decibel(x):
    return 10*n.log10(n.abs(x)**2)

plt.subplot(121)
plt.plot(h)
plt.title("Impulse response")
plt.xlabel("Samples [n]")
plt.ylabel("$h[n]$")
plt.xlim(N//2-100,N//2+100)
plt.subplot(122)
plt.plot(n.fft.fftshift(n.fft.fftfreq(len(h),d=1.0/sr))/1e3,convert_to_decibel(n.fft.fftshift(n.fft.fft(h))))
plt.title("Frequency response")
plt.xlabel("Frequency (kHz)")
plt.ylabel("$|\mathcal{H}(f)|^{2}$ (dB)")
plt.tight_layout()
plt.savefig("../figures/impulse_response.png")
# plt.show()

plt.clf()
plt.plot(n.fft.fftshift(n.fft.fftfreq(len(uncrap),d=1.0/sr))/1e3,convert_to_decibel(n.fft.fftshift(n.fft.fft(uncrap))),color="red")
plt.title("Spectrum of the filtered signal")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Power (dB)")
plt.savefig("../figures/freq_spec_filter.png")
# plt.show()