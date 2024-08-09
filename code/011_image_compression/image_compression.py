import imageio.v3 as si
import matplotlib.pyplot as plt
import numpy as np


# 2d fft image, remove compression_ratio*(width*height)
# spectral components.
#
def compress_image(image, compression_ratio=0.95):
    # 2D DFT.
    image_fft = np.fft.fft2(image)
    L = image.shape[0]*image.shape[1]

    # Convert to 1d array,
    # sort spectral components by magnitude,
    # smallest spectral components first.
    image_fft = image_fft.flatten()
    idx = np.argsort(np.abs(image_fft).flatten())

    # Remove weakest spectral components, these don't
    # need to be stored, so this reduces data storage requirement.
    # Ensure that at least two spectral components are left.
    max_idx = np.min([L-1, int(L*compression_ratio)])
    image_fft[idx[0:max_idx]] = 0.0
    image_fft.shape = image.shape

    # Inverse 2D DFT to get compressed image.
    # Take real component to ensure signal is real.
    comp_image = np.fft.ifft2(image_fft).real

    return ((comp_image, image_fft))


# Read image. Assume the image is perfect.
image = si.imread("husky.jpg", mode="F")

# How much do we compress the image. 0 is no compression,
# 1.0 is nearly 100% compression
# (we still have at least one spectral component.)
compression_ratio = 0.95

plt.figure(figsize=(12, 12))
# Show original image.
plt.subplot(221)
plt.imshow(image, cmap="gray", vmin=0, vmax=255)

plt.title("Original Image")

# Show 2D fourier transform of image.
image_fft = np.fft.fftshift(np.fft.fft2(image))
x_freq = np.linspace(-np.pi, np.pi, num=image_fft.shape[0])
y_freq = np.linspace(-np.pi, np.pi, num=image_fft.shape[1])
plt.subplot(222)
image_fft_dB = 10.0*np.log10(np.abs(image_fft)**2.0)
dB_min = np.min(image_fft_dB)
dB_max = np.max(image_fft_dB)
plt.pcolormesh(y_freq, x_freq, image_fft_dB)
plt.xlabel(r"$\omega_0$")
plt.ylabel(r"$\omega_1$")
plt.xlim([-np.pi, np.pi])
plt.ylim([-np.pi, np.pi])

plt.colorbar()
plt.title(r"$10 \log_{10}|F(\hat{\omega}_0,\hat{\omega}_1)|^2$")

# Compress image using 2D FFT.
plt.subplot(224)
comp_imag, comp_fft = compress_image(image, compression_ratio=compression_ratio)
plt.pcolormesh(y_freq, x_freq, 10.0*np.log10(np.abs(np.fft.fftshift(comp_fft) + 1e-9)**2.0), vmin=dB_min, vmax=dB_max)
plt.xlabel(r"$\omega_0$")
plt.ylabel(r"$\omega_1$")
plt.xlim([-np.pi, np.pi])
plt.ylim([-np.pi, np.pi])
plt.colorbar()
plt.title("2D FFT with smallest spectral components removed")

plt.subplot(223)
plt.imshow(comp_imag, cmap="gray", vmin=0, vmax=255)
plt.title("%1.1f percent compressed image" % (100.0*compression_ratio))
plt.tight_layout()
plt.savefig("image_compression.png")
plt.show()
