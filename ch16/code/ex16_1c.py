import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile
from scipy.signal.windows import hann


def convert_to_decibel(x):
    """Function to convert to dB."""
    return 10*np.log10(np.abs(x)**2)


audio = scipy.io.wavfile.read("b.wav")
sample_rate = audio[0]

# Read only one channel of the stereo signal.
signal = audio[1][:, 0]


def spectrogram(signal, delta_n, N, M):
    """Have a signal x of length L.
    We divide the signal into sub arrays of length N, the step size is then delta_n
    the maximum time units are then L/delta_n

    M - length of FFT.
    N - length of window.
    delta_n - step size in time.
    """

    # Window function (Hann window).
    w = hann(N)

    # Length of signal.
    L = len(signal)

    # Compute the maximum number of time steps.
    t_max = (L - N) // delta_n

    # Allocate space for the spectogram and sub_arrays.
    H = np.zeros([t_max, M], dtype=np.complex64)
    sub_array = np.zeros(N)

    # Step through the signal.
    for i in range(t_max):
        # Get a sub_array and then fft it with the window and store it in H.
        sub_array[:N] = signal[i*delta_n + np.arange(N)]
        H[i, :] = np.fft.fft(sub_array*w, M)

    return H


M = 10480
N = 2000
delta_n = 40

# Compute the spectrogram.
spect = spectrogram(signal, delta_n, N, M)

# Partition the axes correctly with units of Hertz and seconds.
freqs = np.fft.fftfreq(M, d=1.0/sample_rate)
time = delta_n*np.arange(spect.shape[0])/sample_rate

# Create the spectrogram plot, limiting frequency to (0, 1500) Hz.
plt.pcolormesh(time, freqs[:M//2], np.transpose(convert_to_decibel(spect[:, :M//2])), vmin=40)
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.ylim(0, 1500)
plt.colorbar()
# Call this if needed.
# plt.show()

try:
    plt.savefig("../figures/fur_elise_spectogram.png")
except:
    print("couldn't save file")
