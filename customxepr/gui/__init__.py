# -*- coding: utf-8 -*-

from distutils.version import LooseVersion

from .manager_window import ManagerApp
from .customxepr_window import CustomXeprGuiApp
from .splash import SplashScreen

# =======================================================================================
# check if Qt is available with the correct version
# =======================================================================================

from PyQt5 import QtCore

if LooseVersion(QtCore.PYQT_VERSION_STR) < LooseVersion('5.9'):
    raise ImportError('PyQt5 5.9 or higher is required. ' +
                      'You have PyQt5 %s installed.' % QtCore.PYQT_VERSION_STR)


# =======================================================================================
# suppress some Qt error messages
# =======================================================================================

def handler(msg_type, msg_log_context, msg_string):
    pass


QtCore.qInstallMessageHandler(handler)

try:
    # import pyqtgraph before creating QApplication to avoid bugs
    import pyqtgraph
except ImportError:
    pass
