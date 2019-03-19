# -*- coding: utf-8 -*-
import os

from qtpy import QtWidgets, uic, QtGui, QtCore

SPLASH_UI_PATH = os.path.join(os.path.dirname(__file__), "splash.ui")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "resources/logo@2x.png")


class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        uic.loadUi(SPLASH_UI_PATH, self)
        pixmap = QtGui.QPixmap(LOGO_PATH)
        self.splah_image.setPixmap(pixmap.scaledToHeight(460))
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        # adjust font sizes according to os defaults
        font = QtWidgets.QLabel('test').font()
        font_size = font.pointSize()

        fs_title = int(font_size * 2.31)
        fs_info = int(font_size * 1.0)
        fs_status = int(font_size * 0.90)

        font.setPointSize(fs_title)
        self.titleLabel.setFont(font)
        font.setPointSize(fs_info)
        self.infoLabel.setFont(font)
        font.setPointSize(fs_status)
        self.statusLabel.setFont(font)

        # move to screen center
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg = self.frameGeometry()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    def showMessage(self, text):
        self.statusLabel.setText(text)
        self.show()
        self.raise_()
        QtWidgets.QApplication.processEvents()