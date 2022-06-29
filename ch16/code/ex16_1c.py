import numpy as n
import matplotlib.pyplot as plt
import scipy.io.wavfile
import scipy.signal as ss
import sys

# function to convert to dB
def convert_to_decibel(x):
    return 10*n.log10(n.abs(x)**2)

audio = scipy.io.wavfile.read("../../code/023_dynamic_spectrum/b.wav")
sample_rate = audio[0]
# read only one channel of the stereo signal
signal = audio[1][:,0]

# function to compute the spectogram
def spectogram(signal,delta_n,N,M):
    # have a signal x of length L
    # we divide the signal into sub arrays of length N, the step size is then delta_n
    # the maximum time units are then L/delta_n

    # M - length of FFT
    # N - length of window
    # delta_n - step size in time

    # window function (Hann window)
    w = ss.hann(N)

    # length of signal
    L = len(signal)

    # compute the maximum number of time steps
    t_max = int((L-N)/delta_n)

    # allocate space for the spectogram and sub_arrays
    H = n.zeros([t_max,M],dtype=n.complex64)
    sub_array = n.zeros(N)

    # step through the signal
    for i in range(t_max):
        # get a sub_array and then fft it with the window and store it in H
        sub_array[0:N] = signal[i*delta_n + n.arange(N)]
        H[i,:] = n.fft.fft(sub_array*w,M)

    return H

M = 10480
N = 2000
delta_n = 40

# compute the spectogram
spect = spectogram(signal,delta_n,N,M)

# partition the axes correctly with units of Hertz and seconds
freqs = n.fft.fftfreq(M,d=1.0/sample_rate)
time = delta_n*n.arange(spect.shape[0])/sample_rate

# create the spectogram plot, limiting frequency to (0,1500) Hz
plt.pcolormesh(time,freqs[0:M//2],n.transpose(convert_to_decibel(spect[:,0:M//2])),vmin=40)
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.ylim(0,1500)
plt.colorbar()
plt.savefig("../figures/fur_elise_spectogram.png")

if len(sys.argv) == 1:
    plt.show()