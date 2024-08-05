import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read, write

# This code is based on the reverb example.


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


def reverb_model(room_length_std=30.0,  # Room wall to wall distance standard deviation in meters.
                 echo_magnitude=0.5,    # How much is reflected from a wall.
                 n_echoes=10,           # Number of echoes.
                 n_walls=10,            # Number of scattering surfaces.
                 sr=44100,              # Sample-rate.
                 c_sound=340.0):        # Speed of sound (m/s).
    """Simplified model of the acoustics of a room. 
    Model the reflections from reverberations between surfaces in a room.
    """

    echo_len = int(2*sr*room_length_std*n_echoes/c_sound)
    h = np.zeros(echo_len, dtype=np.float32)
    h[0] = 1.0  # This represents the initial impulse (the original signal).

    # Add each echo for the given number of walls.
    for _ in range(n_walls):
        # Generate random wall distance.
        wall_dist = np.abs(np.random.rand()*room_length_std)

        for i in range(n_echoes):
            idx = int(sr*(i + 1)*wall_dist/c_sound)

            if idx < echo_len:
                # Echoes decay. This model makes each echo decay as x^(i + 1), where x < 1
                # and i is the index for the ith echo.
                h[idx] = np.random.rand()*echo_magnitude**(i + 1.0)

    return h


if __name__ == "__main__":

    room_length_std = 75.0  # Standard deviation for the room length.
    echo_magnitude = 0.5  # Must be less than 1.
    n_echoes = 10  # Must be greater than 0.
    n_walls = 10  # Number of walls for the echo to bounce off.
    c_sound = 340.0  # Speed of sound.

    if len(sys.argv) != 2:
        print("Usage: <filename>")
        exit(1)

    _, filename = sys.argv

    print(f"Reading .wav file named {filename}")
    sr, x = read_wav_file(filename)

    print("Computing the reverb model...")
    h = reverb_model(room_length_std, echo_magnitude, n_echoes, n_walls, sr, c_sound)

    # Convolution happens here. The impulse response is convolved with
    # the audio signal (called x here), to spit out the reverb effect signal.
    print("Computing the convolution...")
    y = np.convolve(x, h, mode="full")

    print("Saving reverb.wav file.")
    write_wav_file("reverb.wav", sr, y)

    # Plot the impulse response. 
    plt.plot(h, color="darkblue")
    plt.xlabel("Index [n]")
    plt.ylabel("$h[n]$")
    plt.title(rf"Impulse response for reverb system.")
    plt.text(9.0, 0.7,
             rf"""
                Room length $\sigma$ = {room_length_std} m
                Echo magnitude: {echo_magnitude}
                Echos: {n_echoes}
                Walls: {n_walls} 
                Speed of sound: {c_sound} m/s
            """)
    # plt.show() # If needed
    plt.savefig("../figures/ex10_4b.png")

