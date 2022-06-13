import numpy as n

# Initialize a complex number variable z
z = 1.0 + 0.5j
# get the real component of z
z.real
# and imaginary component of z
z.imag
# the absolute value of z
n.abs(z)

# What is i^{-1}?
z2 = 1j**(-1)

# create complex numbers using the complex exponential function
z1 = n.exp(1j*n.pi)
z2 = n.exp(1j*n.pi/2.0)

# complex multiply
z3=z1*z2
# complex conjugation
z_squared = z1*n.conj(z1)

# determine phase angle 
theta3=n.angle(z3)
