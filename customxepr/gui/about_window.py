# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
import os
from PyQt5 import QtWidgets, uic

from customxepr.main import CustomXepr, __version__, __year__, __author__, __url__

_root = os.path.dirname(os.path.realpath(__file__))


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

        # get default platform font size, increase by 20% for title
        font = QtWidgets.QLabel('test').font()
        font_size = font.pointSize()
        fs_title = int(font_size * 1.2)
        font.setPointSize(fs_title)

        # set title string of window to CustomXepr version
        self.title_string = (CustomXepr.__name__ + ' ' + __version__)
        self.titleText.setText(self.title_string)
        self.titleText.setFont(font)

        # set copyright text
        placeholder = self.labelCopyRight.text()
        self.labelCopyRight.setText(placeholder.format(__year__, __author__))
        self.labelWebsite.setText(self.labelWebsite.text().format(__url__))
