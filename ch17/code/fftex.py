import numpy as n
import scipy.signal as s
N=16384
nn=n.arange(N)
freqs=[0.0003,0.012,0.055,0.102,0.85]
A=[1e5,0.5e5,1e3,1e4,0.5e4]
x1=n.zeros(N)

for i,f in enumerate(freqs):
    x1+=A[i]*n.cos(n.pi*freqs[i]*nn+n.random.randn(1))

# weak signal at the middle of the signal
x2=n.zeros(N)
x2[int(N/2)]=10.0
x2[int(N/2)+1000]=-5.0
x2[int(N/2)-1000]=1.0

x=x1+x2
