import matplotlib.pyplot as plt
import numpy as np

# Load data, download data from:
# http://kaira.uit.no/fys2006/lcb1.dat
d = np.loadtxt("lcb1.dat")

# Measurement times.
m_error = d[:, 2]

# Select find measurements that don't have large errors.
good_idx = np.where(np.abs(m_error) < 1.0)[0]

# Measurement time (units of days.)
m_t = d[good_idx, 0]

# Magnitude measurements (relative magnitude of star.)
m_mag = d[good_idx, 1]

# Fundamental period.
T = 13.124349

# Time, modulo period.
m_modulo_t = np.mod(m_t, T)

plt.plot(m_modulo_t, m_mag, ".")

# Number of Fourier series coefficients.
N = 10
N_meas = len(m_mag)

# Frequency indices.
k_idx = np.arange(-N, N+1)

# Theory matrix.
A = np.zeros([N_meas, len(k_idx)], dtype=np.complex64)

for ki, k in enumerate(k_idx):
    # Setup theory matrix row.
    A[:, ki] = np.exp(1j*(2.0*np.pi/T)*k*m_modulo_t)

# Find maximum likelihood estimate for Fourier Series coefficients c_k.
S = np.linalg.inv(np.dot(np.transpose(np.conj(A)), A))
c_k = np.dot(np.dot(S, np.transpose(np.conj(A))), m_mag)
print(c_k.shape)
# Evaluate the Fourier Series for the maximum likelihood estimate of
# coefficients c_k.
N_model = 100
model_t = np.linspace(0, T, num=N_model)
model = np.zeros(N_model, dtype=np.complex64)

# Sum together signal for all Fourier series coefficients a_k.
for ki, k in enumerate(k_idx):
    # Figure out what to put here.
    # array "model_t" contains time.
    # array "c_k" contains the Fourier series coefficients.
    # We want the array "model" to contain the Fourier Series
    # vector.
    model += c_k[ki]*np.exp(1j*2*np.pi*k*model_t/T)

plt.plot(model_t, model.real, label="Model")
plt.plot(m_modulo_t, m_mag, "x", label="Measurements")
plt.title("Fourier series model for Cepheid variable star")
plt.xlabel("Time (days)")
plt.ylabel("Relative Magnitude")
plt.legend()
plt.show()
