# -*- coding: utf-8 -*-

import os
import pydoc
from qtpy import QtCore, QtWidgets, uic
import CustomXepr


class AboutWindow(QtWidgets.QWidget, QtCore.QCoreApplication):
    """
    Prints version number, copyright info and help output from CustomXepr to a
    PyQt window.
    """
    def __init__(self):

        super(self.__class__, self).__init__()
        # load user interface file
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'AboutWindow.ui'), self)
        # get help output in plain text format
        self.help_output = pydoc.plain(pydoc.render_doc(CustomXepr.CustomXepr))
        # print help output to scroll area of window
        self.docText.setText(self.help_output)
        # set title string of window to CustomXepr version
        self.titleString = CustomXepr.__name__ + ' ' + CustomXepr.__version__
        self.titleText.setText(self.titleString)
