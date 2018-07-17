# -*- coding: utf-8 -*-

import sys
from qtpy import QtCore,QtGui
from traceback import format_exception

def new_except_hook(etype, evalue, tb):
    QtWidgets.QMessageBox.information(None, 
                                      str('error'),
                                      ''.join(format_exception(etype, evalue, tb)))

def _patch_excepthook():
    sys.excepthook = new_except_hook

def patch_excepthook():
    TIMER = QtCore.QTimer()
    TIMER.setSingleShot(True)
    TIMER.timeout.connect(_patch_excepthook)
    TIMER.start()
    