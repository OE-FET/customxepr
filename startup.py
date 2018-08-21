"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

To Do:

* See GitHub issues list at https://github.com/OE-FET/CustomXepr

New in v2.0.0:

    See release notes

"""
import sys
import os
import logging
from qtpy import QtCore, QtWidgets, QtGui

# local imports
from config.main import CONF
from xeprtools.customxepr import CustomXepr, __version__, __author__
from xeprtools.customxper_ui import JobStatusApp
from mercury_gui.feed import MercuryFeed
from mercury_gui.main import MercuryMonitorApp
from keithley_driver import Keithley2600
from keithley_gui.main import KeithleyGuiApp

from utils import dark_style
from utils.misc import check_dependencies, patch_excepthook
from utils.internal_ipkernel import InternalIPKernel

# check if all require packages are installed
direct = os.path.dirname(os.path.realpath(__file__))
filePath = os.path.join(direct, 'dependencies.txt')
exit_code = check_dependencies(filePath)

# if we are running from IPython:
# disable autoreload, start integrated Qt event loop
try:
    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic('%autoreload 0')
    ipython.magic('%gui qt')
    app = QtWidgets.QApplication([' '])
except:
    pass

try:
    sys.path.insert(0, os.popen("Xepr --apipath").read())
    import XeprAPI
except ImportError:
    logging.info('XeprAPI could not be located. Please make sure that it' +
                 ' is installed on your system.')

DARK = CONF.get('main', 'DARK')
KEITHLEY_IP = CONF.get('Keithley', 'KEITHLEY_IP')
MERCURY_IP = CONF.get('MercuryFeed', 'MERCURY_IP')
MERCURY_PORT = CONF.get('MercuryFeed', 'MERCURY_PORT')


# =============================================================================
# Set up Qt event loop and console if necessary
# =============================================================================

def get_qt_app(*args, **kwargs):
    """
    Create a new Qt app or return an existing one.
    """
    CREATED = False
    app = QtCore.QCoreApplication.instance()

    if not app:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
        CREATED = True

    return app, CREATED


# =============================================================================
# Create splash screen
# =============================================================================

def show_splash_screen(app):
    """ Shows a splash screen from file."""

    image = QtGui.QPixmap(os.path.join(direct, 'images/splash.png'))
    image.setDevicePixelRatio(3)
    splash = QtWidgets.QSplashScreen(image)
    splash.show()
    app.processEvents()

    return splash


# =============================================================================
# Connect to instruments: Bruker Xepr, Keithley and MercuryiTC.
# =============================================================================

def connect_to_instruments(keithleyIP=KEITHLEY_IP, mercuryIP=MERCURY_IP,
                           mercuryPort=MERCURY_PORT):
    """Tries to connect to Keithley, Mercury and Xepr."""

    keithley = Keithley2600(keithleyIP)
    mercuryFeed = MercuryFeed(mercuryIP, mercuryPort)

    try:
        xepr = XeprAPI.Xepr()
    except NameError:
        xepr = None
    except IOError:
        logging.info('No running Xepr instance could be found.')
        xepr = None

    customXepr = CustomXepr(xepr, mercuryFeed, keithley)

    return customXepr, mercuryFeed, keithley, xepr


# =============================================================================
# Start CustomXepr and user interfaces
# =============================================================================

def start_gui(customXepr, mercuryFeed, keithley):
    """Starts GUIs for Keithley, Mercury and CustomXepr."""

    customXeprGUI = JobStatusApp(customXepr)
    mercuryGUI = MercuryMonitorApp(mercuryFeed)
    keithleyGUI = KeithleyGuiApp(keithley)

    customXeprGUI.show()
    mercuryGUI.show()
    keithleyGUI.show()

    return customXeprGUI, mercuryGUI, keithleyGUI


if __name__ == '__main__':

    # create a new Qt app or return an existing one
    app, CREATED = get_qt_app()
    if not CREATED:
        patch_excepthook()

    # create and show splash screen
    splash = show_splash_screen(app)

    # apply dark theme
    if DARK:
        dark_style.go_dark()
    else:
        dark_style.go_bright()

    # connect to instruments
    customXepr, mercuryFeed, keithley, xepr = connect_to_instruments()
    # start user interfaces
    customXeprGUI, mercuryGUI, keithleyGUI = start_gui(customXepr, mercuryFeed,
                                                       keithley)

    # reinforce dark theme for figures
    if DARK:
        dark_style.apply_mpl_dark_theme()
    else:
        dark_style.apply_mpl_bright_theme()

    BANNER = ('Welcome to CustomXepr %s. ' % __version__ +
              'You can access connected instruments as ' +
              '"customXepr", "mercuryFeed" and "keithley".\n\n' +
              'Use "%run path_to_file.py" to run a python script such as a ' +
              'measurement routine.\n'
              'Type "exit" to gracefully exit ' +
              'CustomXepr.\n\n(c) 2016 - 2018, %s.' % __author__)

    if CREATED:

        # start event loop and console if run as standalone app
        kernel_window = InternalIPKernel()
        kernel_window.init_ipkernel(banner=BANNER)

        if DARK:
            console_style = dark_style.get_console_dark_style()
        else:
            console_style = ''

        kernel_window.new_qt_console(style=console_style)

        var_dict = {'customXepr': customXepr, 'xepr': xepr,
                    'customXeprGUI': customXeprGUI,
                    'mercuryFeed': mercuryFeed, 'mercuryGUI': mercuryGUI,
                    'keithley': keithley, 'keithleyGUI': keithleyGUI}

        kernel_window.send_to_namespace(var_dict)
        app.aboutToQuit.connect(kernel_window.cleanup_consoles)
        # remove splash screen
        splash.finish(keithleyGUI)
        # start event loop
        kernel_window.ipkernel.start()

    else:
        # print banner
        print(BANNER)
        # remove splash screen
        splash.finish(customXeprGUI)
