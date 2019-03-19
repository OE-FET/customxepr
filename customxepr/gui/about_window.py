# -*- coding: utf-8 -*-
import os
from qtpy import QtWidgets, uic

from customxepr.main import CustomXepr, __version__, __year__, __author__, __url__


# noinspection PyArgumentList
class AboutWindow(QtWidgets.QWidget):
    """
    Shows version number, copyright info and url for CustomXepr in a new window.
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        # load user interface file
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'about_window.ui'), self)

        # set title string of window to CustomXepr version
        self.title_string = (CustomXepr.__name__ + ' ' + __version__)
        self.titleText.setText(self.title_string)

        # set copyright text
        placeholder = self.labelCopyRight.text()
        self.labelCopyRight.setText(placeholder.format(__year__, __author__))
        self.labelWebsite.setText(self.labelWebsite.text().format(__url__))
