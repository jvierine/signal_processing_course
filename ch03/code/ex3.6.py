import numpy as np
import matplotlib.pyplot as plt

# Simple function to compute the kth order root of unity of degree m.
def root_unity(k: int, m: int) -> float:
    return np.exp(2*np.pi*k*1j/m)


# Loop from 0 to 5, recall that the % operator computes the remainder, giving 0-4, then 0 again.
roots = np.array([root_unity(k % 5, 5) for k in range(6)])

# Partition an interval of one period.
t = np.linspace(0, 2*np.pi, num=50)

# Used to plot the unit circle.
x = np.cos(t)
y = np.sin(t)

# Extract the real and imaginary components.
z1 = roots.real
z2 = roots.imag

plt.figure(figsize=(4, 4))
ax = plt.gca()
plt.plot(z1, z2)
plt.plot(x, y)
plt.grid(True)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Fifth roots of unity")
ax.set_aspect("equal")
# Call this if needed.
# plt.show()
try:
    plt.savefig("../figures/roots.png")
except:
    print("couldn't save file")
