# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
import os
import markdown2
from PyQt5 import QtWidgets, uic

from customxepr import __version__, __url__

_root = os.path.dirname(os.path.realpath(__file__))


# noinspection PyArgumentList
class UpdateWindow(QtWidgets.QDialog):
    """
    Show new version number, link to changes.
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        # load user interface file
        uic.loadUi(os.path.join(_root, 'update_dialog.ui'), self)

        # set text
        placeholder = self.label.text()
        self.label.setText(placeholder.format(
            __version__, __url__ + '/en/latest/changelog.html'))

        # generate and set changelog html
        path = os.path.join(_root, 'resources/CHANGELOG.md')
        with open(path, 'r') as f:
            changes_text = f.read()

        html = markdown2.markdown(changes_text)

        self.textBrowser.setHtml(html)
