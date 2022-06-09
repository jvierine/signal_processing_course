# Compendium for Signal Processing Course (FYS-2006)

## Main structure of the project
Structure of the repository has been changed. The notes have been divided into chapters. These being:
| Directory     | Description           | Status |
----------------|-----------------------|--------|
| ch01          | Introduction          | Done   |
| ch02          | Python                | Done   |
| ch03          | Complex Algebra       | Done*  |
| ch04          | Signals and Systems   | Done*  |
| ch05          | Elementary Signals    | Done*  |
| ch06          | Sinusodial Signals    | Done*  |
| ch07          | Fourier series        | Read*  |
| ch08          | Fourier Transform     | Read*  |
| ch09          | Discrete-time Signals | N/A    |

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
- Exercise 4.1, 4.6, 4.7, 4.8 and 4.9 have been removed
- Frequency response has been removed from the Fourier transform chapter
- Overall typos have been fixed. 

## To do
- Add a new programming exercise on signals and systems
- Fix the electromagnetic wave image in ch04 (remove the code examples and git clone https://github.com/jvierine/signal_processing into the code directory). The code examples in the notes repo are no longer up to date. Some of the figures are also from there. 
- Fix Python listing ch07 (add comments)
- Read through Python code and comment it
- Try to find a heat equation exercise

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
