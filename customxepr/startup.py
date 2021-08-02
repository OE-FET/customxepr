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
import subprocess
import traceback

try:
    from IPython import get_ipython
    IP = get_ipython()
except ImportError:
    IP = None

try:
    res = subprocess.check_output(["Xepr", "--apipath"])
except (FileNotFoundError, subprocess.CalledProcessError):
    BRUKER_XEPR_API_PATH = ""
else:
    BRUKER_XEPR_API_PATH = res.decode()

ENVIRON_XEPR_API_PATH = os.environ.get("XEPR_API_PATH", "")
os.environ["SPY_UMR_ENABLED"] = "False"

logger = logging.getLogger(__name__)


# ======================================================================================
# Create splash screen
# ======================================================================================


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
    splash.showMessage("Initializing...")

    return splash


# ======================================================================================
# Connect to instruments: Bruker Xepr, Keithley and MercuryiTC.
# ======================================================================================


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

    keithley_address = KCONF.get("Connection", "VISA_ADDRESS")
    keithley_visa_lib = KCONF.get("Connection", "VISA_LIBRARY")
    mercury_address = MCONF.get("Connection", "VISA_ADDRESS")
    mercury_visa_lib = MCONF.get("Connection", "VISA_LIBRARY")

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
        logger.info("XeprAPI could not be located.")
        xepr = None
    except IOError:
        logger.info("No running Xepr instance could be found.")
        xepr = None

    mercury = MercuryITC(
        mercury_address, mercury_visa_lib, open_timeout=1, timeout=5000
    )
    keithley = Keithley2600(
        keithley_address, keithley_visa_lib, open_timeout=1, timeout=5000
    )

    return xepr, mercury, keithley


# ======================================================================================
# Start CustomXepr and user interfaces
# ======================================================================================


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


def run_cli():
    """
    This is the main interactive shell entry point. Calling ``run_cli`` will connect to
    all instruments and return instantiated control classes.

    :returns: Tuple containing instrument instances.
    :rtype: tuple
    """
    from customxepr.main import CustomXepr

    xepr, mercury, keithley = connect_to_instruments()
    customXepr = CustomXepr(xepr, mercury, keithley)

    return customXepr, xepr, mercury, keithley


def run_gui():
    """
    Runs the CustomXepr GUI -- this is the main entry point. Calling ``run_gui`` will
    first create a Qt application, then aim to connect to Xepr, a Keithley2600
    instrument and a MercuryiTC temperature controller and finally create user
    interfaces to control all three instruments.
    """
    from customxepr import __version__, __author__
    from customxepr.main import CustomXepr
    from customxepr.gui.error_dialog import patch_excepthook

    year = str(time.localtime().tm_year)

    banner = (
        "Welcome to CustomXepr {0}. You can access connected instruments through "
        '"customXepr" or directly as "xepr", "keithley" and "mercury".\n\n'
        'Use "%run -i path/to/file.py" to run a python script such '
        "as a measurement routine. An introduction to CustomXepr is "
        "available at \x1b[1;34mhttps://customxepr.readthedocs.io\x1b[0m.\n\n"
        "(c) 2016-{1}, {2}.".format(__version__, year, __author__)
    )

    ui = ()

    # start qt app
    from PyQt5 import QtCore, QtWidgets

    app = QtWidgets.QApplication(["CustomXepr"])
    app.setApplicationName("CustomXepr")

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    splash = show_splash_screen()  # create splash screen for messages

    splash.showMessage("Connecting to instruments...")
    xepr, mercury, keithley = connect_to_instruments()
    customXepr = CustomXepr(xepr, mercury, keithley)

    splash.showMessage("Loading user interface...")
    ui = start_gui(customXepr, mercury, keithley)

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
    kernel.shell.banner1 = ""
    kernel_manager.kernel.shell.ask_exit = lambda: print(
        "Please close this window to exit."
    )
    kernel.gui = "qt"

    kernel_client = kernel_manager.client()
    kernel_client.start_channels()

    font_size = int(QtWidgets.QTextEdit().font().pointSize())

    ipython_widget = CustomRichJupyterWidget(
        banner=banner,
        font_size=font_size,
        gui_completion="droplist",
        on_close=exit_customxepr,
    )
    ipython_widget.kernel_manager = kernel_manager
    ipython_widget.kernel_client = kernel_client
    ipython_widget.show()

    var_dict = {
        "customXepr": customXepr,
        "xepr": xepr,
        "mercury": mercury,
        "keithley": keithley,
        "ui": ui,
        "kernel_manager": kernel_manager,
    }

    kernel.shell.push(var_dict)

    patch_excepthook()  # display errors from Qt event loop to user
    splash.close()  # remove splash screen

    # clear all root loggers
    logging.getLogger().handlers.clear()

    # start event loop
    sys.exit(app.exec_())


def run_ip():
    """
    Runs the CustomXepr GUI from IPython.
    """

    global customXepr, xepr, mercury, keithley, ui, app

    from customxepr import __version__, __author__
    from customxepr.main import CustomXepr

    year = str(time.localtime().tm_year)

    banner = (
        "Welcome to CustomXepr {0}. You can access connected instruments through "
        '"customXepr" or directly as "xepr", "keithley" and "mercury".\n\n'
        'Use "%run -i path/to/file.py" to run a python script such '
        "as a measurement routine. An introduction to CustomXepr is "
        "available at \x1b[1;34mhttps://customxepr.readthedocs.io\x1b[0m.\n\n"
        "(c) 2016-{1}, {2}.".format(__version__, year, __author__)
    )

    # start qt app
    from PyQt5 import QtCore, QtWidgets

    IP.enable_gui("qt")
    IP.run_line_magic("load_ext", "autoreload")
    IP.run_line_magic("autoreload", "0")

    app = QtWidgets.QApplication(["CustomXepr"])
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    try:
        import matplotlib
        matplotlib.use("Qt5Agg")
    except ImportError:
        pass

    splash = show_splash_screen()  # create splash screen for messages

    splash.showMessage("Connecting to instruments...")
    xepr, mercury, keithley = connect_to_instruments()
    customXepr = CustomXepr(xepr, mercury, keithley)

    splash.showMessage("Loading user interface...")
    ui = start_gui(customXepr, mercury, keithley)

    splash.close()  # remove splash screen

    IP.run_line_magic("clear", "")

    print(banner)


if __name__ == "__main__":

    if IP:
        run_ip()
    else:
        run_gui()
