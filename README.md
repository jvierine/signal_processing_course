# Compendium for Signal Processing Course (FYS-2006)

## Main structure of the project
Structure of the repository has been changed. The notes have been divided into chapters. These being:
| Directory     | Description                            | Status |
----------------|----------------------------------------|--------|
| ch01          | Introduction                           | Done   |
| ch02          | Python                                 | Done   |
| ch03          | Complex Algebra                        | Done*  |
| ch04          | Signals and Systems                    | Done*  |
| ch05          | Elementary Signals                     | Done*  |
| ch06          | Sinusodial Signals                     | Done*  |
| ch07          | Fourier series                         | Done*  |
| ch08          | Fourier Transform                      | Done*  |
| ch09          | Discrete-time Signals                  | Done*  |
| ch10          | Linear Time-invariant Systems          | Read*  |
| ch11          | Frequency Response                     | Done*  |
| ch12          | Discrete-time Fourier Transform (DTFT) | Done*  |

Furthermore, each directory has the following structure
| Directory     | Contains                                                           |
----------------|--------------------------------------------------------------------|
| figures       | Directory for figures used in the chapter                          |
| code          | Contains the Python source code used in the corresponding chapter  |
| text.tex      | LaTex file with the source code for the chapter                    |
| exercises.tex | LaTex file with the exercises for the given chapter                |
| solutions.tex | LaTex file with suggested solutions to the exercises               |

## Changes
- Wrote a segment on exponents for complex exponentials (ch03)
- Causality has been removed from ch04 and all the exercises refering to this has been removed
- Added some details on time-invariant systems
- Exercise 3.9 has been rewritten. Added a new programming exercise
- Chapter 4 has been rewritten to make time-invariant systems easier and shorter
- Chapter 4 solutions has been changed to account for this
- Exercise 4.1, 4.6, 4.7, 4.8 and 4.9 have been removed; also infinite impulse exercise has been removed
- Exercise 5 from the Fourier transform chapter have been moved to ch10 as exercise 1
- Frequency response has been removed from the Fourier transform chapter
- Overall typos have been fixed. 
- Applications have been added to one 
- All source code has been added and is up to date
- Ordered lists have been removed (ch11)

## To do
- Add a new programming exercise on signals and systems
- Fix the rectangular signal exercise
- Read through Python code and comment it
- Try to find a heat equation exercise
- Shorten Gaussian derivation of Fourier transform
- Shorten convolution property discussion and derivation

### Everything you need to know
#### Complex Algebra:
    - Euler's formula
    - Amplitude, phase and the relation between rectangular and polar form of a complex number
    - Real and imaginary parts of a complex number
    - The complex exponential and that it is a periodic complex function with a period of 2\pi. 
    - The complex conjugate
    - Inverse Euler relations
    - The interpretation of sums and products of complex numbers

#### Signals and Systems
    - What is a signal and what is a system
    - Discrete v.s. continuous signals
    - Examples of signals and systems
    - Time delay system
    - Amplification system
    - Linear systems
    - Time-invariant systems
    - How to implement a simple system in Python

#### Elementary Signals
    - Definition and properties of the Dirac delta-function
    - Definition and properties of the unit-step function
    - Difference between continuous and discrete Dirac delta-function
    - The continuous and discrete unit-step function
    - Evaluation of integrals using these functions

#### Sinusodial Signals
    - Definition of sinusoid
    - Angular frequency, frequency, phase, fundamental period
    - Delay system on sinusodial signal

#### Fourier Series
    - Definition of a Fourier series
    - How to find the Fourier series for a periodic function
    - How to determine if a signal is periodic
    - Finding the fundamental frequency and fundamental period
    - How the Fourier series is affected by time shifting and taking a derivative
    - The Fourier transform as the limit of a Fourier series for an infinite period

#### Fourier transform
    - Definition of the forward and inverse Fourier transform
    - Properties of the Fourier transform
    - Common Fourier transform pairs
    - That the Fourier series can be shown as a special case of the Fourier transform
    - Plancherel's theorem and Parseval's theorem
    - Convolution theorem

#### Discrete-time Signals
    - Converting a signal from continuous-time to discrete-time (discritization)
    - Sample-rate and sample-spacing; how these relate to discrete-time angular frequency
    - Sampling of complex sinusoids and real signals
    - Aliasing and folding
    - Nyquist zones, the principal spectrum
    - Shannon-sampling theorem and the sampling criteria
    - Reconstruction of signals from the samples; the ideal reconstruction filter