# -*- coding: utf-8 -*-

"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""

from qtpy import QtCore, QtWidgets, uic
import sys
import os
import logging
import visa

from MercuryDriver import MercuryITC
from HelpFunctions import ping

logger = logging.getLogger(__name__)


class MercuryFeed(QtWidgets.QWidget):
    """
    Povides a data feed from the MercuryiTC with the most important readings
    of the gasflow, heater, temperature sensor and control loop modules. This
    enables other programs to get readings from the feed and reduced direct
    communication with the mercury.
    """

    # status signals
    newReadingsSignal = QtCore.Signal(object)
    notifySignal = QtCore.Signal(str)
    connectedSignal = QtCore.Signal(bool)

    def __init__(self, address, port='7020', refresh=1):
        super(self.__class__, self).__init__()

        self.refresh = refresh
        self.address = address
        self.port = port
        self.mercury = None
        self.thread = None

        self._connect()

    # BASE FUNCTIONALITY CODE

    def pause(self):
        # stop worker thread
        self.worker.running = False
        self.thread.terminate()

        # disconnect mercury
        self.connectedSignal.emit(False)
        self.mercury.disconnect()

    def resume(self):
        # resconnect mercury
        self.mercury.connect()
        self.connectedSignal.emit(True)

        # restart thread
        self.worker.running = True
        self.thread.start()

    def exit_(self):
        if self.thread is not None:
            self.worker.running = False
            self.thread.quit()
            self.thread.wait()
        if self.mercury is not None:
            self.mercury.disconnect()
        self.connectedSignal.emit(False)
        self.deleteLater()

# CODE TO INTERACT WITH MERCURYITC

    def _connect(self):
        """
        Tries to connect to MercuryiTC at the given IP address. If successful,
        a thread is started to periodically update readings.
        """
        # try to ping mercury (quicker than opening a visa connection)
        if ping(self.address) is False:
            self.mercury = None
            # start a timer to try again in 30 sec
            QtCore.QTimer.singleShot(30000, self._connect)
            return

        try:
            self.mercury = MercuryITC(self.address, self.port)
        except visa.VisaIOError:
            # start a timer to try again in 30 sec
            QtCore.QTimer.singleShot(30000, self._connect)
            return

        self.dialog = SensorDialog(self.mercury.modules)
        self.dialog.accepted.connect(self.updateModules)

        # start data collection thread
        self.thread = QtCore.QThread()
        self.worker = DataCollectionWorker(self.refresh, self.mercury.modules,
                                           self.dialog.modNumbers)
        self.worker.moveToThread(self.thread)
        self.worker.readingsSignal.connect(self._getData)
        self.worker.connectedSignal.connect(self.connectedSignal.emit)
        self.thread.started.connect(self.worker.run)
        self.updateModules(self.dialog.modNumbers)
        self.thread.start()

        self.connectedSignal.emit(True)

    def updateModules(self, modNumbers):
        """
        Updates module list after the new modules have been selected in dialog.
        """
        self.gasflow = self.mercury.modules[modNumbers['gasflow']]
        self.heater = self.mercury.modules[modNumbers['heater']]
        self.temperature = self.mercury.modules[modNumbers['temperature']]
        self.control = self.mercury.modules[modNumbers['temperature']+1]

        # send new modules to thread if running
        self.worker.updateModules(modNumbers)

    def _getData(self, readingsFromThread):
        self.readings = readingsFromThread
        self.newReadingsSignal.emit(self.readings)


