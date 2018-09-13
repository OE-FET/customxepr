# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, absolute_import
from qtpy import QtWidgets, uic
import os
from config.main import CONF


class AddressDialog(QtWidgets.QDialog):
    """
    Provides a user dialog to select the modules for the feed.
    """
    def __init__(self, feed):
        super(self.__class__, self).__init__()
        # load user interface layout from .ui file
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'address_dialog.ui'), self)

        self.feed = feed
        self.lineEditAddress.setText(self.feed.address)
        self.buttonBox.accepted.connect(self._onAccept)

    def _onAccept(self):
        mercuryConnected = (self.feed.mercury is not None)
        # update connection settings in mercury feed
        self.feed.address = self.lineEditAddress.text()

        # update connection settings in config file
        CONF.set('MercuryFeed', 'MERCURY_ADDRESS', self.lineEditAddress.text())

        # restart feed for changes to become effective
        if mercuryConnected:
            self.feed.pause()
            self.feed.resume()
