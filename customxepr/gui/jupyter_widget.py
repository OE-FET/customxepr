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

    def __init__(self, *args, **kwargs):
        RichJupyterWidget.__init__(self, *args, **kwargs)
        self.update_darkmode()

    def changeEvent(self, QEvent):

        if QEvent.type() == QtCore.QEvent.PaletteChange:
            self.update_darkmode()

    def update_darkmode(self):

        if isDarkWindow():
            self.set_default_style('linux')
        else:
            self.set_default_style()

        self.setStyleSheet('')


if __name__ == '__main__':

    from qtpy import QtWidgets
    from qtconsole.inprocess import QtInProcessKernelManager

    app = QtWidgets.QApplication([])

    kernel_manager = QtInProcessKernelManager()
    kernel_manager.start_kernel(show_banner=False)
    kernel_manager.kernel.shell.banner1 = ''
    kernel = kernel_manager.kernel

    kernel_client = kernel_manager.client()
    kernel_client.start_channels()

    ipython_widget = CustomRichJupyterWidget(banner='Hi!')
    ipython_widget.kernel_manager = kernel_manager
    ipython_widget.kernel_client = kernel_client
    ipython_widget.show()

    app.exec_()
