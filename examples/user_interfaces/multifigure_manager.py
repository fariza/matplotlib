from __future__ import print_function
import matplotlib
matplotlib.use('GTK3Cairo')
matplotlib.rcParams['backend.multifigure'] = True
matplotlib.rcParams['toolbar'] = 'toolmanager'
 
import matplotlib.pyplot as plt
import numpy as np
 
for i in range(5):
    fig = plt.figure(i)
    ax = fig.add_subplot(111)
    ax.plot(np.random.rand(10))
 
plt.show()