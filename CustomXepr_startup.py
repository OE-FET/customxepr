# system imports
import sys
import os
import logging
from qtpy import QtCore, QtWidgets

# custom imports
from XeprTools import CustomXepr, JobStatusApp, InternalIPKernel
from XeprTools.CustomXepr import __version__, __author__
from MercuryGUI import MercuryFeed, MercuryMonitorApp
from Keithley import Keithley, KeithleyGuiApp
from HelpFunctions import applyDarkTheme

try:
    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic("%autoreload 0")
    
except ImportError:
    pass

try:
    sys.path.insert(0, os.popen("Xepr --apipath").read())
    import XeprAPI
except ImportError:
    logging.info('XeprAPI could not be located. Please make sure that it is ' +
                 'installed on your system.')

DARK = True
KEITHLEY_IP = '192.168.2.121'
MERCURY_IP = '172.20.91.43'


BANNER = ('Welcome to CustomXepr %s. ' % __version__ +
          'You can access connected instruments as ' +
          '"customXepr", "mercuryFeed" and "keithley".\n\n' +
          'Use "%run path_to_file.py" to run a python script such as a ' +
          'measurement routine.\n'
          'Execute "goDark()" or "goBright()" to switch the user interface ' +
          'style. Type "exit" to gracefully exit CustomXepr.\n\n' +
          '(c) 2016 - 2018, %s.' % __author__)


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
# Connect to instruments: Bruker Xepr, Keithley and MercuryiTC.
# =============================================================================

def connectToInstruments(keithleyIP=KEITHLEY_IP, mercuryIP=MERCURY_IP):
    """Tries to connect to Keithley, Mercury and Xepr."""

    keithley = Keithley(keithleyIP)
    mercuryFeed = MercuryFeed(mercuryIP)

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
    # create the user interfaces
    customXeprGUI = JobStatusApp(customXepr)
    customXeprGUI.show()

    keithleyGUI = KeithleyGuiApp(keithley)
    keithleyGUI.show()

    mercuryGUI = MercuryMonitorApp(mercuryFeed)
    mercuryGUI.show()

    return customXeprGUI, mercuryGUI, keithleyGUI


# =============================================================================
# Go dark! (not yet supported for standalone console)
# =============================================================================

def goDark():
    applyDarkTheme.goDark()
    applyDarkTheme.applyMPLDarkTheme()


def goBright():
    applyDarkTheme.goBright()
    applyDarkTheme.applyMPLBrightTheme()


# =============================================================================
# Monkeypatch exception hook to get errors from Qt event loop in Jupyter
# =============================================================================

def patch_excepthook():

    from traceback import format_exception

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

    # Create a new Qt app or return an existing one.
    app, created = getQtApp()
    if not created:
        patch_excepthook()

    # connect to instruments
    customXepr, mercuryFeed, keithley, xepr = connectToInstruments()
    # start user interfaces
    customXeprGUI, mercuryGUI, keithleyGUI = startGUI(customXepr, mercuryFeed,
                                                      keithley)

    if DARK:
        goDark()
        console_style = 'base16_ocean_dark'
    else:
        console_style = ''


    if created:
        # start event loop and console if run as standalone app
        kernel_window = InternalIPKernel()
        kernel_window.init_ipkernel(banner=BANNER)

        kernel_window.new_qt_console(style=console_style)

        varDict = {'customXepr': customXepr, 'xepr': xepr,
                   'customXeprGUI': customXeprGUI,
                   'mercuryFeed': mercuryFeed, 'mercuryGUI': mercuryGUI,
                   'keithley': keithley, 'keithleyGUI': keithleyGUI,
                   'goDark': goDark, 'goBright': goBright}

        kernel_window.send_to_namespace(varDict)
        app.aboutToQuit.connect(kernel_window.cleanup_consoles)
        kernel_window.ipkernel.start()

    else:
        # only print BANNER if started from running Jupyter console
        # (e.g. from Spyder)
        print(BANNER)
