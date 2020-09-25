# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from PyQt5 import QtCore, QtWidgets
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from keithleygui.pyqt_labutils.dark_mode_support import isDarkWindow


class CustomRichJupyterWidget(RichJupyterWidget):
    def __init__(self, *args, on_close=None, **kwargs):
        RichJupyterWidget.__init__(self, *args, **kwargs)
        self.setWindowTitle("CustomXepr Console")
        self.update_darkmode()
        self._on_close = on_close

    def changeEvent(self, event):

        if event.type() == QtCore.QEvent.PaletteChange:
            self.update_darkmode()

    def closeEvent(self, event):

        res = QtWidgets.QMessageBox.question(
            self,
            "CustomXepr",
            "Are you sure you want to quit CustomXper?",
            QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.Yes,
        )
        if res == QtWidgets.QMessageBox.Yes:
            if self._on_close:
                self._on_close()
            event.accept()
        else:
            event.ignore()

    def update_darkmode(self):

        if isDarkWindow():
            self.set_default_style("linux")
        else:
            self.set_default_style()

        self.setStyleSheet("")
