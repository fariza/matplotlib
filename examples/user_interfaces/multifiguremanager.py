import matplotlib
matplotlib.use('GTK3Cairo')
matplotlib.rcParams['toolbar'] = 'navigation'
matplotlib.rcParams['backend.multifigure'] = True

from matplotlib.backends.backend_gtk3cairo import FigureCanvas, FigureManager, show
 
figure1 = matplotlib.figure.Figure()
ax1 = figure1.add_subplot(111)
ax1.plot([1,2,3])
canvas1 = FigureCanvas(figure1)
manager = FigureManager(canvas1, 1)
 
figure2 = matplotlib.figure.Figure()
ax2 = figure2.add_subplot(111)
ax2.plot([3,2,3])
canvas2 = FigureCanvas(figure2)
 
 
manager.add_canvas(canvas2, 2)
 
figure3 = matplotlib.figure.Figure()
ax3 = figure3.add_subplot(111)
ax3.plot([3,2,1])
canvas3 = FigureCanvas(figure3)
 
manager.add_canvas(canvas3, 3)
 
canvas2.set_title("dude")
 
manager.set_active_canvas(canvas1)
 
manager.show()
show.mainloop()


# import matplotlib.pyplot as plt
# 
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(111)
# ax1.plot([1,2,3])
# 
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111)
# ax2.plot([3,2,3])
# 
# fig2.canvas.set_title('dude')
# 
# plt.show()