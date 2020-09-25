# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
import sys
import os
import logging
import time
import traceback

try:
    from IPython import get_ipython
    from PyQt5 import QtWidgets
    IP = get_ipython()
    if IP:
        IP.enable_gui('qt')
        IP.run_line_magic('load_ext', 'autoreload')
        IP.run_line_magic('autoreload', '0')
        # create app here to trigger start of IPython Qt event loop
        app = QtWidgets.QApplication(['CustomXepr'])
        import matplotlib
        matplotlib.use('Qt5Agg')
except ImportError:
    IP = None


BRUKER_XEPR_API_PATH = os.popen('Xepr --apipath').read()
ENVIRON_XEPR_API_PATH = os.environ.get('XEPR_API_PATH', '')


# ========================================================================================
# Get or start Qt application instance
# ========================================================================================

def get_qt_app():
    """
    Creates a new Qt application or returns an existing one (for instance if run
    from an IPython console with Qt backend).

    :returns: QApplication instance.
    :rtype: `PyQt5.QtWidgets.QApplication`
    """

    from PyQt5 import QtCore, QtWidgets

    if IP:
        os.environ.update(SPY_UMR_ENABLED='False')
        # get app instance
        app = QtWidgets.QApplication.instance()
    else:
        app = QtWidgets.QApplication(['CustomXepr'])
        app.setApplicationName('CustomXepr')

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    return app


# ========================================================================================
# Create splash screen
# ========================================================================================

def show_splash_screen():
    """
    Shows the CustomXepr splash screen.

    :returns: :class:`PyQt5.QtWidgets.QSplashScreen`.
    """

    from PyQt5 import QtWidgets
    from customxepr.gui import SplashScreen

    splash = SplashScreen()
    splash.show()
    splash.raise_()
    QtWidgets.QApplication.processEvents()
    splash.showMessage('Initializing...')

    return splash


# ========================================================================================
# Connect to instruments: Bruker Xepr, Keithley and MercuryiTC.
# ========================================================================================

def connect_to_instruments():
    """
    Tries to connect to Keithley, Mercury and Xepr. Uses the visa
    addresses saved in the respective configuration files.

    :returns: Tuple containing instrument instances.
    :rtype: tuple
    """

    from keithley2600 import Keithley2600
    from keithleygui.config.main import CONF as KCONF
    from mercuryitc import MercuryITC
    from mercurygui.config.main import CONF as MCONF

    keithley_address = KCONF.get('Connection', 'VISA_ADDRESS')
    keithley_visa_lib = KCONF.get('Connection', 'VISA_LIBRARY')
    mercury_address = MCONF.get('Connection', 'VISA_ADDRESS')
    mercury_visa_lib = MCONF.get('Connection', 'VISA_LIBRARY')

    try:
        # Search for the XeprAPI in the following locations, use the first match:
        # 1) path from environment variable, if given
        # 2) installed python package
        # 3) pre-installed version with Xepr
        sys.path.insert(0, ENVIRON_XEPR_API_PATH)
        sys.path.insert(-1, BRUKER_XEPR_API_PATH)
        from XeprAPI import Xepr
        xepr = Xepr()
    except ImportError:
        logging.info('XeprAPI could not be located.')
        xepr = None
    except IOError:
        logging.info('No running Xepr instance could be found.')
        xepr = None

    mercury = MercuryITC(mercury_address, mercury_visa_lib, open_timeout=1, timeout=5000)
    keithley = Keithley2600(keithley_address, keithley_visa_lib, open_timeout=1, timeout=5000)

    return xepr, mercury, keithley


# ========================================================================================
# Start CustomXepr and user interfaces
# ========================================================================================

def start_gui(customXepr, mercury, keithley):
    """
    Starts GUIs for Keithley, Mercury and CustomXepr.

    :returns: Tuple containing GUI instances.
    :rtype: tuple
    """
    from keithleygui.main import KeithleyGuiApp
    from mercurygui.main import MercuryMonitorApp
    from customxepr.gui import CustomXeprGuiApp

    mercury_gui = MercuryMonitorApp(mercury)
    keithley_gui = KeithleyGuiApp(keithley)
    customXepr_gui = CustomXeprGuiApp(customXepr)

    mercury_gui.QUIT_ON_CLOSE = False
    keithley_gui.QUIT_ON_CLOSE = False
    customXepr_gui.QUIT_ON_CLOSE = False

    customXepr_gui.show()
    mercury_gui.show()
    keithley_gui.show()

    return customXepr_gui, mercury_gui, keithley_gui


