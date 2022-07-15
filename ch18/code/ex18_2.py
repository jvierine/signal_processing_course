import numpy as n
import matplotlib.pyplot as plt
import sys

# sample value we want to plot on
nn = n.array([-2,-1,0,1,2,3,4,5,6,7,8,9,10])

# values for the impulse response function
h = n.array([0,1,1,3,-0.5,0,0,0,0,0,0,0,4])

# plot as a stem plot to emphasize the 
# discrete nature of the function
plt.stem(nn,h)
plt.xlabel("samples [n]")
plt.ylabel("$h[n]$")
plt.title("Impulse response")
# call this if needed
# plt.show()

try:
    plt.savefig("../figures/18_2.png")
except:
    print("couldn't save file")