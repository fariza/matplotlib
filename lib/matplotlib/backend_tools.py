"""
Abstract base classes define the primitives for Tools.
These tools are used by `NavigationBase`

:class:`ToolBase`
    Simple tool that gets instantiated every time it is used

:class:`ToolPersistentBase`
    Tool whose instance gets registered within `Navigation`

:class:`ToolToggleBase`
    PersistentTool that has two states, only one Toggle tool can be
    active at any given time for the same `Navigation`
"""


from matplotlib import rcParams
from matplotlib._pylab_helpers import Gcf
import matplotlib.cbook as cbook
from weakref import WeakKeyDictionary
import numpy as np


class Cursors:
    # this class is only used as a simple namespace
    HAND, POINTER, SELECT_REGION, MOVE = list(range(4))
cursors = Cursors()


class ToolBase(object):
    """Base tool class

    Attributes
    ----------
    navigation : `NavigationBase`
        Navigation that controls this Tool
    figure : `FigureCanvas`
        Figure instance that is affected by this Tool
    """

    keymap = None
    """Keymap to associate with this tool

    **string**: List of comma separated keys that will be used to call this
    tool when the keypress event of *self.figure.canvas* is emited
    """

    description = None
    """Description of the Tool

    **string**: If the Tool is included in the Toolbar this text is used
    as a Tooltip
    """

    image = None
    """Filename of the image

    **string**: Filename of the image to use in the toolbar. If None, the
    `name` is used as a label in the toolbar button
    """

    intoolbar = True
    """Add the tool to the toolbar"""

    cursor = None
    """Cursor to use when the tool is active"""

    def __init__(self, figure, event=None):
        self.figure = None
        self.navigation = None
        self.set_figure(figure)
        self.trigger(event)

    def trigger(self, event):
        """Called when this tool gets used

        Parameters
        ----------
        event : `Event`
            The event that caused this tool to be called
        """

        pass

    def set_figure(self, figure):
        """Set the figure and navigation

        Set the figure to be affected by this tool

        Parameters
        ----------
        figure : `Figure`
        """

        self.figure = figure
        self.navigation = figure.canvas.manager.navigation


class ToolPersistentBase(ToolBase):
    """Persisten tool

    Persistent Tools are keept alive after their initialization,
    a reference of the instance is kept by `navigation`.

    Notes
    -----
    The difference with `ToolBase` is that `trigger` method
    is not called automatically at initialization
    """

    def __init__(self, figure, name, event=None):
        self._name = name
        self.figure = None
        self.navigation = None
        self.set_figure(figure)
        # persistent tools don't call trigger a at instantiation
        # it will be called by Navigation

    def unregister(self, *args):
        """Unregister the tool from the instances of Navigation

        It is usually called by during destroy if it is a
        graphical Tool.

        If the reference in navigation was the last reference
        to the instance of the tool, it will be garbage collected
        """

        # call this to unregister from navigation
        self.navigation.unregister(self._name)


class ToolToggleBase(ToolPersistentBase):
    """Toggleable tool

    This tool is a Persistent Tool that has a toggled state.
    Every time it is triggered, it switches between enable and disable
    """

    _toggled = False

    def trigger(self, event):
        if self._toggled:
            self.disable(event)
        else:
            self.enable(event)
        self._toggled = not self._toggled

    def enable(self, event=None):
        """Enable the toggle tool

        This method is called when the tool is triggered and not toggled
        """

        pass

    def disable(self, event=None):
        """Disable the toggle tool

        This method is called when the tool is triggered and toggled.
         * Second click on the toolbar tool button
         * Another toogle tool is triggered (from the same `navigation`)
        """

        pass

    @property
    def toggled(self):
        """State of the toggled tool"""

        return self._toggled


class ToolQuit(ToolBase):
    """Tool to call the figure manager destroy method"""

    intoolbar = False
    description = 'Quit the figure'
    keymap = rcParams['keymap.quit']

    def trigger(self, event):
        Gcf.destroy_fig(self.figure)


class ToolEnableAllNavigation(ToolBase):
    """Tool to enable all axes for navigation interaction"""

    intoolbar = False
    description = 'Enables all axes navigation'
    keymap = rcParams['keymap.all_axes']

    def trigger(self, event):
        if event.inaxes is None:
            return

        for a in self.figure.get_axes():
            if event.x is not None and event.y is not None \
                    and a.in_axes(event):
                a.set_navigate(True)


