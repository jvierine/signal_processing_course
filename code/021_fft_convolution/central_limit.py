#
# Use convolution to demonstrate that
# by convolving a signal with itself
# the signal approaches a gaussian
# density. This is a numerical demonstration
# of the central limit theorem.
# 
import numpy as n
import matplotlib.pyplot as plt
import scipy.signal as s

# input signals to be convolved
a=n.ones(12)
a[0]=0.0
a[11]=0.0
b=n.copy(a)

fig=plt.figure(figsize=(4,8))
# zero-padded FFT (10+20=30)
for i in range(10):
    idx=n.arange(len(b))-len(b)/2.0
    plt.plot(idx,b/n.max(b)+i,color="black")
    plt.text(0,i+1.1,"%d"%(i))
    b=s.fftconvolve(a,b)
plt.axis("off")
plt.tight_layout()
plt.savefig("central_limit.png",bbox_inches='tight')
plt.show()
