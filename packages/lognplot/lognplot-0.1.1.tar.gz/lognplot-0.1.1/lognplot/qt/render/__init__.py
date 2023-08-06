""" Render a graph on a QPainter. """
import contextlib
from ..qtapi import QtCore, QtGui
from ...chart import Chart
from .render import Renderer
from .layout import ChartLayout
from .options import ChartOptions


def render_chart_on_qpainter(chart: Chart, painter: QtGui.QPainter, layout, options):
    """ Call this function to paint a chart onto the given painter within the rectangle specified.
    """
    renderer = Renderer(painter, chart, layout, options)
    # with bench_it("render"):
    renderer.render()
