#!/usr/bin/env python3
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
from qtpy import QtCore, QtWidgets, QtGui, uic
from IPython import get_ipython

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
        # get app instance
        app = QtWidgets.QApplication.instance()
    else:
        interactive = False
        app = QtWidgets.QApplication(['CustomXepr'])
        app.setApplicationName('CustomXepr')

    return app, interactive


# ========================================================================================
# Create splash screen
# ========================================================================================

SPLASH_UI_PATH = os.path.join(os.path.dirname(__file__), "splash.ui")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "resources/logo@2x.png")


class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        uic.loadUi(SPLASH_UI_PATH, self)
        pixmap = QtGui.QPixmap(LOGO_PATH)
        self.splah_image.setPixmap(pixmap.scaledToHeight(460))
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

    def showMessage(self, text):
        self.statusLabel.setText(text)
        QtWidgets.QApplication.processEvents()


def show_splash_screen():
    """
    Shows the CustomXepr splash screen.

    :param app: Qt application instance.
    :returns: :class:`qtpy.QtWidgets.QSplashScreen`.
    """
    splash = SplashScreen()
    splash.show()
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
    :rtype: (:class:`XeprAPI.Xepr`, :class:`mercuryitc.MercuryITC`,
        :class:`keithley2600.Keithley2600`)
    """

    import sys
    from keithley2600 import Keithley2600
    from keithleygui import CONF as KCONF
    from mercuryitc import MercuryITC
    from mercurygui import CONF as MCONF

    KEITHLEY_ADDRESS = KCONF.get('Connection', 'VISA_ADDRESS')
    KEITHLEY_VISA_LIB = KCONF.get('Connection', 'VISA_LIBRARY')
    MERCURY_ADDRESS = MCONF.get('Connection', 'VISA_ADDRESS')
    MERCURY_VISA_LIB = MCONF.get('Connection', 'VISA_LIBRARY')

    try:
        sys.path.insert(0, os.popen('Xepr --apipath').read())
        import XeprAPI
    except ImportError:
        XeprAPI = None
        logging.info('XeprAPI could not be located.')

    try:
        xepr = XeprAPI.Xepr()
    except AttributeError:
        xepr = None
    except IOError:
        logging.info('No running Xepr instance could be found.')
        xepr = None

    mercury = MercuryITC(MERCURY_ADDRESS, MERCURY_VISA_LIB, open_timeout=1)
    keithley = Keithley2600(KEITHLEY_ADDRESS, KEITHLEY_VISA_LIB, open_timeout=1)

    return xepr, mercury, keithley


# ========================================================================================
# Start CustomXepr and user interfaces
# ========================================================================================

def start_gui(xepr, mercury, keithley):
    """
    Starts GUIs for Keithley, Mercury and CustomXepr.

    :returns: Tuple containing GUI instances.
    :rtype: (:class:`main.CustomXepr`, :class:`main_ui.JobStatusApp`,
        :class:`mercurygui.MercuryFeed`, :class:`mercurygui.MercuryMonitorApp`,
        :class:`keithleygui.KeithleyGuiApp`)
    """
    from keithleygui import KeithleyGuiApp
    from mercurygui import MercuryFeed, MercuryMonitorApp
    from customxepr.main import CustomXepr
    from customxepr.main_ui import JobStatusApp

    mercuryfeed = MercuryFeed(mercury)
    mercury_gui = MercuryMonitorApp(mercuryfeed)
    keithley_gui = KeithleyGuiApp(keithley)

    customXepr = CustomXepr(xepr, mercuryfeed, keithley)
    customXepr_gui = JobStatusApp(customXepr)

    customXepr_gui.show()
    mercury_gui.show()
    keithley_gui.show()

    return customXepr, customXepr_gui, mercuryfeed, mercury_gui, keithley_gui


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
    :rtype: (:class:`main.CustomXepr`, :class:`XeprAPI.Xepr`,
        :class:`keithley2600.Keithley2600`, :class:`mercuryitc.MercuryITC`,
        :class:`main_ui.JobStatusApp`, :class:`mercurygui.MercuryMonitorApp`,
        :class:`keithleygui.KeithleyGuiApp`)
    """

    from customxepr.main import __version__, __author__, __year__
    from customxepr.utils.misc import patch_excepthook

    # create a new Qt app or return an existing one
    app, interactive = get_qt_app()

    # create and show splash screen
    splash = show_splash_screen()

    # connect to instruments
    splash.showMessage("Connecting to instruments...")
    xepr, mercury, keithley = connect_to_instruments()
    # start user interfaces
    splash.showMessage("Loading user interface...")
    customXepr, customXepr_gui, mercuryfeed, mercury_gui, keithley_gui = start_gui(xepr, mercury, keithley)

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

        return (customXepr, xepr, mercury, mercuryfeed, keithley,
                customXepr_gui, mercury_gui, keithley_gui)

    else:
        splash.showMessage("Loading console...")

        from customxepr.utils.internal_ipkernel import InternalIPKernel

        # start event loop and console if run as a standalone app
        internal_kernel = InternalIPKernel(banner=banner)
        internal_kernel.new_qt_console()

        var_dict = {'customXepr': customXepr, 'xepr': xepr, 'mercury': mercury,
                    'mercuryfeed': mercuryfeed, 'keithley': keithley,
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
        return internal_kernel.ipkernel.start()


if __name__ == '__main__':
    import customxepr
    customXepr, xepr, mercury, mercuryfeed, keithley, customXepr_gui, \
        mercury_gui, keithley_gui = customxepr.run()
