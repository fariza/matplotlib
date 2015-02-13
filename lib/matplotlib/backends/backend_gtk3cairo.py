from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

from . import backend_gtk3
from . import backend_cairo
from .backend_cairo import cairo, HAS_CAIRO_CFFI
from matplotlib.figure import Figure
import weakref
from matplotlib import rcParams


class RendererGTK3Cairo(backend_cairo.RendererCairo):
    def set_context(self, ctx):
        if HAS_CAIRO_CFFI:
            ctx = cairo.Context._from_pointer(
                cairo.ffi.cast(
                    'cairo_t **',
                    id(ctx) + object.__basicsize__)[0],
                incref=True)

        self.gc.ctx = ctx


class FigureCanvasGTK3Cairo(backend_gtk3.FigureCanvasGTK3,
                            backend_cairo.FigureCanvasCairo):
    def __init__(self, figure):
        backend_gtk3.FigureCanvasGTK3.__init__(self, figure)

    def _renderer_init(self):
        """use cairo renderer"""
        self._renderer = RendererGTK3Cairo(self.figure.dpi)

    def _render_figure(self, width, height):
        self._renderer.set_width_height (width, height)
        self.figure.draw (self._renderer)

    def on_draw_event(self, widget, ctx):
        """ GtkDrawable draw event, like expose_event in GTK 2.X
        """
        # the _need_redraw flag doesnt work. it sometimes prevents
        # the rendering and leaving the canvas blank
        #if self._need_redraw:
        self._renderer.set_context(ctx)
        allocation = self.get_allocation()
        x, y, w, h = allocation.x, allocation.y, allocation.width, allocation.height
        self._render_figure(w, h)
        #self._need_redraw = False

        return False  # finish event propagation?


class FigureManagerGTK3Cairo(backend_gtk3.FigureManagerGTK3):
    pass


class _a(object):
    pass

last_manager = weakref.ref(_a())


def new_figure_manager(num, *args, **kwargs):
    """
    Create a new figure manager instance
    """
    manager = None
    if rcParams['backend.multifigure']:
        manager = kwargs.pop('manager', None)
        if manager is None:
            manager = last_manager()
    FigureClass = kwargs.pop('FigureClass', Figure)
    thisFig = FigureClass(*args, **kwargs)
    return new_figure_manager_given_figure(num, thisFig, manager)


def new_figure_manager_given_figure(num, figure, manager):
    """
    Create a new figure manager instance for the given figure.
    """
    global last_manager
    canvas = FigureCanvasGTK3Cairo(figure)
    if manager:
        manager.add_canvas(canvas, num)
    else:
        manager = FigureManagerGTK3Cairo(canvas, num)
    last_manager = weakref.ref(manager)
    return manager


FigureCanvas = FigureCanvasGTK3Cairo
FigureManager = FigureManagerGTK3Cairo
show = backend_gtk3.show
