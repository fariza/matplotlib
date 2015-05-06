from __future__ import print_function
import matplotlib
matplotlib.use('GTK3Cairo')
matplotlib.rcParams['backend.multifigure'] = True
matplotlib.rcParams['toolbar'] = 'toolmanager'

import matplotlib.pyplot as plt

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
b = ax1.plot([1, 2, 3])

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot([3, 2, 1])

fig2.canvas.set_title('dude')

plt.show()