"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

To Do:

* See GitHub issues list at https://github.com/OE-FET/CustomXepr

New in v1.5.0:

    See release notes

"""
# system imports
import sys
import os
import logging
from qtpy import QtCore, QtWidgets, QtGui
from traceback import format_exception

# local imports
from Config.main import CONF
from XeprTools import CustomXepr
from MercuryGUI import MercuryFeed, MercuryMonitorApp
from KeithleyDriver import Keithley2600
from XeprTools import JobStatusApp, InternalIPKernel
from XeprTools.CustomXepr import __version__, __author__
from Keithley import KeithleyGuiApp
from Utils import check_dependencies, applyDarkTheme, get_dark_style

# check if all require packages are installed
direct = os.path.dirname(os.path.realpath(__file__))
filePath = os.path.join(direct, 'dependencies.txt')
exit_code = check_dependencies(filePath)

# if we are running from IPython, disable autoreload
try:
    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic("%autoreload 0")
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

def getQtApp(*args, **kwargs):
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

def showSplashScreen(app):
    """ Shows a splash screen from file."""

    image = QtGui.QPixmap(os.path.join(direct, 'Images/CustomXeprSplash.png'))
    image.setDevicePixelRatio(3)
    splash = QtWidgets.QSplashScreen(image)
    splash.show()
    app.processEvents()

    return splash


# =============================================================================
# Connect to instruments: Bruker Xepr, Keithley and MercuryiTC.
# =============================================================================

def connectToInstruments(keithleyIP=KEITHLEY_IP, mercuryIP=MERCURY_IP,
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

def startGUI(customXepr, mercuryFeed, keithley):
    """Starts GUIs for Keithley, Mercury and CustomXepr."""

    customXeprGUI = JobStatusApp(customXepr)
    mercuryGUI = MercuryMonitorApp(mercuryFeed)
    keithleyGUI = KeithleyGuiApp(keithley)

    customXeprGUI.show()
    mercuryGUI.show()
    keithleyGUI.show()

    return customXeprGUI, mercuryGUI, keithleyGUI


# =============================================================================
# Go dark! (not yet supported for standalone console)
# =============================================================================

def goDark():
    applyDarkTheme.goDark()
    applyDarkTheme.applyMPLDarkTheme()

    CONF.set('main', 'DARK', True)


def goBright():
    applyDarkTheme.goBright()
    applyDarkTheme.applyMPLBrightTheme()

    CONF.set('main', 'DARK', False)


# =============================================================================
# Monkeypatch exception hook to get errors from Qt event loop in Jupyter
# =============================================================================

def patch_excepthook():

    global TIMER

    def new_except_hook(etype, evalue, tb):
        QtWidgets.QMessageBox.warning(None, 'error',
                                      ''.join(format_exception(etype,
                                                               evalue, tb)))

    def _patch_excepthook():
        sys.excepthook = new_except_hook

    TIMER = QtCore.QTimer()
    TIMER.setSingleShot(True)
    TIMER.timeout.connect(_patch_excepthook)
    TIMER.start()


if __name__ == '__main__':

    # create a new Qt app or return an existing one
    app, created = getQtApp()
    if not created:
        patch_excepthook()

    # create and show splash screen
    splash = showSplashScreen(app)

    # apply dark theme
    if DARK:
        applyDarkTheme.goDark()

    # connect to instruments
    customXepr, mercuryFeed, keithley, xepr = connectToInstruments()
    # start user interfaces
    customXeprGUI, mercuryGUI, keithleyGUI = startGUI(customXepr, mercuryFeed,
                                                      keithley)

    # reinforce dark theme for figures
    if DARK:
        applyDarkTheme.applyMPLDarkTheme()

    BANNER = ('Welcome to CustomXepr %s. ' % __version__ +
              'You can access connected instruments as ' +
              '"customXepr", "mercuryFeed" and "keithley".\n\n' +
              'Use "%run path_to_file.py" to run a python script such as a ' +
              'measurement routine.\n'
              'Execute "goDark()" or "goBright()" to switch the user ' +
              'interface style. Type "exit" to gracefully exit ' +
              'CustomXepr.\n\n(c) 2016 - 2018, %s.' % __author__)

    if created:

        # start event loop and console if run as standalone app
        kernel_window = InternalIPKernel()
        kernel_window.init_ipkernel(banner=BANNER)

        if DARK:
            console_style = get_dark_style()
        else:
            console_style = ''

        kernel_window.new_qt_console(style=console_style)

        varDict = {'customXepr': customXepr, 'xepr': xepr,
                   'customXeprGUI': customXeprGUI,
                   'mercuryFeed': mercuryFeed, 'mercuryGUI': mercuryGUI,
                   'keithley': keithley, 'keithleyGUI': keithleyGUI,
                   'goDark': goDark, 'goBright': goBright}

        kernel_window.send_to_namespace(varDict)
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
