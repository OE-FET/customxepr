# -*- coding: utf-8 -*-

import os
import qdarkstyle
import pygments
from qtpy import QtCore, QtGui
import matplotlib as mpl
import shutil


if QtCore.PYQT_VERSION_STR[0] == '5':
    from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg
                                                    as FigureCanvas)
elif QtCore.PYQT_VERSION_STR[0] == '4':
    from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg
                                                    as FigureCanvas)

direct = os.path.dirname(os.path.realpath(__file__))


def get_canvas_list():
    """
    Search for figure canvases in all open windows. Returns a list of canvases
    found.
    """
    app = QtCore.QCoreApplication.instance()
    widgetList = app.topLevelWidgets()

    convasList = []

    for w in widgetList:
        for attr_name, attr_value in w.__dict__.iteritems():
            if type(attr_value) == FigureCanvas:
                convasList.append(attr_value)
    return convasList


def set_label_color(ax, labelColor):
    """Sets color of all labels, titles and borders of axes."""
    ax.spines['bottom'].set_color(labelColor)
    ax.spines['top'].set_color(labelColor)
    ax.spines['left'].set_color(labelColor)
    ax.spines['right'].set_color(labelColor)
    ax.xaxis.label.set_color(labelColor)
    ax.yaxis.label.set_color(labelColor)
    ax.tick_params(axis='both', colors=labelColor)
    ax.title.set_color(labelColor)


def go_dark():
    """ Apply dark theme to all windows and future MPL figures."""
    # apply dark theme to all future figures
    mpl.style.use(os.path.join(direct, 'mpl_dark_style.mplstyle'))

    # apply dark theme to PyQt windows
    if QtCore.PYQT_VERSION_STR[0] == '5':
        os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'
    elif QtCore.PYQT_VERSION_STR[0] == '4':
        os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt4'

    app = QtCore.QCoreApplication.instance()
    app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment())


def apply_mpl_dark_theme():
    """
    Changes appearance of existing matplotlib figures to match qdarkstyle.
    Input argument is a list of canvases.
    """

    canvasList = get_canvas_list()

    labelColor = [1, 1, 1, 0.5]

    for canvas in canvasList:
        fig = canvas.figure
        fig.set_facecolor([49/255.0, 54/255.0, 59/255.0, 1])
        axList = fig.get_axes()
        for ax in axList:
            ax.set_facecolor([0.204, 0.225, 0.246, 1])
            ax.grid(True, color=[0.3, 0.3, 0.3, 1])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            set_label_color(ax, labelColor)

        canvas.draw()


def go_bright():
    """ Apply bright theme to all windows and future MPL figures."""
    mpl.style.use('default')
    app = QtCore.QCoreApplication.instance()
    app.setStyleSheet('')


def apply_mpl_bright_theme():
    """
    Changes appearance of matplotlib current figures to match bright style.
    Input argument is a list of figures.
    """

    canvasList = get_canvas_list()

    color = QtGui.QPalette().window().color().getRgb()
    color = [x/255.0 for x in color]

    labelColor = 'black'

    for canvas in canvasList:
        fig = canvas.figure
        fig.set_facecolor(color)
        axList = fig.get_axes()
        for ax in axList:
            ax.set_facecolor('white')
            ax.grid(False)
            ax.spines['top'].set_visible(True)
            ax.spines['right'].set_visible(True)
            set_label_color(ax, labelColor)

        canvas.draw()


def install_pygemets_style(source_path):
    """Installs pigments style from 'source_path' to pygments style folder."""
    # find pygments path
    pygments_path = os.path.dirname(pygments.__file__)
    style_path = os.path.join(pygments_path, 'styles')

    # copy customxeprdark.py to style_path
    shutil.copy2(source_path, style_path)


def get_console_dark_style():
    """
    Tries to get customxeprdark pygments sytle. if this fails, it tries to
    install the customxeprdark style in the current pygments folder.
    If this fails, it falls back to the 'native' pygments style.
    """
    try:
        pygments.styles.get_style_by_name('ipconsoledark')
        console_style = 'ipconsoledark'
    except pygments.util.ClassNotFound:
        try:
            source_path = os.path.join(direct, 'ipconsoledark.py')
            install_pygemets_style(source_path)
            console_style = 'ipconsoledark'
        except:
            # fall back to pygments default dark style 'native'
            console_style = 'native'

    return console_style
