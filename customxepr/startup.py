#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from IPython.display import clear_output
from qtpy import QtCore, QtWidgets, QtGui

from keithley2600 import Keithley2600
from keithleygui import KeithleyGuiApp
from keithleygui import CONF as KCONF

from mercuryitc import MercuryITC
from mercurygui import MercuryFeed, MercuryMonitorApp
from mercurygui import CONF as MCONF

# local imports
from customxepr.utils.misc import patch_excepthook
from customxepr.main import CustomXepr, __version__, __author__, __year__
from customxepr.main_ui import JobStatusApp

try:
    sys.path.insert(0, os.popen('Xepr --apipath', stderr=subprocess.PIPE).read())
    import XeprAPI
except ImportError:
    XeprAPI = None
    logging.info('XeprAPI could not be located.')

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


# ========================================================================================
# Get or start Qt application instance
# ========================================================================================

def get_qt_app():
    """
    Creates a new Qt application or returns an existing one (for instance if run
    from an IPython console with Qt backend).

    :returns: Tuple (``app``, ``created``) where ``created`` is `True` if a new application
        has been created and `False` if an existing one is returned.
    :rtype: (:class:`qtpy.QtWidgets.QApplication`, bool)
    """
    created = False
    app = QtCore.QCoreApplication.instance()

    if not app:
        app = QtWidgets.QApplication([''],)
        created = True

    return app, created


# ========================================================================================
# Create splash screen
# ========================================================================================

def show_splash_screen(app):
    """
    Shows the CustomXepr splash screen.

    :param app: Qt application instance.
    :returns: :class:`qtpy.QtWidgets.QSplashScreen`.
    """
    direct = os.path.dirname(os.path.realpath(__file__))
    image = QtGui.QPixmap(os.path.join(direct, 'resources', 'splash.png'))
    image.setDevicePixelRatio(3)
    splash = QtWidgets.QSplashScreen(image)
    splash.show()
    app.processEvents()

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

    try:
        xepr = XeprAPI.Xepr()
    except AttributeError:
        xepr = None
    except IOError:
        logging.info('No running Xepr instance could be found.')
        xepr = None

    mercury = MercuryITC(MERCURY_ADDRESS, MERCURY_VISA_LIB)
    keithley = Keithley2600(KEITHLEY_ADDRESS, KEITHLEY_VISA_LIB)

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

    # create a new Qt app or return an existing one
    app, created = get_qt_app()

    # create and show splash screen
    splash = show_splash_screen(app)

    # connect to instruments
    xepr, mercury, keithley = connect_to_instruments()
    # start user interfaces
    customXepr, customXepr_gui, mercuryfeed, mercury_gui, keithley_gui = start_gui(xepr, mercury, keithley)

    banner = ('Welcome to CustomXepr %s. ' % __version__ +
              'You can access connected instruments through "customXepr" ' +
              'or directly as "xepr", "keithley" and "mercury".\n\n' +
              'Use "%run -i path/to/file.py" to run a python script such ' +
              'as a measurement routine.\n'
              'Type "exit" to gracefully exit ' +
              'CustomXepr.\n\n(c) 2016 - %s, %s.' % (__year__, __author__))

    if created:

        from customxepr.utils.internal_ipkernel import InternalIPKernel

        # start event loop and console if run as a standalone app
        kernel_window = InternalIPKernel(banner=banner)
        kernel_window.new_qt_console()

        var_dict = {'customXepr': customXepr, 'xepr': xepr, 'mercury': mercury,
                    'mercuryfeed': mercuryfeed, 'keithley': keithley,
                    'customXepr_gui': customXepr_gui,
                    'mercury_gui': mercury_gui, 'keithley_gui': keithley_gui,
                    }

        kernel_window.send_to_namespace(var_dict)
        # noinspection PyUnresolvedReferences
        app.aboutToQuit.connect(kernel_window.cleanup_consoles)
        # remove splash screen
        splash.finish(customXepr_gui)
        # patch exception hook to display errors from Qt event loop
        patch_excepthook()
        # start event loop
        kernel_window.ipkernel.start()

    else:
        # print banner
        clear_output()
        print(banner)
        # remove splash screen
        splash.finish(customXepr_gui)
        # patch exception hook to display errors from Qt event loop
        patch_excepthook()

        return (customXepr, xepr, mercury, mercuryfeed, keithley,
                customXepr_gui, mercury_gui, keithley_gui)


if __name__ == '__main__':
    import customxepr
    customXepr, xepr, mercury, mercuryfeed, keithley, customXepr_gui, \
        mercury_gui, keithley_gui = customxepr.run()
