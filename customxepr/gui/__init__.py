# -*- coding: utf-8 -*-
from .manager_window import ManagerApp
from .customxepr_window import CustomXeprGuiApp
from .splash import SplashScreen

# =======================================================================================
# check if Qt is available with the correct version
# =======================================================================================

import qtpy

if not qtpy.API == 'pyqt5':
    raise ImportError('Could not import PyQt5. PyQt5 is required for the CustomXepr GUI.')

if qtpy.LooseVersion(qtpy.PYQT_VERSION) < qtpy.LooseVersion('5.9'):
    raise ImportError('PyQt 5.9 or higher is required. ' +
                      'You have PyQt %s installed.' % qtpy.PYQT_VERSION)

# =======================================================================================
# suppress some Qt error messages
# =======================================================================================

from qtpy import QtCore


def handler(msg_type, msg_log_context, msg_string):
    pass

QtCore.qInstallMessageHandler(handler)

try:
    # import pyqtgraph before creating QApplication to avoid bugs
    import pyqtgraph
except Exception:
    pass
