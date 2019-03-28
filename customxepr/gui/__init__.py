# -*- coding: utf-8 -*-
from .manager_window import ManagerApp
from .customxepr_window import CustomXeprGuiApp
from .splash import SplashScreen

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
