import sys

import matplotlib.pyplot as plt
import numpy as np


def running_average_filter(L: int, x: np.ndarray) -> np.ndarray:
    """Simple implementation of a running average
    filter."""

    y = np.zeros_like(x)

    # TODO: implement me!

    return y


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: L")
        exit(-1)

    L = int(sys.argv[1]) if sys.argv[1].isdecimal() else None

    if L is None:
        print("You need to specify the L value as an integer!")
        exit(-1)

    N = 500  # Length of the example signals.
    t = np.arange(N)

    # Random noise signal, will change with each run of the program.
    x = np.cumsum(np.random.randn(N))

    # Apply the running average filter.
    y = running_average_filter(L=3, x=x)

    plt.plot(t, x, label="Original", color="red")
    plt.plot(t, y, label="Filter", color="blue")
    plt.legend()
    plt.show()
