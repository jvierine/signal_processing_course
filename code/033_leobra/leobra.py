import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as n

z=iio.imread("zebra.png")
l=iio.imread("leopard.png")

z=(n.array(z[:,:,0],dtype=n.float32)+n.array(z[:,:,1],dtype=n.float32)+n.array(z[:,:,2]))/3.0
l=(n.array(l[:,:,0],dtype=n.float32)+n.array(l[:,:,1],dtype=n.float32)+n.array(l[:,:,2]))/3.0


plt.subplot(221)
plt.title("Zebra")
plt.imshow(z)

plt.subplot(222)
plt.title("Leopard")
plt.imshow(l)
#plt.show()
print(z.shape)
print(l.shape)

leobra = n.copy(z)
leobra[:,:]=0.0

zebard = n.copy(z)
zebard[:,:]=0.0

Z=n.fft.fft2(z[:,:])
L=n.fft.fft2(l[:,:])

# abs of leopard and phase of zebra
leobra[:,:] = n.fft.ifft2(n.abs(L)*n.exp(1j*n.angle(Z)))
zebard[:,:] = n.fft.ifft2(n.abs(Z)*n.exp(1j*n.angle(L)))
plt.subplot(223)
plt.title(r"LeoBra $|\hat{L}|e^{\angle  \hat{Z}}$")
plt.imshow(leobra.real)
plt.subplot(224)
plt.title(r"ZePard $|\hat{Z}|e^{\angle  \hat{L}}$")
plt.imshow(zebard.real)
plt.tight_layout()
plt.show()
    

