#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 13:11:20 2018

@author: Sam Schott
"""
from __future__ import division, absolute_import
import sys
from qtpy import QtCore, QtWidgets
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonTracebackLexer
from traceback import format_exception

from customxepr.main import __author__


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, title, message, error_info, parent=None):
        super(self.__class__, self).__init__(parent=parent)
        self.setWindowTitle(title)
        self.setFixedWidth(650)

        self.gridLayout = QtWidgets.QGridLayout()
        self.setLayout(self.gridLayout)

        self.title = QtWidgets.QLabel(self)
        self.title.setStyleSheet('font-weight: bold;')
        self.title.setText(title)

        self.message = QtWidgets.QLabel(self)
        self.message.setWordWrap(True)
        self.message.setText(message)

        self.details = QtWidgets.QTextEdit(self)
        self.details.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        html_formatter = HtmlFormatter(noclasses=True, nobackground=True)
        html_info = highlight(''.join(format_exception(*error_info)),
                              PythonTracebackLexer(), html_formatter)
        self.details.setHtml(html_info)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)

        self.gridLayout.addWidget(self.title)
        self.gridLayout.addWidget(self.message)
        self.gridLayout.addWidget(self.details)
        self.gridLayout.addWidget(self.buttonBox)


def new_except_hook(etype, evalue, tb):
    """
    Custom exception hook which displays exceptions from threads in a QMessageBox.
    """
    title = 'CustomXepr Internal Error'
    message = ('CustomXepr has encountered an internal error. ' +
               'Please report this bug to %s.' % __author__)
    error_info = (etype, evalue, tb)
    msg_box = ErrorDialog(title, message, error_info)
    msg_box.exec_()


def _patch_excepthook():
    """
    Replaces old exception hook with new.
    """
    sys.excepthook = new_except_hook


def patch_excepthook():
    """
    Replaces old exception hook with new in Qt event loop.
    """
    global TIMER

    TIMER = QtCore.QTimer()
    TIMER.setSingleShot(True)
    TIMER.timeout.connect(_patch_excepthook)
    TIMER.start()
