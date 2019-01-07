"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import
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

# local imports
from customxepr.utils.misc import patch_excepthook
from customxepr.customxepr import CustomXepr, __version__, __author__, __year__
from customxepr.customxper_ui import JobStatusApp

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
    image = QtGui.QPixmap(os.path.join(direct, 'resources', 'splash.png'))
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


def run():

    # create a new Qt app or return an existing one
    app, CREATED = get_qt_app()

    # create and show splash screen
    splash = show_splash_screen(app)

    # connect to instruments
    customXepr, xepr, keithley, mercury, mercuryfeed = connect_to_instruments()
    # start user interfaces
    customXepr_gui, keithley_gui, mercury_gui = start_gui(customXepr,
                                                          mercuryfeed,
                                                          keithley)

    BANNER = ('Welcome to CustomXepr %s. ' % __version__ +
              'You can access connected instruments through "customXepr" ' +
              'or directly as "xepr", "keithley" and "mercury".\n\n' +
              'Use "%run path/to/file.py" to run a python script such as a ' +
              'measurement routine.\n'
              'Type "exit" to gracefully exit ' +
              'CustomXepr.\n\n(c) 2016 - %s, %s.' % (__year__, __author__))

    if CREATED:

        from customxepr.utils.internal_ipkernel import InternalIPKernel

        # start event loop and console if run as a standalone app
        kernel_window = InternalIPKernel(banner=BANNER)
        kernel_window.new_qt_console()

        var_dict = {'customXepr': customXepr, 'xepr': xepr,
                    'customXepr_gui': customXepr_gui, 'mercury': mercury,
                    'mercuryfeed': mercuryfeed, 'mercury_gui': mercury_gui,
                    'keithley': keithley, 'keithley_gui': keithley_gui}

        kernel_window.send_to_namespace(var_dict)
        app.aboutToQuit.connect(kernel_window.cleanup_consoles)
        # remove splash screen
        splash.finish(keithley_gui)
        # patch exception hook to display errors from Qt event loop
        patch_excepthook()
        # start event loop
        kernel_window.ipkernel.start()

    else:
        # print banner
        print(BANNER)
        # remove splash screen
        splash.finish(customXepr_gui)
        # patch exception hook to display errors from Qt event loop
        patch_excepthook()

        return (customXepr, xepr, mercury, mercuryfeed, keithley,
                customXepr_gui, keithley_gui, mercury_gui)


if __name__ == '__main__':
    customXepr, xepr, mercury, mercuryfeed, keithley, customXepr_gui, keithley_gui, mercury_gui = run()
