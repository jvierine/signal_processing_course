#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt

def u(x):
    uo=n.zeros(len(x))
    uo[x>=0]=1.0
    return(uo)


a1=0.5
b0=1.0
b1=1.0

nn=n.arange(-10,20)

h=b0*a1**nn*u(nn)+b1*a1**(nn-1)*u(nn-1)
plt.stem(nn,h)
plt.title("$h[n]=0.5^n u[n] + 0.5^{n-1}u[n-1]$")
plt.savefig("iir.png")

