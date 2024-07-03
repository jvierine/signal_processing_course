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

         # Use +1 since n is never actually the final index of y.
        y[n] = np.mean(x[start:n+1]) 

    return y


if __name__ == "__main__":

    x = np.array([1.2, 4.3, 4.7, 3.3, 2.9], dtype=np.float32)

    print(running_average_filter(3, x))
