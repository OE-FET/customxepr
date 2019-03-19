# -*- coding: utf-8 -*-
import os
from qtpy import QtWidgets, uic

from customxepr.main import __version__, __url__


# noinspection PyArgumentList
class UpdateWindow(QtWidgets.QDialog):
    """
    Show new version number, link to changes.
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        # load user interface file
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'update_dialog.ui'), self)

        # set copyright text
        placeholder = self.label.text()
        self.label.setText(placeholder.format(__version__, __url__ +
                                              '/en/latest/changelog.html'))
