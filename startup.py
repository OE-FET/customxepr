"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

To Do:

* See GitHub issues list at https://github.com/OE-FET/CustomXepr

New in v2.2:
    * Window position and size is saved and restored between sessions.

New in v2.1.:
    * Included revamped keithleygui with IV sweep functionality.
    * Proper disconnection from instruments when closing windows or shutting
      down the console with "exit" command.
    * Fixed a bug that would prevent Xepr experiments to run if the measurement
      time cannot be estimated. Applies for instance to rapid scan and time
      domain measurements where proper ETA estimates have not yet been
      implemented.

New in v2.1.0:
    * Removed dark theme: code is easier to maintain.
    * Split off mercury_gui and keithley_gui as separate packages.
    * Warnings when invalid file paths are handed to Xepr.

New in v2.0.0:

    * Moved driver backends from NI-VISA to pyvisa-py. It is no longer
      necessary to install NI-VISA from National Instruments on your system.
    * Moved drivers to external packages. Install with pip before first use.
    * Improved data plotting in Mercury user interface:
        - heater output and gasflow are plotted alongside the temperature
        - major speedups in plotting framerate by relying on numpy for updating
          the data, redrawing only changed elements of plot widget
        - allow real-time panning and zooming of plots
    * Started working on Python 3.6 compatability.

"""
import logging
import os
import sys

from IPython import get_ipython
from keithley2600 import Keithley2600
from keithleygui import CONF as KCONF
from keithleygui import KeithleyGuiApp
from mercurygui import CONF as MCONF
from mercurygui import MercuryFeed, MercuryMonitorApp
from mercuryitc import MercuryITC
from qtpy import QtCore, QtWidgets, QtGui

from utils.misc import patch_excepthook
# local imports
from xeprtools.customxepr import CustomXepr, __version__, __author__, __year__
from xeprtools.customxper_ui import JobStatusApp

try:
    sys.path.insert(0, os.popen("Xepr --apipath").read())
    import XeprAPI
except ImportError:
    XeprAPI = None
    logging.info('XeprAPI could not be located. Please make sure that it' +
                 ' is installed on your system.')

# if we are running from IPython:
# start integrated Qt event loop, disable autoreload
ipython = get_ipython()
if ipython:
    ipython.magic('%gui qt')
    ipython.magic('%load_ext autoreload')
    ipython.magic('%autoreload 0')
    app = QtWidgets.QApplication([' '])

KEITHLEY_ADDRESS = KCONF.get('Connection', 'VISA_ADDRESS')
KEITHLEY_VISA_LIB = KCONF.get('Connection', 'VISA_LIBRARY')
MERCURY_ADDRESS = MCONF.get('Connection', 'VISA_ADDRESS')
MERCURY_VISA_LIB = MCONF.get('Connection', 'VISA_LIBRARY')


# =============================================================================
# Set up Qt event loop and console if necessary
# =============================================================================

def get_qt_app(*args, **kwargs):
    """
    Create a new Qt app or return an existing one.
    """
    created = False
    app = QtCore.QCoreApplication.instance()

    if not app:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
        created = True

    return app, created


# =============================================================================
# Create splash screen
# =============================================================================

def show_splash_screen(app):
    """ Shows a splash screen from file."""
    direct = os.path.dirname(os.path.realpath(__file__))
    image = QtGui.QPixmap(os.path.join(direct, 'images', 'splash.png'))
    image.setDevicePixelRatio(3)
    splash = QtWidgets.QSplashScreen(image)
    splash.show()
    app.processEvents()

    return splash


# =============================================================================
# Connect to instruments: Bruker Xepr, Keithley and MercuryiTC.
# =============================================================================

def connect_to_instruments():
    """Tries to connect to Keithley, Mercury and Xepr."""

    keithley = Keithley2600(KEITHLEY_ADDRESS, KEITHLEY_VISA_LIB)
    mercury = MercuryITC(MERCURY_ADDRESS, MERCURY_VISA_LIB)
    mercuryfeed = MercuryFeed(mercury)

    try:
        xepr = XeprAPI.Xepr()
    except AttributeError:
        xepr = None
    except IOError:
        logging.info('No running Xepr instance could be found.')
        xepr = None

    customxepr = CustomXepr(xepr, mercuryfeed, keithley)

    return customxepr, xepr, keithley, mercury, mercuryfeed


# =============================================================================
# Start CustomXepr and user interfaces
# =============================================================================

def start_gui(customxepr, mercuryfeed, keithley):
    """Starts GUIs for Keithley, Mercury and CustomXepr."""

    customxepr_gui = JobStatusApp(customxepr)
    mercury_gui = MercuryMonitorApp(mercuryfeed)
    keithley_gui = KeithleyGuiApp(keithley)

    customxepr_gui.show()
    mercury_gui.show()
    keithley_gui.show()

    return customxepr_gui, keithley_gui, mercury_gui


if __name__ == '__main__':

    # create a new Qt app or return an existing one
    app, CREATED = get_qt_app()

    # create and show splash screen
    splash = show_splash_screen(app)

    # connect to instruments
    customXepr, xepr, keithley, mercury, mercuryfeed = connect_to_instruments()
    # start user interfaces
    customXepr_gui, keithley_gui, mercury_gui = start_gui(customXepr, mercuryfeed,
                                                          keithley)

    BANNER = ('Welcome to CustomXepr %s. ' % __version__ +
              'You can access connected instruments through "customXepr" ' +
              'or directly as "xepr", "keithley" and "mercury".\n\n' +
              'Use "%run path/to/file.py" to run a python script such as a ' +
              'measurement routine.\n'
              'Type "exit" to gracefully exit ' +
              'CustomXepr.\n\n(c) 2016 - %s, %s.' % (__year__, __author__))

    if CREATED:

        from utils.internal_ipkernel import InternalIPKernel

        # start event loop and console if run as standalone app
        kernel_window = InternalIPKernel(banner=BANNER)
        kernel_window.new_qt_console()

        var_dict = {'customXepr': customXepr, 'xepr': xepr,
                    'customXepr_gui': customXepr_gui, 'mercury': mercury,
                    'mercuryfeed': mercuryfeed, 'mercury_gui': mercury_gui,
                    'keithley': keithley, 'keithley_gui': keithley_gui}

        kernel_window.send_to_namespace(var_dict)
        # noinspection PyUnresolvedReferences
        app.aboutToQuit.connect(kernel_window.cleanup_consoles)
        # remove splash screen
        splash.finish(keithley_gui)
        # start event loop
        kernel_window.ipkernel.start()

    else:
        # print banner
        print(BANNER)
        # remove splash screen
        splash.finish(customXepr_gui)
        # patch exception hook to display errors from Qt event loop
        patch_excepthook()
