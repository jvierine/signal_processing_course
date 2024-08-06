import sys

import matplotlib.pyplot as plt
import numpy as np


def running_average_filter(L: int, x: np.ndarray) -> np.ndarray:
    """Simple implementation of a running average
    filter."""

    y = np.zeros_like(x)

    for n in range(len(y)):

        # Determine if the index is negative.
        # If yes, pick 0 as the starting point, otherwise
        # use n - L + 1. Add 1 to avoid the n = L case.
        start = max(0, n - L + 1)

        y[n] = np.mean(x[start:n+1])  # Use +1 since n is never actually the final index of y.

    return y


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: <L>")
        exit(1)

    L = int(sys.argv[1]) if sys.argv[1].isdecimal() else None

    if L is None:
        print("L should be an integer!")
        exit(1)

    N = 500  # Length of the example signals.
    t = np.arange(N)

    # Random noise signal, will change with each run of the program.
    x = np.cumsum(np.random.randn(N))

    # Apply the running average filter.
    y = running_average_filter(L=L, x=x)

    plt.plot(t, x, label="Original", color="red")
    plt.plot(t, y, label="Running average filtered", color="blue")
    plt.xlabel("Samples $n$")
    plt.legend()
    # # plt.show() # Call this if needed.
    plt.savefig("../figures/ex10_3c.png")
