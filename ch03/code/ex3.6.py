import numpy as n
import matplotlib.pyplot as plt

# simple function to compute the kth order root of unity of degree m
def rootUnity(k,m):
    return n.exp((2*n.pi*k*1j)/m)

# put all the roots in an array
roots = n.array([rootUnity(0,5),rootUnity(1,5),rootUnity(2,5),rootUnity(3,5),rootUnity(4,5),rootUnity(0,5)])

# partition an interval of one period
t = n.linspace(0,2*n.pi,num=50)

# used to plot the unit circle
x = n.cos(t)
y = n.sin(t)

# extract the real and imaginary components
z1 = roots.real
z2 = roots.imag

# plotting
plt.plot(z1,z2)
plt.plot(x,y)
plt.grid(True)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Fifth roots of unity")
plt.show()