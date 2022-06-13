#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt

# load data
# download data from:
# http://kaira.uit.no/fys2006/lcb1.dat
d=n.loadtxt("lcb1.dat")

# measurement times
m_error=d[:,2]

# select find measurements that don't have large errors
good_idx=n.where(n.abs(m_error)<1.0)[0]

# measurement time (units of days)
m_t=d[good_idx,0]

# magnitude measurements (relative magnitude of star)
m_mag=d[good_idx,1]

# fundamental period
T=13.124349

# time, modulo period
m_modulo_t=n.mod(m_t,T)

plt.plot(m_modulo_t,m_mag,".")

# number of Fourier series coefficients
N=10
N_meas=len(m_mag)

# frequency indices
k_idx=n.arange(-N,N+1)

# theory matrix
A=n.zeros([N_meas,len(k_idx)],dtype=n.complex)

for ki,k in enumerate(k_idx):
    # setup theory matrix row
    A[:,ki]=n.exp(1j*(2.0*n.pi/T)*k*m_modulo_t)

# find maximum likelihood estimate for Fourier Series coefficients c_k
S=n.linalg.inv(n.dot(n.transpose(n.conj(A)),A))
c_k=n.dot(n.dot(S,n.transpose(n.conj(A))),m_mag)
print(c_k.shape)
# Evaluate the Fourier Series for the maximum likelihood estimate of
# coefficients c_k
N_model=100
model_t=n.linspace(0,T,num=N_model)
model = n.zeros(N_model,dtype=n.complex64)

# sum together signal for all Fourier series coefficients a_k
for ki,k in enumerate(k_idx):
    # figure out what to put here. 
    # array "model_t" contains time
    # array "c_k" contains the Fourier series coefficients
    # we want the array "model" to contain the Fourier Series
    # vector
    model+= # ... figure out what to put here
        
plt.plot(model_t,model.real,label="Model")
plt.plot(m_modulo_t,m_mag,"x",label="Measurements")
plt.title("Fourier series model for Cepheid variable star")
plt.xlabel("Time (days)")
plt.ylabel("Relative Magnitude")
plt.legend()
plt.show()
