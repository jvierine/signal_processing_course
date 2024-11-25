# Signal Processing

By Juha Vierinen and Jørn Olav Jensen (2016-today). With contributions from numerous other students, teaching assistants, and educators. 

<img width="447" alt="Sum of sinusoids tends towards and infinitely narrow pulse" src="https://github.com/user-attachments/assets/a723dba9-9435-4ec0-85bf-70f3be17eb68">

Get the <a href="https://github.com/jvierine/signal_processing_course/blob/main/signal_processing.pdf">PDF here</a>.

This project consists of material, a book, intended to be used for a first course in signal processing on an undergraduate level. The main focus is on digital signal processing through practical real world programming tasks, including e.g., processing the laser gravitational wave interferometric observatory (LIGO) measurements. The material includes continuous-time theory out of necessity, as this froms the basis digital signal processing. Any course in signal processing would be incomplete and not stand on a firm foundation if we would have left this out. The programming examples are provided in the Python programming language. As with any mathematical course, we also include pencil and paper exercises that are intended to reinforce the learning of theoretical concepts. 

The course was developed for the Department of Physics and Technology students at University of Tromsø. The background of the students is highly varied, from e.g., electrical engineering, physics, computer science, machine learning, biology, and medical sciences. Because of the diversity of students, we have opted to include also mathematical concepts that might have not been included for students coming from purely an engineering background. 

The book is free for everyone to use. We have licensed it with the CC BY-NC 4.0. We invite students and educators to help us to develop this material further, as together we can do accomplish something that is better.

# Cheat Sheet

![Screenshot from 2024-11-25 12-21-41](https://github.com/user-attachments/assets/468899eb-1b7e-4fdf-b332-e21f12587fe5)


## Getting started

The easiest way to get started is to simply download the file signal_processing.pdf. It is the compiled book in pdf format, containing all the chapters, exercises, and programming tasks. The programming exercises can be found in the subdirectory: code. 

In case you want to modify or edit the content, feel free to browse the chapter_config.tex file to configure what content is included. To run all the Python examples (also creating the figures needed for the document), simply type: 
<code>
make 
</code>
The course book will be compiled in signal_processing.pdf

To only compile the LaTeX document without running the Python examples, type:
<code>
make pdf
</code>
Note that if you have never run the programming examples, you will be missing some figures. 

## Contributing to the project

In case you have found an error or want to propose a change, feel free to fork the project and send a pull request to the repository. You may also want to submit an issue directly on this project. 

## Contents

The course is divided into chapters. The order is the recommended sequence that the topics be taught. 

| Directory     | Description                            | Status |
----------------|----------------------------------------|--------|
| ch01          | Introduction                           | Done   |
| ch02          | Python                                 | Done   |
| ch03          | Complex Algebra                        | Done   |
| ch04          | Signals and Systems                    | Done   |
| ch05          | Elementary Signals                     | Done   |
| ch06          | Sinusodial Signals                     | Done   |
| ch07          | Fourier series                         | Done   |
| ch08          | Fourier Transform                      | Done   |
| ch09          | Discrete-time Signals                  | Done   |
| ch10          | Linear Time-invariant Systems          | Done   |
| ch11          | Frequency Response                     | Done   |
| ch12          | Discrete-time Fourier Transform (DTFT) | Done   |
| ch13          | Ideal and Tapered Filters              | Done   |
| ch14          | Time-frequency Uncertainty Principle   | Done   |
| ch15          | Discrete Fourier Transform             | Done   |
| ch16          | Spectral Analysis                      | Done   |
| ch17          | Arbitrary Frequency Response Filters   | Done   |
| ch18          | Z-transform, Finite Impulse Response   | Done   |
| ch19          | Z-Transform, Infinite Impulse Response | Done   |

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
- Causality has been removed from ch04 and all the exercises referring to this has been removed
- Added some details on time-invariant systems
- Exercise 3.9 has been rewritten. Added a new programming exercise
- Chapter 4 has been rewritten to make time-invariant systems easier and shorter
- Chapter 4 solutions has been changed to account for this
- Exercise 4.1, 4.6, 4.7, 4.8 and 4.9 have been removed; also infinite impulse exercise has been removed
- Exercise 5 from the Fourier transform chapter have been moved to ch10 as exercise 1
- Frequency response has been removed from the Fourier transform chapter
- Overall typos have been fixed and grammar has been improved
- Applications have been added to one 
- All source code has been added and is up-to-date
- Ordered lists have been removed (ch11)
- The proof of the commutative property of convolution is now an exercise in ch10
- Sonar exercise in ch10 has been removed
- Convolution of two rectangles example has been removed
- Moved Fur Elise to Spectral Analysis (ch16)
- Added exercise with solution for ch15 (DFT)
- Added make figures support
- fixed exercise in ch13

## To do

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

#### Linear Time-invariant Systems
