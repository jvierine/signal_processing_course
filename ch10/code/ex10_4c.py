
import numpy as np
import matplotlib.pyplot as plt


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


h1 = reverb_model(2.0, 0.5, 10, 10, 44100, 340)
h2 = reverb_model(75.0, 0.5, 10, 10, 44100, 340)

# h1 will be shorter than h2 when the room is larger.
length = min(len(h1), len(h2))

t = np.arange(length)

plt.plot(t, h1[:length], label="Small room", color="blue")
plt.plot(t, h2[:length], label="Large room", color="red")
plt.xlabel("Samples $n$")
plt.legend()
plt.title("Impulse response comparison.")
# plt.show() # Run if needed.
plt.savefig("../figures/ex10_4c.png")
