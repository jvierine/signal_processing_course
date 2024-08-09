import numpy as np
import scipy.io.wavfile as sw


# Remove low power spectral components.
def compress_snippet(clip, compression_ratio=0.99):
    # Length of sound clip.
    L = len(clip)
    # Half length (real-valued signals have conjugate symmetric spectra).
    L2 = int(L/2)

    # Compress audio.

    # DFT using the FFT algorithm, only use 
    # half of spectrum because it is symmetric.
    clip_fft = np.fft.fft(clip)[:L2]
    # Remove the DC component. 
    clip_fft[0] = 0.0

    # Store original (for plotting).
    orig_fft = np.copy(clip_fft)

    # Sort spectral components by magnitude, 
    # smallest spectral components first.
    idx = np.argsort(np.abs(clip_fft))

    # To store the compressed file, one saves the spectral 
    # indexes of the strongest frequency components
    # and the sparse frequency domain 
    # representation of the signal.
    idxs = np.array(idx[int(L2*compression_ratio):L2], dtype="uint16")

    # Convert to 8-bit integer format to save space.
    spec_re = np.real(clip_fft[idxs])
    spec_im = np.imag(clip_fft[idxs])
    max_amp = np.max([np.max(spec_re), np.max(spec_im)])
    scale = np.array(max_amp, dtype=np.float32)
    spec_re = np.array(128.0*spec_re/max_amp, dtype=np.int8)
    spec_im = np.array(128.0*spec_im/max_amp, dtype=np.int8)

    # Store compressed audio as binary files on disk.
    idxs.tofile("compressed_idx.bin")
    scale.tofile("compressed_scale.bin")
    spec_re.tofile("compressed_spec_re.bin")
    spec_im.tofile("compressed_spec_im.bin")

    # Decompress audio.

    # Load compressed audio signal from binary files.
    idxs = np.fromfile("compressed_idx.bin", dtype="uint16")

    # Use 8-bit as they take up less space.
    spec_re = np.fromfile("compressed_spec_re.bin", dtype=np.int8) 
    spec_im = np.fromfile("compressed_spec_im.bin", dtype=np.int8) 
    # Store scale.
    scale = np.fromfile("compressed_scale.bin", dtype=np.float32)  

    spec = np.array(spec_re + spec_im*1j, dtype=np.complex64)*scale/128.0
    comp_fft = np.zeros(L, dtype=np.complex64)

    # Insert sparse spectral components into spectrum.
    comp_fft[idxs] = spec

    # Insert conjugate symmetric sparse 
    # spectral components into spectrum.
    comp_fft[L-idxs] = np.conj(spec)

    # Inverse DFT to get the time domain signal, based on
    # the sparse spectral representation
    # i.e., the reconstructed audio signal.
    # Discard the imaginary component.
    comp_clip = np.fft.ifft(comp_fft).real

    # Calculate actual compression ratio based on storage size.
    original_size = 16.0*L  # Uncompressed size  (16 bits per sample).
    # Sparse 8-bit spectra, 16-bit spectral indices, 32-bit scale factor.
    compressed_size = 8.0*2.0*len(idxs) + 16.0*len(idxs) + 32.0  
    real_comp_ratio = compressed_size/original_size

    return comp_clip, comp_fft[:L2], orig_fft, real_comp_ratio


# Read wav file.
# This is the audio signal to be compressed.
ts = sw.read("original.wav")
sr, clip = ts # Get the sample rate and the data from the file.
if len(clip.shape) == 2:  # If stereo, only use one channel.
    print("Using only one stereo channel.")
    clip = clip[:, 0] # Extract only one channel.



# Compress and decompress audio file.
# Compression_ratio=0.95 means 95% reduction in
# file size.
cr = 0.9

# Compress full length of the clip.
W = 100000
n_window = int(np.floor(len(clip)/W))
comp_clip = np.zeros(len(clip))
idx = np.arange(W)

for i in range(n_window):
    snippet = clip[i*W + idx]
    c, c_fft, o_fft, real_comp_ratio = compress_snippet(snippet, compression_ratio=cr)
    print(f"Achieved compression {(100.0*(1.0 - real_comp_ratio)):1.2f} %")
    comp_clip[i*W + idx] = c

# Save result as wav file so that we can easily listen to the 
# audio quality after decompression of the compressed signal.

# Scale numbers to 0..1 scale.
comp_clip = comp_clip/(1.5*np.max(comp_clip))
sw.write("compressed_signal.wav", 44100, comp_clip)
