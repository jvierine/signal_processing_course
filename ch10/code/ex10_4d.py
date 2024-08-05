import sys

import numpy as np
from scipy.io.wavfile import read, write

# This code is based on the reverb example .


def read_wav_file(filename: str) -> tuple[int, np.ndarray]:
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
    of the filename to write to, the sample rate and 
    the actual data to write into the file."""

    # Use the floating point file format for .wav files.
    # This requires the data to be cropped between -1 and 1.
    # clipped_signal = np.clip(signal, a_min=-1.0, a_max=1.0, dtype=np.float32)
    clipped_signal = 0.9*signal/np.max(np.abs(signal))

    write(filename, sr, clipped_signal.astype(np.float32))


def reverb_1000_meters_model(room_length_std=1000.0,  # Room wall to wall distance standard deviation in meters.
                             echo_magnitude=0.5,      # How much is reflected from a wall.
                             sr=44100,                # Sample-rate.
                             c_sound=343.0):          # Speed of sound (m/s).
    """Implementation of the delta[n] + 0.5delta[n - n0] system.
    """

    # Formula for computing n0, see pdf for the computation.
    n0 = int((2*sr*room_length_std)/c_sound)
    h = np.zeros(2*n0, dtype=np.float32)

    h[0] = 1.0  # This represents the initial impulse (the original signal).

    # This is the reflection coming from a wall at a 1000 meter distance.
    # Note that the amplitude is halved.
    h[n0] = echo_magnitude

    return h


if __name__ == "__main__":

    room_length_std = 1000.0  # Standard deviation for the room length.
    echo_magnitude = 0.5  # Must be less than 1.
    c_sound = 343.0  # Speed of sound.

    if len(sys.argv) != 2:
        print("Usage: <filename>")
        exit(1)

    _, filename = sys.argv

    print(f"Reading .wav file named {filename}")
    sr, x = read_wav_file(filename)

    print("Computing the reverb model...")
    h = reverb_1000_meters_model(room_length_std, echo_magnitude, sr, c_sound)

    # Convolution happens here. The impulse response is convolved with
    # the audio signal (called x here), to spit out the reverb effect signal.
    print("Computing the convolution...")
    y = np.convolve(x, h, mode="full")

    print("Saving 1000m_reverb.wav file.")
    write_wav_file("1000m_reverb.wav", sr, y)
