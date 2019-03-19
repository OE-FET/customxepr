from __future__ import division, absolute_import, unicode_literals
import os
from customxepr.startup import run
from customxepr.main import CustomXepr
from customxepr.experiment.xepr_dataset import XeprData, XeprParam
from customxepr.manager import queued_exec

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
