import scipy.io.wavfile as sw
import scipy.signal as ss
import numpy as n
import matplotlib.pyplot as plt

ts=sw.read("elysium.wav")
sr=ts[0]
clip=ts[1][:,0]
print(clip.shape)
n_samples=len(clip)
print(n_samples)
noise=n.random.randn(n_samples)

# filter length
nn = n.arange(-1000,1000)+1e-7
N=len(nn)
print(nn)

f0=3e3
f1=5e3
om0 = 2.0*n.pi*f0/sr
om1 = 2.0*n.pi*f1/sr
print(om0)
print(om1)
bpf=ss.hann(N)*(n.sin(om1*nn)/(n.pi*nn) - n.sin(om0*nn)/(n.pi*nn))
#plt.plot(bpf)
#plt.show()
#

# implement convolution using fft (periodic convolution)
noise_bpf=n.fft.irfft(n.fft.rfft(noise,len(noise))*n.fft.rfft(bpf,len(noise)))*10000*n.mean(n.abs(clip))
crap = noise_bpf + clip
crap = 0.9*crap/n.max(n.abs(crap))
plt.plot(crap)
plt.show()

sw.write("crappy.wav",sr,n.array(crap,dtype=n.float32))

sf0=f0-0.2e3
sf1=f1+0.2e3
om0 = 2.0*n.pi*sf0/sr
om1 = 2.0*n.pi*sf1/sr

bsf=ss.hann(N)*( ( n.abs(nn)<1e-6) + n.sin(om0*nn)/(n.pi*nn)-n.sin(om1*nn)/(n.pi*nn))

plt.plot(10.0*n.log10(n.abs(n.fft.fftshift(n.fft.fft(bsf)))**2.0))
plt.plot(10.0*n.log10(n.abs(n.fft.fftshift(n.fft.fft(bpf)))**2.0))
plt.show()

uncrap=n.convolve(crap,bsf,mode="same")

uncrap[0:1000]=0.0
uncrap[(len(uncrap)-1000):len(uncrap)]=0.0
plt.plot(uncrap)
plt.show()

uncrap = 0.9*uncrap/n.max(n.abs(uncrap))


sw.write("uncrappy.wav",sr,n.array(uncrap,dtype=n.float32))
