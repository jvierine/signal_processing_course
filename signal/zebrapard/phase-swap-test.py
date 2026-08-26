import numpy as np


def swap_magnitude_and_phase(image1, image2):
    spectrum1 = np.fft.fft2(image1)
    spectrum2 = np.fft.fft2(image2)
    image12 = np.fft.ifft2(np.abs(spectrum1) * np.exp(1j * np.angle(spectrum2))).real
    image21 = np.fft.ifft2(np.abs(spectrum2) * np.exp(1j * np.angle(spectrum1))).real
    return image12, image21


rng = np.random.default_rng(42)
image1 = rng.normal(size=(32, 32))
image2 = rng.normal(size=(32, 32))
image12, image21 = swap_magnitude_and_phase(image1, image2)

np.testing.assert_allclose(np.abs(np.fft.fft2(image12)), np.abs(np.fft.fft2(image1)), atol=1e-10)
np.testing.assert_allclose(np.abs(np.fft.fft2(image21)), np.abs(np.fft.fft2(image2)), atol=1e-10)

same1, same2 = swap_magnitude_and_phase(image1, image1)
np.testing.assert_allclose(same1, image1, atol=1e-10)
np.testing.assert_allclose(same2, image1, atol=1e-10)

print("Zebrapard phase-swap tests passed")