def _exit_hook(instruments, guis=None):
    if guis:
        for ui in guis:
            try:
                ui.exit_()  # this will disconnect automatically
            except Exception:
                traceback.print_exc()

    for inst in instruments:
        try:
            inst.disconnect()  # disconnect instruments manually
        except Exception:
            traceback.print_exc()


def run(gui=True):
    """
    Runs CustomXepr -- this is the main entry point. Calling ``run`` will first
    create or retrieve an existing Qt application, then aim to connect to Xepr,
    a Keithley 2600 instrument and a MercuryiTC temperature controller and finally
    create user interfaces to control all three instruments.

    If run from an interactive Jupyter or IPython console with a Qt backend, ``run``
    will start an interactive session and return instances of the above instrument
    controllers. Otherwise, it will create its own Jupyter console to receive user input.

    :param bool gui: If ``False``, CustomXepr is started without a GUI and no Qt
        application will be started. In this case, CustomXepr does not require an
        installation of PyQt5. Defaults to ``True``.

    :returns: Tuple containing instrument instances (and UIs).
    :rtype: tuple
    """
    from customxepr import __version__, __author__
    from customxepr.main import CustomXepr
    from customxepr.gui.error_dialog import patch_excepthook

    year = str(time.localtime().tm_year)

    banner = (
        'Welcome to CustomXepr {0}. You can access connected instruments through '
        '"customXepr" or directly as "xepr", "keithley" and "mercury".\n\n'
        'Use "%run -i path/to/file.py" to run a python script such '
        'as a measurement routine. An introduction to CustomXepr is '
        'available at \x1b[1;34mhttps://customxepr.readthedocs.io\x1b[0m.\n\n'
        '(c) 2016-{1}, {2}.'.format(__version__, year, __author__)
    )

    ui = ()

    if not gui:
        print('Connecting to instruments...')
        xepr, mercury, keithley = connect_to_instruments()
        customXepr = CustomXepr(xepr, mercury, keithley)
        exit_customxepr = lambda: _exit_hook(instruments=(mercury, keithley))
        print(banner)

    else:
        app = get_qt_app()  # create a new Qt app or return an existing one
        splash = show_splash_screen()  # create splash screen for messages

        splash.showMessage('Connecting to instruments...')
        xepr, mercury, keithley = connect_to_instruments()
        customXepr = CustomXepr(xepr, mercury, keithley)

        splash.showMessage('Loading user interface...')
        ui = start_gui(customXepr, mercury, keithley)

        if IP:  # we have been started from a jupyter console

            def exit_customxepr():
                _exit_hook(instruments=(mercury, keithley), guis=ui)
                IP.ask_exit_saved()

            # print banner
            IP.run_line_magic('clear', '')
            IP.ask_exit_saved = IP.ask_exit
            IP.ask_exit = exit_customxepr
            print(banner)

            splash.close()

        else:
            # start ipython kernel and jupyter console
            splash.showMessage("Loading console...")

            from qtconsole.inprocess import QtInProcessKernelManager
            from customxepr.gui.jupyter_widget import CustomRichJupyterWidget

            def exit_customxepr():
                _exit_hook(instruments=(mercury, keithley), guis=ui)
                app.quit()

            kernel_manager = QtInProcessKernelManager()
            kernel_manager.start_kernel(show_banner=False)
            kernel = kernel_manager.kernel
            kernel.shell.banner1 = ''
            kernel_manager.kernel.shell.ask_exit = lambda: print('Please close this window to exit.')
            kernel.gui = 'qt'

            kernel_client = kernel_manager.client()
            kernel_client.start_channels()

            font_size = int(QtWidgets.QTextEdit().font().pointSize())

            ipython_widget = CustomRichJupyterWidget(
                banner=banner,
                font_size=font_size,
                gui_completion='droplist',
                on_close=exit_customxepr
            )
            ipython_widget.kernel_manager = kernel_manager
            ipython_widget.kernel_client = kernel_client
            ipython_widget.show()

            var_dict = {'customXepr': customXepr, 'xepr': xepr, 'mercury': mercury,
                        'keithley': keithley, 'ui': ui, 'kernel_manager': kernel_manager}

            kernel.shell.push(var_dict)

            patch_excepthook()  # display errors from Qt event loop to user
            splash.close()  # remove splash screen

            # start event loop
            sys.exit(app.exec_())

    return customXepr, xepr, mercury, keithley, ui


if __name__ == '__main__':
    customXepr, xepr, mercury, keithley, ui = run()
