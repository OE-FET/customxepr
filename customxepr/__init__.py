from __future__ import division, absolute_import, unicode_literals
import os
from customxepr.startup import run
from customxepr.main import CustomXepr
from customxepr.xepr_dataset import XeprData, XeprParam
from customxepr.manager import queued_exec

# =======================================================================================
# work around some pyqtgraph at Qt bugs
# =======================================================================================

from qtpy import QtCore


def handler(msg_type, msg_log_context, msg_string):
    pass

QtCore.qInstallMessageHandler(handler)

def cleanup():
    global _cleanupCalled
    if _cleanupCalled:
        return

    if not getConfigOption('exitCleanup'):
        return

    ViewBox.quit()  ## tell ViewBox that it doesn't need to deregister views anymore.
    _cleanupCalled = True

try:
    # import pyqtgraph before creating QApplication to avoid bugs
    import pyqtgraph
    # monkeypatch pyqtgraph cleanup to avoid crash in exit from garbage collection
    pyqtgraph.cleanup = cleanup

except ImportError:
    pass