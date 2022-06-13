#!/usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]
})

import numpy as n

import imageio

# read image
im = imageio.imread('fourier_head.jpg')
im=n.array(im[:,:,0],dtype=n.float32)/255.0
plt.imshow(im,cmap="gray")
plt.show()

I=n.fft.rfft2(im)
oshape=I.shape

idxs=n.argsort(n.abs(I),axis=None)[::-1]

IO=n.copy(I)
IO[:,:]=0
S=n.copy(im)
S[:,:]=0.0
for i in range(10000):
    print(i)
    
    x,y=n.unravel_index(idxs[i],shape=oshape)
    IO[:,:]=0.0
    IO[x,y]=I[x,y]
    S0=n.fft.irfft2(IO)
    S+=S0
    

    plt.figure(figsize=(8,4))
    plt.subplot(121)
    plt.title("Spectral component\n$\displaystyle{\Psi_{%d}= \mathrm{Re}\{A_{%d} e^{i k_{%d} x}e^{i \ell_{%d} y}}\}$"%(i+1,i+1,i+1,i+1))
    plt.xlabel("$x$")
    plt.ylabel("$y$")    
#    plt.title("Spectral component %d"%(i+1))
    plt.imshow(S0,cmap="gray")
 #   plt.colorbar()
        
        
    plt.subplot(122)
    plt.title("Sparse estimate\n$S = \sum_{n=1}^{%d} \Psi_n$"%(i+1))
    plt.imshow(S,cmap="gray")
    plt.xlabel("$x$")
    plt.ylabel("$y$")        
#    plt.colorbar()
    plt.savefig("ft-%04d.jpg"%(i))
    plt.clf()
    plt.close()


