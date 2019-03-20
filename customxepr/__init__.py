from __future__ import division, absolute_import, unicode_literals
from customxepr.startup import run
from customxepr.main import CustomXepr
from customxepr.manager import Experiment, Manager, queued_exec
from customxepr.experiment.xepr_dataset import XeprData, XeprParam
from customxepr.experiment.mode_picture_dataset import ModePicture

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
