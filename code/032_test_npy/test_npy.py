import numpy as n
import matplotlib.pyplot as plt


signal=n.load("test.npy")
plt.stem(signal)
plt.show()