class ToolEnableNavigation(ToolBase):
    """Tool to enable a specific axes for navigation interaction"""

    intoolbar = False
    description = 'Enables one axes navigation'
    keymap = (1, 2, 3, 4, 5, 6, 7, 8, 9)

    def trigger(self, event):
        if event.inaxes is None:
            return

        n = int(event.key) - 1
        for i, a in enumerate(self.figure.get_axes()):
            # consider axes, in which the event was raised
            # FIXME: Why only this axes?
            if event.x is not None and event.y is not None \
                    and a.in_axes(event):
                    a.set_navigate(i == n)


class ToolToggleGrid(ToolBase):
    """Tool to toggle the grid of the figure"""

    intoolbar = False
    description = 'Toogle Grid'
    keymap = rcParams['keymap.grid']

    def trigger(self, event):
        if event.inaxes is None:
            return
        event.inaxes.grid()
        self.figure.canvas.draw()


class ToolToggleFullScreen(ToolBase):
    """Tool to toggle full screen"""

    intoolbar = False
    description = 'Toogle Fullscreen mode'
    keymap = rcParams['keymap.fullscreen']

    def trigger(self, event):
        self.figure.canvas.manager.full_screen_toggle()


class ToolToggleYScale(ToolBase):
    """Tool to toggle between linear and logarithmic the Y axis"""

    description = 'Toogle Scale Y axis'
    keymap = rcParams['keymap.yscale']
    intoolbar = False

    def trigger(self, event):
        ax = event.inaxes
        if ax is None:
            return

        scale = ax.get_yscale()
        if scale == 'log':
            ax.set_yscale('linear')
            ax.figure.canvas.draw()
        elif scale == 'linear':
            ax.set_yscale('log')
            ax.figure.canvas.draw()


class ToolToggleXScale(ToolBase):
    """Tool to toggle between linear and logarithmic the X axis"""

    description = 'Toogle Scale X axis'
    keymap = rcParams['keymap.xscale']
    intoolbar = False

    def trigger(self, event):
        ax = event.inaxes
        if ax is None:
            return

        scalex = ax.get_xscale()
        if scalex == 'log':
            ax.set_xscale('linear')
            ax.figure.canvas.draw()
        elif scalex == 'linear':
            ax.set_xscale('log')
            ax.figure.canvas.draw()


class ViewsPositionsMixin(object):
    views = WeakKeyDictionary()
    positions = WeakKeyDictionary()

    def init_vp(self):
        if self.figure not in self.views:
            self.views[self.figure] = cbook.Stack()
            self.positions[self.figure] = cbook.Stack()
            # Define Home
            self.push_current()

    @classmethod
    def clear(cls, figure):
        """Reset the axes stack"""
        if figure in cls.views:
            cls.views[figure].clear()
            cls.positions[figure].clear()

    def update_view(self):
        """Update the viewlim and position from the view and
        position stack for each axes
        """

        lims = self.views[self.figure]()
        if lims is None:
            return
        pos = self.positions[self.figure]()
        if pos is None:
            return
        for i, a in enumerate(self.figure.get_axes()):
            xmin, xmax, ymin, ymax = lims[i]
            a.set_xlim((xmin, xmax))
            a.set_ylim((ymin, ymax))
            # Restore both the original and modified positions
            a.set_position(pos[i][0], 'original')
            a.set_position(pos[i][1], 'active')

        self.figure.canvas.draw_idle()

    def push_current(self):
        """push the current view limits and position onto the stack"""

        lims = []
        pos = []
        for a in self.figure.get_axes():
            xmin, xmax = a.get_xlim()
            ymin, ymax = a.get_ylim()
            lims.append((xmin, xmax, ymin, ymax))
            # Store both the original and modified positions
            pos.append((
                a.get_position(True).frozen(),
                a.get_position().frozen()))
        self.views[self.figure].push(lims)
        self.positions[self.figure].push(pos)

    def refresh_locators(self):
        """Redraw the canvases, update the locators"""
        for a in self.figure.get_axes():
            xaxis = getattr(a, 'xaxis', None)
            yaxis = getattr(a, 'yaxis', None)
            zaxis = getattr(a, 'zaxis', None)
            locators = []
            if xaxis is not None:
                locators.append(xaxis.get_major_locator())
                locators.append(xaxis.get_minor_locator())
            if yaxis is not None:
                locators.append(yaxis.get_major_locator())
                locators.append(yaxis.get_minor_locator())
            if zaxis is not None:
                locators.append(zaxis.get_major_locator())
                locators.append(zaxis.get_minor_locator())

            for loc in locators:
                loc.refresh()
        self.figure.canvas.draw_idle()

    def home(self):
        self.views[self.figure].home()
        self.positions[self.figure].home()

    def back(self):
        self.views[self.figure].back()
        self.positions[self.figure].back()

    def forward(self):
        self.views[self.figure].forward()
        self.positions[self.figure].forward()


