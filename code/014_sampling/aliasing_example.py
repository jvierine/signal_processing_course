#!/usr/bin/env python

import numpy as n
import matplotlib.pyplot as plt


fs=10.0 # 10 Hz sample-rate
t = n.arange(20)/fs # sample indices
f0=1.0
fk=f0 + n.arange(-2,2)*fs

dt_signal=n.cos(2.0*n.pi*f0*t)
plt.plot(dt_signal,".")
# plot all aliases
for fi,f in enumerate(fk):
    dt_signal=n.cos(2.0*n.pi*f*t)
    plt.plot(5*fi+dt_signal,".",label="f=%1.2f Hz"%(f))
plt.xlabel("Sample index (n)")
plt.ylabel("Signal amplitude (each frequency offset by a constant)")
plt.title("Aliased signals")
plt.legend()
plt.savefig("aliased_signals.png")
plt.show()

