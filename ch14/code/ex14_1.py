import numpy as n
import matplotlib.pyplot as plt

# frequency response for the Hann window with T = 1
def H1(omega):
    return (n.sin(omega/2)/omega + (1/2)*n.sin(n.pi - (1/2)*omega)/(2*n.pi - omega) + (1/2)*n.sin(n.pi + (1/2)*omega)/(2*n.pi + omega))*n.exp(-1j*1/2*omega)

# frequency response for the rectangular window with T = 1
def H2(omega):
    return 2*n.sin(omega/2)/omega*n.exp(-1j*1/2*omega)

# function to convert to dB
def convert_to_decibel(x):
    return 10*n.log10(n.abs(x)**2)

# partition the interval (-10pi,10pi) into 1000 equally spaced points
x = n.linspace(-10*n.pi,10*n.pi,num=1000)

# plot the window functions to compare 
# radians per sample on the x-axis and dB on the y-axis
plt.plot(x,convert_to_decibel(H1(x)),label="Hann window")
plt.plot(x,convert_to_decibel(H2(x)),label="Rectangular window")
plt.xlabel("$\hat{\omega}$")
plt.ylim(-120,10)   # limit the y-axis to (-120,10)
plt.legend()
# call this if needed
# plt.show()

try:
    plt.savefig("../figures/filters.png")
except:
    print("couldn't save file")