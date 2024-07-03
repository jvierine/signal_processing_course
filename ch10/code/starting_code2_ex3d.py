import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read, write


def read_wav_file(filename: str) -> tuple[float, np.ndarray]:
    """Function to read a .wav file. Returns the sample
    rate and a single channel with the audio.
    """

    # Read the file, then extract the necessary information.
    wav_file = read(filename)
    sr, signal = wav_file

    # Check if the audio is stereo or mono.
    if len(signal.shape) == 2:
        # Use only 1 channel if stereo.
        signal = signal[:, 0]

    return sr, signal


def write_wav_file(filename: str, sr: float, signal: np.ndarray) -> None:
    """Function to write to a .wav file. Arguments consists
    of the filename to write to, the sample rate and the actual
    data to write into the file."""

    # Use the floating point file format for .wav files.
    # This requires the data to be cropped between -1 and 1.
    clipped_signal = np.clip(signal, a_min=-1.0, a_max=1.0, dtype=np.float32)

    write(filename, sr, clipped_signal)


def running_average_filter(L: int, x: np.ndarray) -> np.ndarray:
    """Simple implementation of a running average
    filter."""

    y = np.zeros_like(x)

    # TODO: Implement me!

    return y


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: <filename> <L>")
        exit(1)

    _, filename, l = sys.argv
    print(f"Filtering file: '{filename}' using L = {l}")

    # Verify that the input for the program is okay.
    L = int(l) if l.isdecimal() else None

    if L is None:
        print("Invalid size of running average filter.")
        exit(1)

    # Read the file from disk.
    sr, signal = read_wav_file(filename)

    # Filter the audio signal using a running average
    # low-pass filter with the user specified L.
    filtered_signal = running_average_filter(L, signal)

    # Partition the x-axis into units of time (in seconds).
    t = np.arange(len(signal))  # TODO: Adjust this line to get units of seconds, instead of samples.

    plt.plot(t, signal, label="Original", color="red")
    plt.plot(t, filtered_signal, label="Filtered", color="blue")
    plt.show()

    # Write the result to disk.
    write_wav_file(f"{filename}_filtered.wav", sr, filtered_signal)
