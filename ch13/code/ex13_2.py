import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile as sw
import scipy.signal as ss
import sys

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
f0 = 180
f1 = 400

# time-frequency uncertainty; to get the length of the filter
N = int(100.0*sr*(1.0/(f1 - f0)))
print(f"Length of filter = {N}")

# frequency in units of rad / s
om0 = 2*n.pi*f0
om1 = 2*n.pi*f1

# frequency in units of rad / sample
om0_hat = om0/sr
om1_hat = om1/sr

# allocate the impulse response
h = n.zeros(N,dtype=n.float32)

# use a Hann window of length N
w = ss.hann(N)

# loop over the range from 0 to N - 1
for i in range(N):
    if i == int(N/2):   # careful to avoid the 0/0 problem
        h[i] = (1 + (om0_hat - om1_hat)/(n.pi))*w[i]
    else:
        h[i] = (n.sin(om0_hat*(i - int(N/2))) / ((i - int(N/2))*n.pi) - n.sin(om1_hat*(i - int(N/2))) / ((i - int(N/2))*n.pi))*w[i]

# do some plotting of the impulse response
plt.subplot(121)
plt.plot(h)
plt.title("Impulse response")
plt.xlabel("Sample points (n)")
plt.ylabel("$h[n]$")
plt.xlim(N//2-100,N//2+100)
plt.subplot(122)
plt.plot(n.fft.fftshift(n.fft.fftfreq(len(h),d=1.0/sr))/1e3,convert_to_decibel(n.fft.fftshift(n.fft.fft(h))))
plt.title("Frequency response")
plt.xlabel("Frequency (kHz)")
plt.ylabel("$|\mathcal{H}|^{2}(f)$ (dB)")
plt.xlim(-1,1)
plt.tight_layout()
plt.savefig("../figures/impulse_response.png")
if len(sys.argv) == 1:
    plt.show()
plt.clf()

# apply the filter 
print("computing convolution")
res = n.convolve(h,clip,mode="full")

# normalize to unity
res = res/(n.max(n.abs(res)))

# plot the filtered signal and the frequency 
# domain representation of the signal
plt.plot(res)
plt.title("Filtered signal")
plt.xlabel("Sample points [n]")
if len(sys.argv) == 1:
    plt.show()
plt.clf()

plt.plot(n.fft.fftshift(n.fft.fftfreq(len(res),d=1.0/sr))/1e3,convert_to_decibel(n.fft.fftshift(n.fft.fft(res))),color="red")
plt.title("Filtered signal")
plt.xlim(-2,2)
plt.xlabel("Frequency (kHz)")
plt.ylabel("Power (dB)")
plt.savefig("../figures/freq_spec_filter.png")
if len(sys.argv) == 1:
    plt.show()
plt.clf()

print("Saving filtered.wav")
# save as .wav file with 44.1 kHz sample rate
sw.write("filtered.wav",sr,n.array(res,dtype=n.float32))