def clear_views_positions(figure):
    ViewsPositionsMixin.clear(figure)


class ViewsPositionsBase(ViewsPositionsMixin, ToolBase):
    # Simple base to avoid repeating code on Home, Back and Forward
    _on_trigger = None

    def set_figure(self, *args):
        ToolBase.set_figure(self, *args)
        self.init_vp()

    def trigger(self, *args):
        getattr(self, self._on_trigger)()
        self.update_view()


class ToolHome(ViewsPositionsBase):
    """Restore the original view"""

    description = 'Reset original view'
    image = 'home.png'
    keymap = rcParams['keymap.home']
    _on_trigger = 'home'


class ToolBack(ViewsPositionsBase):
    """move back up the view lim stack"""

    description = 'Back to  previous view'
    image = 'back.png'
    keymap = rcParams['keymap.back']
    _on_trigger = 'back'


class ToolForward(ViewsPositionsBase):
    """Move forward in the view lim stack"""

    description = 'Forward to next view'
    image = 'forward.png'
    keymap = rcParams['keymap.forward']
    _on_trigger = 'forward'


class ConfigureSubplotsBase(ToolPersistentBase):
    """Base tool for the configuration of subplots"""

    description = 'Configure subplots'
    image = 'subplots.png'


class SaveFigureBase(ToolBase):
    """Base tool for figure saving"""

    description = 'Save the figure'
    image = 'filesave.png'
    keymap = rcParams['keymap.save']


class ZoomPanBase(ViewsPositionsMixin, ToolToggleBase):
    def __init__(self, *args):
        ToolToggleBase.__init__(self, *args)
        self.init_vp()
        self._button_pressed = None
        self._xypress = None
        self._idPress = None
        self._idRelease = None

    def enable(self, event):
        self.figure.canvas.widgetlock(self)
        self._idPress = self.figure.canvas.mpl_connect(
            'button_press_event', self._press)
        self._idRelease = self.figure.canvas.mpl_connect(
            'button_release_event', self._release)

    def disable(self, event):
        self._cancel_action()
        self.figure.canvas.widgetlock.release(self)
        self.figure.canvas.mpl_disconnect(self._idPress)
        self.figure.canvas.mpl_disconnect(self._idRelease)


