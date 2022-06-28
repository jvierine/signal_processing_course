import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile as sw
import scipy.signal as ss

# read audio file (wav format)
ts = sw.read("test.wav")
sr = ts[0]        # sample rate
clip = ts[1]      # extract audio file as numpy data vector

if len(clip.shape)==2: # if stereo, only use one channel
    print("using only one stereo channel. read on")
    clip = ts[1][:,0]

# length of filter
N = int(len(clip)/20)

f0 = 150
f1 = 400

om0 = 2*n.pi*f0
om1 = 2*n.pi*f1

om0_hat = om0/sr
om1_hat = om1/sr

h = n.zeros(N,dtype=n.float32)
w = ss.hann(N)

print(f"length = {N}")

for i in range(N):
    if i == int(N/2):
        h[i] = (1 + (om0_hat - om1_hat)/(n.pi))*w[i]
    else:
        h[i] = (n.sin(om0_hat*(i - int(N/2))) / ((i - int(N/2))*n.pi) - n.sin(om1_hat*(i - int(N/2))) / ((i - int(N/2))*n.pi))*w[i]

print("computing convolution")
res = n.convolve(h,clip[0:N],mode="full")

# normalize to unity
res = res/(n.max(n.abs(res)))

plt.plot(res)
plt.show()

print("Saving filtered.wav")
# save as .wav file with 44.1 kHz sample rate
sw.write("filtered.wav",sr,n.array(res,dtype=n.float32))

print('\a')