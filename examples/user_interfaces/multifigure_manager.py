# from __future__ import print_function
# import matplotlib
# matplotlib.use('GTK3AGG')
# matplotlib.rcParams['backend.multifigure'] = False
# matplotlib.rcParams['toolbar'] = 'toolmanager'

import matplotlib
matplotlib.use('GTK3AGG')
from matplotlib.figure import Figure
from matplotlib.backend_managers import FigureManager

fig = Figure()
manager = FigureManager(fig, 1)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3])
manager.show()

manager.mpl_connect('window_destroy_event', manager.destroy)
manager._mainloop()


# window = Window(fig)
# window.show()

# for i in range(5):
#     fig = plt.figure(i)
#     ax = fig.add_subplot(111)
#     ax.plot(np.random.rand(100))
#  
# plt.show()
