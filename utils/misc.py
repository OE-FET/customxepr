#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 13:11:20 2018

@author: Sam Schott
"""
import os
import sys
from pkgutil import iter_modules
from qtpy import QtCore, QtWidgets
from traceback import format_exception

import subprocess


def check_dependencies(filePath):
    exit_code = 0
    modules = set(x[1] for x in iter_modules())
    with open(filePath, 'rb') as f:
        for line in f:
            requirement = line.rstrip()
            if requirement not in modules:
                print('Error: Could not find module ' + requirement + '. ' +
                      'Please install to run CustomXepr.')
                exit_code += 1

    return exit_code


def new_except_hook(etype, evalue, tb):
    """
    Custom exception hook which displays exceptions from threads in
    a QMessageBox.
    """
    QtWidgets.QMessageBox.information(None,
                                      str('error'),
                                      ''.join(format_exception(etype, evalue,
                                                               tb)))


def _patch_excepthook():
    """Replaces old exception hook with new."""
    sys.excepthook = new_except_hook


def patch_excepthook():
    """Replaces old exception hook with new in Qt event loop."""
    global TIMER

    TIMER = QtCore.QTimer()
    TIMER.setSingleShot(True)
    TIMER.timeout.connect(_patch_excepthook)
    TIMER.start()


def ping(ipAddress, ms_timeout=20):
    """
    Ping command for UNIX based systems. Millisecond timeout will only work
    if fping is installed. Returns True if IP address is reachable within
    timeout.
    """
    # check if fping is installed, otherwise use ping
    if os.system('which fping 2>&1 >/dev/null') == 0:
        command = 'fping'
        options = '-c 1 -t %i' % round(ms_timeout)
    else:
        sec_timeout = max(1, ms_timeout/1000)
        command = 'ping'
        options = '-c 1 -t %i ' % int(sec_timeout)

    return subprocess.call([command, options, ipAddress]) == 0
