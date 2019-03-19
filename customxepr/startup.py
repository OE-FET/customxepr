# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import
import os
import logging

from qtpy import QtCore, QtWidgets
from IPython import get_ipython

from customxepr.gui import SplashScreen

ipython = get_ipython()
if ipython:
    # if we are running from IPython start integrated Qt event loop
    ipython.magic('%gui qt')
    app = QtWidgets.QApplication(['CustomXepr'])


# ========================================================================================
# Get or start Qt application instance
# ========================================================================================

def get_qt_app():
    """
    Creates a new Qt application or returns an existing one (for instance if run
    from an IPython console with Qt backend).

    :returns: Tuple (``app``, ``interactive``) where ``interactive`` is `True`
        if run from an interactive jupyter console and `False` otherwise.
    :rtype: (:class:`qtpy.QtWidgets.QApplication`, bool)
    """

    from IPython import get_ipython

    ipython = get_ipython()
    if ipython:
        interactive = True
        # disable autoreload
        ipython.magic('%load_ext autoreload')
        ipython.magic('%autoreload 0')
        os.environ.update(SPY_UMR_ENABLED='False')
        # get app instance
        app = QtWidgets.QApplication.instance()
    else:
        interactive = False
        app = QtWidgets.QApplication(['CustomXepr'])
        app.setApplicationName('CustomXepr')

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    return app, interactive


# ========================================================================================
# Create splash screen
# ========================================================================================

def show_splash_screen():
    """
    Shows the CustomXepr splash screen.

    :returns: :class:`qtpy.QtWidgets.QSplashScreen`.
    """
    splash = SplashScreen()
    splash.show()
    splash.raise_()
    QtWidgets.QApplication.processEvents()
    splash.showMessage("Initializing...")

    return splash


# ========================================================================================
# Connect to instruments: Bruker Xepr, Keithley and MercuryiTC.
# ========================================================================================

def connect_to_instruments():
    """
    Tries to connect to Keithley, Mercury and Xepr. Uses the visa
    addresses saved in the respective configuration files.

    :returns: Tuple containing instrument instances.
    """

    import sys
    from keithley2600 import Keithley2600
    from keithleygui import CONF as KCONF
    from mercuryitc import MercuryITC
    from mercurygui import CONF as MCONF
    from mercurygui import MercuryFeed

    keithley_address = KCONF.get('Connection', 'VISA_ADDRESS')
    keithley_visa_lib = KCONF.get('Connection', 'VISA_LIBRARY')
    mercury_address = MCONF.get('Connection', 'VISA_ADDRESS')
    mercury_visa_lib = MCONF.get('Connection', 'VISA_LIBRARY')

    try:
        sys.path.insert(0, os.popen('Xepr --apipath').read())
        # noinspection PyUnresolvedReferences
        import XeprAPI
        xepr = XeprAPI.Xepr()
    except ImportError:
        logging.info('XeprAPI could not be located.')
        xepr = None
    except IOError:
        logging.info('No running Xepr instance could be found.')
        xepr = None

    mercury = MercuryITC(mercury_address, mercury_visa_lib, open_timeout=1)
    mercury_feed = MercuryFeed(mercury)
    keithley = Keithley2600(keithley_address, keithley_visa_lib, open_timeout=1)

    return xepr, customXepr, mercury, mercury_feed, keithley


# ========================================================================================
# Start CustomXepr and user interfaces
# ========================================================================================

def start_gui(xepr, mercury_feed, keithley):
    """
    Starts GUIs for Keithley, Mercury and CustomXepr.

    :returns: Tuple containing GUI instances.
    """
    from keithleygui import KeithleyGuiApp
    from mercurygui import MercuryMonitorApp
    from customxepr.main import CustomXepr
    from customxepr.gui import CustomXeprGuiApp

    mercury_gui = MercuryMonitorApp(mercury_feed)
    keithley_gui = KeithleyGuiApp(keithley)

    customXepr = CustomXepr(xepr, mercury_feed, keithley)
    customXepr_gui = CustomXeprGuiApp(customXepr)

    mercury_gui.QUIT_ON_CLOSE = False
    keithley_gui.QUIT_ON_CLOSE = False
    customXepr_gui.QUIT_ON_CLOSE = False

    customXepr_gui.show()
    mercury_gui.show()
    keithley_gui.show()

    return customXepr_gui, mercury_gui, keithley_gui


def run():
    """
    Runs CustomXepr -- this is the main entry point. Calling ``run`` will first
    create or retrieve an existing Qt application, then aim to connect to Xepr,
    a Keithley 2600 instrument and a MercuryiTC temperature controller and finally
    create user interfaces to control all three instruments.

    If run from an interactive Jupyter or IPython console with Qt backend, ``run``
    will start an interactive session and return instances of the above instrument
    controllers. Otherwise, it will create its own Jupyter console to receive user input.

    :returns: Tuple containing instrument and GUI instances.
    """

    from customxepr.main import __version__, __author__, __year__
    from customxepr.gui.error_dialog import patch_excepthook

    # create a new Qt app or return an existing one
    app, interactive = get_qt_app()

    # create and show splash screen
    splash = show_splash_screen()

    # connect to instruments
    splash.showMessage("Connecting to instruments...")
    xepr, customXepr, mercury, mercury_feed, keithley = connect_to_instruments()
    # start user interfaces
    splash.showMessage("Loading user interface...")
    customXepr_gui, mercury_gui, keithley_gui = start_gui(xepr, mercury_feed, keithley)

    banner = ('Welcome to CustomXepr %s. ' % __version__ +
              'You can access connected instruments through "customXepr" ' +
              'or directly as "xepr", "keithley" and "mercury".\n\n' +
              'Use "%run -i path/to/file.py" to run a python script such ' +
              'as a measurement routine. '
              'Type "exit" to gracefully exit ' +
              'CustomXepr.\n\n(c) 2016 - %s, %s.' % (__year__, __author__))

    if interactive:
        # print banner
        from IPython import get_ipython
        ipython = get_ipython()
        if ipython:
            ipython.magic('%clear')
        print(banner)

        # patch exception hook to display errors from Qt event loop
        patch_excepthook()

        # remove splash screen
        splash.hide()

        return (customXepr, xepr, mercury, mercury_feed, keithley,
                customXepr_gui, mercury_gui, keithley_gui)

    else:
        splash.showMessage("Loading console...")

        from customxepr.utils.internal_ipkernel import InternalIPKernel

        # start event loop and console if run as a standalone app
        internal_kernel = InternalIPKernel(banner=banner)
        internal_kernel.new_qt_console()

        var_dict = {'customXepr': customXepr, 'xepr': xepr, 'mercury': mercury,
                    'mercury_feed': mercury_feed, 'keithley': keithley,
                    'customXepr_gui': customXepr_gui,
                    'mercury_gui': mercury_gui, 'keithley_gui': keithley_gui,
                    }

        internal_kernel.send_to_namespace(var_dict)
        # noinspection PyUnresolvedReferences
        app.aboutToQuit.connect(internal_kernel.cleanup_consoles)
        # patch exception hook to display errors from Qt event loop
        patch_excepthook()
        # remove splash screen
        splash.hide()
        # start event loop
        internal_kernel.ipkernel.start()


if __name__ == '__main__':
    customXepr, xepr, mercury, mercury_feed, keithley, customXepr_gui, \
        mercury_gui, keithley_gui = run()
