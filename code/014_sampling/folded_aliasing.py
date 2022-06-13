#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt


sample_rate = 1000.0

frequencies = n.linspace(510,990,num=5)

t=n.arange(100.0)/sample_rate

for f0 in frequencies:
    x=n.cos(2.0*n.pi*f0*t+n.pi/2.0)
    plt.plot(t,x)
    plt.title("Sample-rate=%1.2f frequency=%1.2f"%(sample_rate,f0))
    plt.xlabel("Time (s)")
    plt.show()
    
