# from __future__ import print_function
import matplotlib
matplotlib.use('GTK3AGG')
# matplotlib.rcParams['backend.multifigure'] = False
matplotlib.rcParams['toolbar'] = 'toolmanager'
from matplotlib.backend_tools import ToolToggleBase


from matplotlib.figure import Figure
from matplotlib.backend_managers import FigureManager


class t1(ToolToggleBase):
    radio_group = 'multifigure'
    description = "change canvas"
    def __init__(self, *args, **kwargs):
        self.mfigure = kwargs.pop('figure')
        ToolToggleBase.__init__(self, *args, **kwargs)

    def enable(self, *args, **kwargs):
        self.toolmanager.manager.figure = self.mfigure


manager = FigureManager(None, 1)
backend = manager._backend

fig1 = Figure()
canvas1 = backend.FigureCanvas(fig1)
ax1 = fig1.add_subplot(111)
ax1.plot([1, 2, 3])

manager.figure = fig1

fig2 = Figure()
canvas2 = backend.FigureCanvas(fig2)
ax2 = fig2.add_subplot(111)
ax2.plot([3, 2, 1])

fig3 = Figure()
canvas3 = backend.FigureCanvas(fig3)
ax3 = fig3.add_subplot(111)
ax3.plot([1, 1, 1])

sidebar = manager._get_toolbar()
sidebar.set_flow('vertical')


manager.toolmanager.add_tool('f1', t1, figure=fig1)
manager.toolmanager.add_tool('f2', t1, figure=fig2)
manager.toolmanager.add_tool('f3', t1, figure=fig3)
sidebar.add_tool('f1', 'foo')
sidebar.add_tool('f2', 'foo')
sidebar.add_tool('f3', 'foo')
manager.window.add_element(sidebar, False, 'west')


manager.show()
manager.mpl_connect('window_destroy_event', manager.destroy)
manager._mainloop()