class SensorDialog(QtWidgets.QDialog):
    """
    Provides a user dialog to select the modules for the feed.
    """

    accepted = QtCore.Signal(object)

    def __init__(self, mercuryModules):
        super(self.__class__, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'ChoseSensorDialog.ui'), self)

        num = len(mercuryModules)
        temp_modules_nick = []
        self.temp_modules = []
        gas_modules_nick = []
        self.gas_modules = []
        heat_modules_nick = []
        self.heat_modules = []

        self.modNumbers = {}

        for i in range(num-1, -1, -1):
            address = mercuryModules[i].address
            type_ = address.split(':')[-1]
            nick = mercuryModules[i].nick
            if type_ == 'AUX':
                gas_modules_nick.append(nick)
                self.gas_modules.append(i)
            elif type_ == 'HTR':
                heat_modules_nick.append(nick)
                self.heat_modules.append(i)
            elif type_ == 'TEMP':
                if nick not in temp_modules_nick:
                    temp_modules_nick.append(nick)
                    self.temp_modules.append(i)

        self.comboBox.addItems(temp_modules_nick)
        self.comboBox_2.addItems(gas_modules_nick)
        self.comboBox_3.addItems(heat_modules_nick)

        self.modNumbers['temperature'] = self.temp_modules[self.comboBox.currentIndex()]
        self.modNumbers['gasflow'] = self.gas_modules[self.comboBox_2.currentIndex()]
        self.modNumbers['heater'] = self.heat_modules[self.comboBox_3.currentIndex()]

        self.buttonBox.accepted.connect(self._onAccept)

    def _onAccept(self):
        self.modNumbers['temperature'] = self.temp_modules[self.comboBox.currentIndex()]
        self.modNumbers['gasflow'] = self.gas_modules[self.comboBox_2.currentIndex()]
        self.modNumbers['heater'] = self.heat_modules[self.comboBox_3.currentIndex()]
        self.accepted.emit(self.modNumbers)


class DataCollectionWorker(QtCore.QObject):

    readingsSignal = QtCore.Signal(object)
    connectedSignal = QtCore.Signal(bool)

    def __init__(self, refresh, mercuryModules, modNumbers):
        QtCore.QObject.__init__(self)
        self.refresh = refresh
        self.mercuryModules = mercuryModules
        self.modNumbers = modNumbers
        self.running = True
        self.readings = {}
        self.updateModules(self.modNumbers)

    def run(self):
        while self.running:
            try:
                # proceed with full update
                self.getReadings()
                # sleep untill next scheduled refresh
                QtCore.QThread.msleep(int(self.refresh*1000))
            except:
                # emit signal if connection is lost
                self.connectedSignal.emit(False)
                # stop worker thread
                self.running = False
                logging.warning('Connection to MercuryiTC lost.')

    def getReadings(self):
        # read heater data
        self.readings['HeaterVolt'] = self.heater.volt[0]
        self.readings['HeaterAuto'] = self.control.heater_auto
        self.readings['HeaterPercent'] = self.control.heater

        # read gas flow data
        self.readings['FlowAuto'] = self.control.flow_auto
        self.readings['FlowPercent'] = self.gasflow.perc[0]
        self.readings['FlowMin'] = self.gasflow.gmin
        self.readings['FlowSetpoint'] = self.control.flow

        # read temperature data
        self.readings['Temp'] = self.temperature.temp[0]
        self.readings['TempSetpoint'] = self.control.t_setpoint
        self.readings['TempRamp'] = self.control.ramp
        self.readings['TempRampEnable'] = self.control.ramp_enable

        self.readingsSignal.emit(self.readings)

    def updateModules(self, modNumbers):
        """
        Updates module list after the new modules have been selected in dialog.
        """
        self.gasflow = self.mercuryModules[modNumbers['gasflow']]
        self.heater = self.mercuryModules[modNumbers['heater']]
        self.temperature = self.mercuryModules[modNumbers['temperature']]
        self.control = self.mercuryModules[modNumbers['temperature']+1]


# if we're running the file directly and not importing it
if __name__ == '__main__':

    # check if event loop is already running (e.g. in IPython),
    # otherwise create a new one
    created = 0
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        created = 1

    feed = MercuryFeed('172.20.91.43')

    if created == 1:
        sys.exit(app.exec_())
