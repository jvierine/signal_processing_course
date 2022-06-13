import scipy.io.wavfile as sw
import numpy as n

# remove low power spectral components
def compress_snippet(clip,compression_ratio=0.99):
    # length of sound clip
    L = len(clip)
    # half length (real valued signals have conjugate symmetric spectra)
    L2 = int(L/2)

    ## compress audio
    
    # DFT using the FFT algorithm, only use half of spectrum because it is symmetric
    clip_fft = n.fft.fft(clip)[0:L2]
    # remove DC
    clip_fft[0]=0.0
    
    # store orignal (for plotting)
    orig_fft = n.copy(clip_fft)

    # Sort spectral components by magnitude, smallest spectral components first
    idx=n.argsort(n.abs(clip_fft))

    # to store the compressed file, one saves the spectral indexes
    # of the strongest frequency components
    # and the sparse Frequency domain representation of the signal
    idxs=n.array(idx[int(L2*compression_ratio):L2],dtype="uint16")

    # convert to 8-bit integer format to save space
    spec_re=n.real(clip_fft[idxs])
    spec_im=n.imag(clip_fft[idxs])
    max_amp=n.max([n.max(spec_re),n.max(spec_im)])
    scale=n.array(max_amp,dtype=n.float32)
    spec_re=n.array(128.0*spec_re/max_amp,dtype=n.int8)
    spec_im=n.array(128.0*spec_im/max_amp,dtype=n.int8)

    ##  store compressed audio as binary files on disk
    idxs.tofile("compressed_idx.bin")
    scale.tofile("compressed_scale.bin")    
    spec_re.tofile("compressed_spec_re.bin")
    spec_im.tofile("compressed_spec_im.bin")    

    ## Decompress audio
    
    # load compressed audio signal from binary files
    idxs=n.fromfile("compressed_idx.bin",dtype="uint16")
    spec_re=n.fromfile("compressed_spec_re.bin",dtype=n.int8) # use 8-bit as they take up less space
    spec_im=n.fromfile("compressed_spec_im.bin",dtype=n.int8) # use 8-bit as they take up less space
    scale=n.fromfile("compressed_scale.bin",dtype=n.float32)  # store scale
    
    spec=n.array(spec_re+spec_im*1j,dtype=n.complex64)*scale/128.0
    comp_fft=n.zeros(L,dtype=n.complex64)

    # insert sparse spectral components into spectrum 
    comp_fft[idxs]=spec

    # insert conjugate symmetric sparse spectral components into spectrum 
    comp_fft[L-idxs]=n.conj(spec)
    
    # inverse DFT to get the time domain signal, based on
    # the sparse spectral representation
    # i.e., the reconstructed audio signal.
    # Discard the imaginary component.
    comp_clip=n.fft.ifft(comp_fft).real

    # calculate actual compression ratio based on storage size
    original_size=16.0*L # uncompressed size  (16 bits per sample)
    compressed_size=8.0*2.0*len(idxs) + 16.0*len(idxs) + 32.0 # sparse 8-bit spectra, 16-bit spectral indices, 32-bit scale factor
    real_comp_ratio=compressed_size/original_size
    
    return(comp_clip,comp_fft[0:L2],orig_fft,real_comp_ratio)

# read wav file
# this is the audio signal to be compressed
ts=sw.read("original.wav")
sr=ts[0]     # sample rate
clip=ts[1]  # extract audio file as numpy data vector
if len(clip.shape)==2: # if stereo, only use one channel
    print("using only one stereo channel")
    clip=ts[1][:,0]

# compress and decompress audio file
# compression_ratio=0.95 means 95% reduction in 
# file size. 
cr=0.9

# compress full length of the clip
W=100000
n_window=int(n.floor(len(clip)/W))
comp_clip=n.zeros(len(clip))
idx=n.arange(W)
for i in range(n_window):
    snippet=clip[i*W+idx]
    c,c_fft,o_fft,real_comp_ratio=compress_snippet(snippet,compression_ratio=cr)
    print("Achieved compression %1.2f %%"%(100.0*(1.0-real_comp_ratio)))
    comp_clip[i*W+idx]=c

# Save result as wav file so that we can easily listen to the audio
# quality after decompression of the compressed signal.

# scale numbers to 0..1 scale
comp_clip = comp_clip/(1.5*n.max(comp_clip))
sw.write("compressed_signal.wav",44100,comp_clip)
