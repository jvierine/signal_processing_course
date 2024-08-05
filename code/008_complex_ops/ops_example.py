import numpy as np

# Initialize a complex number variable z.
z = 1.0 + 0.5j
# Get the real component of z
z.real
# and imaginary component of z.
z.imag
# The absolute value of z.
np.abs(z)

# What is i^{-1}?
z2 = 1j**(-1)

# Create complex numbers using the complex exponential function.
z1 = np.exp(1j*np.pi)
z2 = np.exp(1j*np.pi/2.0)

# Complex multiply.
z3 = z1*z2
# Complex conjugation.
z_squared = z1*np.conj(z1)

# Determine phase angle.
theta3 = np.angle(z3)
