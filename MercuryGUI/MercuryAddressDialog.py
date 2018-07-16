# -*- coding: utf-8 -*-
from qtpy import QtWidgets, uic
import os


class AddressDialog(QtWidgets.QDialog):
    """
    Provides a user dialog to select the modules for the feed.
    """
    def __init__(self, feed):
        super(self.__class__, self).__init__()
        # load user interface layout from .ui file
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'MercuryAddressDialog.ui'), self)

        self.feed = feed

        self.lineEditIP.setText(self.feed.address)
        self.lineEditPort.setText(self.feed.port)

        self.buttonBox.accepted.connect(self._onAccept)

    def _onAccept(self):
        mercuryConnected = (self.feed.mercury is not None)
        # update connection settings in mercury feed
        self.feed.address = str(self.lineEditIP.text())
        self.feed.port = str(self.lineEditPort.text())
        # restart feed for changes to become effective
        if mercuryConnected:
            self.feed.pause()
            self.feed.resume()