class ToolZoom(ZoomPanBase):
    """Zoom to rectangle"""

    description = 'Zoom to rectangle'
    image = 'zoom_to_rect.png'
    keymap = rcParams['keymap.zoom']
    cursor = cursors.SELECT_REGION

    def __init__(self, *args):
        ZoomPanBase.__init__(self, *args)
        self._ids_zoom = []

    def _cancel_action(self):
        for zoom_id in self._ids_zoom:
            self.figure.canvas.mpl_disconnect(zoom_id)
        self.navigation.remove_rubberband(None, self)
        self.refresh_locators()
        self._xypress = None
        self._button_pressed = None
        self._ids_zoom = []
        return

    def _press(self, event):
        """the _press mouse button in zoom to rect mode callback"""

        # If we're already in the middle of a zoom, pressing another
        # button works to "cancel"
        if self._ids_zoom != []:
            self._cancel_action()

        if event.button == 1:
            self._button_pressed = 1
        elif event.button == 3:
            self._button_pressed = 3
        else:
            self._cancel_action()
            return

        x, y = event.x, event.y

        self._xypress = []
        for i, a in enumerate(self.figure.get_axes()):
            if (x is not None and y is not None and a.in_axes(event) and
                    a.get_navigate() and a.can_zoom()):
                self._xypress.append((x, y, a, i, a.viewLim.frozen(),
                                      a.transData.frozen()))

        id1 = self.figure.canvas.mpl_connect(
            'motion_notify_event', self._mouse_move)
        id2 = self.figure.canvas.mpl_connect(
            'key_press_event', self._switch_on_zoom_mode)
        id3 = self.figure.canvas.mpl_connect(
            'key_release_event', self._switch_off_zoom_mode)

        self._ids_zoom = id1, id2, id3
        self._zoom_mode = event.key

    def _switch_on_zoom_mode(self, event):
        self._zoom_mode = event.key
        self._mouse_move(event)

    def _switch_off_zoom_mode(self, event):
        self._zoom_mode = None
        self._mouse_move(event)

    def _mouse_move(self, event):
        """the drag callback in zoom mode"""

        if self._xypress:
            x, y = event.x, event.y
            lastx, lasty, a, _ind, _lim, _trans = self._xypress[0]

            # adjust x, last, y, last
            x1, y1, x2, y2 = a.bbox.extents
            x, lastx = max(min(x, lastx), x1), min(max(x, lastx), x2)
            y, lasty = max(min(y, lasty), y1), min(max(y, lasty), y2)

            if self._zoom_mode == "x":
                x1, y1, x2, y2 = a.bbox.extents
                y, lasty = y1, y2
            elif self._zoom_mode == "y":
                x1, y1, x2, y2 = a.bbox.extents
                x, lastx = x1, x2

            self.navigation.draw_rubberband(event, self, x, y, lastx, lasty)

    def _release(self, event):
        """the release mouse button callback in zoom to rect mode"""

        for zoom_id in self._ids_zoom:
            self.figure.canvas.mpl_disconnect(zoom_id)
        self._ids_zoom = []

        if not self._xypress:
            self._cancel_action()
            return

        last_a = []

        for cur_xypress in self._xypress:
            x, y = event.x, event.y
            lastx, lasty, a, _ind, lim, _trans = cur_xypress
            # ignore singular clicks - 5 pixels is a threshold
            if abs(x - lastx) < 5 or abs(y - lasty) < 5:
                self._cancel_action()
                return

            x0, y0, x1, y1 = lim.extents

            # zoom to rect
            inverse = a.transData.inverted()
            lastx, lasty = inverse.transform_point((lastx, lasty))
            x, y = inverse.transform_point((x, y))
            Xmin, Xmax = a.get_xlim()
            Ymin, Ymax = a.get_ylim()

            # detect twinx,y axes and avoid double zooming
            twinx, twiny = False, False
            if last_a:
                for la in last_a:
                    if a.get_shared_x_axes().joined(a, la):
                        twinx = True
                    if a.get_shared_y_axes().joined(a, la):
                        twiny = True
            last_a.append(a)

            if twinx:
                x0, x1 = Xmin, Xmax
            else:
                if Xmin < Xmax:
                    if x < lastx:
                        x0, x1 = x, lastx
                    else:
                        x0, x1 = lastx, x
                    if x0 < Xmin:
                        x0 = Xmin
                    if x1 > Xmax:
                        x1 = Xmax
                else:
                    if x > lastx:
                        x0, x1 = x, lastx
                    else:
                        x0, x1 = lastx, x
                    if x0 > Xmin:
                        x0 = Xmin
                    if x1 < Xmax:
                        x1 = Xmax

            if twiny:
                y0, y1 = Ymin, Ymax
            else:
                if Ymin < Ymax:
                    if y < lasty:
                        y0, y1 = y, lasty
                    else:
                        y0, y1 = lasty, y
                    if y0 < Ymin:
                        y0 = Ymin
                    if y1 > Ymax:
                        y1 = Ymax
                else:
                    if y > lasty:
                        y0, y1 = y, lasty
                    else:
                        y0, y1 = lasty, y
                    if y0 > Ymin:
                        y0 = Ymin
                    if y1 < Ymax:
                        y1 = Ymax

            if self._button_pressed == 1:
                if self._zoom_mode == "x":
                    a.set_xlim((x0, x1))
                elif self._zoom_mode == "y":
                    a.set_ylim((y0, y1))
                else:
                    a.set_xlim((x0, x1))
                    a.set_ylim((y0, y1))
            elif self._button_pressed == 3:
                if a.get_xscale() == 'log':
                    alpha = np.log(Xmax / Xmin) / np.log(x1 / x0)
                    rx1 = pow(Xmin / x0, alpha) * Xmin
                    rx2 = pow(Xmax / x0, alpha) * Xmin
                else:
                    alpha = (Xmax - Xmin) / (x1 - x0)
                    rx1 = alpha * (Xmin - x0) + Xmin
                    rx2 = alpha * (Xmax - x0) + Xmin
                if a.get_yscale() == 'log':
                    alpha = np.log(Ymax / Ymin) / np.log(y1 / y0)
                    ry1 = pow(Ymin / y0, alpha) * Ymin
                    ry2 = pow(Ymax / y0, alpha) * Ymin
                else:
                    alpha = (Ymax - Ymin) / (y1 - y0)
                    ry1 = alpha * (Ymin - y0) + Ymin
                    ry2 = alpha * (Ymax - y0) + Ymin

                if self._zoom_mode == "x":
                    a.set_xlim((rx1, rx2))
                elif self._zoom_mode == "y":
                    a.set_ylim((ry1, ry2))
                else:
                    a.set_xlim((rx1, rx2))
                    a.set_ylim((ry1, ry2))

        self._zoom_mode = None
        self.push_current()
        self._cancel_action()


