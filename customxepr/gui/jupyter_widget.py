# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from qtpy import QtCore
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from keithleygui.pyqt_labutils.dark_mode_support import isDarkWindow


class CustomRichJupyterWidget(RichJupyterWidget):

    def __init__(self, banner=''):
        RichJupyterWidget.__init__(self)
        self.banner = banner
        self.gui_completion = 'droplist'
        self.update_darkmode()

    def changeEvent(self, QEvent):

        if QEvent.type() == QtCore.QEvent.PaletteChange:
            self.update_darkmode()

    def update_darkmode(self):

        if isDarkWindow():
            self.set_default_style('linux')
        else:
            self.set_default_style()

        self.setStyleSheet("")