class ToolPan(ZoomPanBase):
    """Pan axes with left mouse, zoom with right"""

    keymap = rcParams['keymap.pan']
    description = 'Pan axes with left mouse, zoom with right'
    image = 'move.png'
    cursor = cursors.MOVE

    def __init__(self, *args):
        ZoomPanBase.__init__(self, *args)
        self._idDrag = None

    def _cancel_action(self):
        self._button_pressed = None
        self._xypress = []
        self.figure.canvas.mpl_disconnect(self._idDrag)
        self.navigation.messagelock.release(self)
#         self.navigation.draw()
        self.refresh_locators()

    def _press(self, event):
        if event.button == 1:
            self._button_pressed = 1
        elif event.button == 3:
            self._button_pressed = 3
        else:
            self._cancel_action()
            return

        x, y = event.x, event.y

        self._xypress = []
        for i, a in enumerate(self.figure.get_axes()):
            if (x is not None and y is not None and a.in_axes(event) and
                    a.get_navigate() and a.can_pan()):
                a.start_pan(x, y, event.button)
                self._xypress.append((a, i))
                self.navigation.messagelock(self)
                self._idDrag = self.figure.canvas.mpl_connect(
                    'motion_notify_event', self._mouse_move)

    def _release(self, event):
        if self._button_pressed is None:
            self._cancel_action()
            return

        self.figure.canvas.mpl_disconnect(self._idDrag)
        self.navigation.messagelock.release(self)

        for a, _ind in self._xypress:
            a.end_pan()
        if not self._xypress:
            self._cancel_action()
            return

#         self.navigation.push_current()
        self.push_current()
        self._cancel_action()

    def _mouse_move(self, event):
        for a, _ind in self._xypress:
            # safer to use the recorded button at the _press than current
            # button: # multiple button can get pressed during motion...
            a.drag_pan(self._button_pressed, event.key, event.x, event.y)
        self.navigation.canvas.draw_idle()


tools = (('Grid', ToolToggleGrid),
         ('Fullscreen', ToolToggleFullScreen),
         ('Quit', ToolQuit),
         ('EnableAll', ToolEnableAllNavigation),
         ('EnableOne', ToolEnableNavigation),
         ('XScale', ToolToggleXScale),
         ('YScale', ToolToggleYScale),
         ('Home', ToolHome),
         ('Back', ToolBack),
         ('Forward', ToolForward),
         ('Spacer1', None),
         ('Zoom', ToolZoom),
         ('Pan', ToolPan),
         ('Spacer2', None),
         ('Subplots', 'ConfigureSubplots'),
         ('Save', 'SaveFigure'))
"""Default tools"""
