#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:01:18 2018

@author: SamSchott
"""

# system imports
from __future__ import division, print_function, absolute_import
import os
from visa import InvalidSession
from qtpy import QtGui, QtCore, QtWidgets, uic
from matplotlib.figure import Figure
from Keithley2600 import TransistorSweepData

# local imports
from utils.led_indicator_widget import LedIndicator
from config.main import CONF

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg
                                                as FigureCanvas)


class KeithleyGuiApp(QtWidgets.QMainWindow):
    """ Provides a GUI for transfer and output sweeps on the Keithley 2600."""
    def __init__(self, keithley):
        super(self.__class__, self).__init__()
        # load user interface layout from .ui file
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'main.ui'), self)
        self.keithley = keithley

        # create figure area
        self._set_up_fig()

        # create LED indicator
        self.led = LedIndicator(self)
        self.led.setDisabled(True)  # Make the led non clickable
        self.statusBar.addPermanentWidget(self.led)
        self.led.setChecked(False)

        # change color of status bar
        self.statusBar.setStyleSheet('QStatusBar{background:transparent;}')

        # set validators for lineEdit fields
        self.lineEditVgStart.setValidator(QtGui.QDoubleValidator())
        self.lineEditVgStop.setValidator(QtGui.QDoubleValidator())
        self.lineEditVgStep.setValidator(QtGui.QDoubleValidator())
        self.lineEditVdStart.setValidator(QtGui.QDoubleValidator())
        self.lineEditVdStop.setValidator(QtGui.QDoubleValidator())
        self.lineEditVdStep.setValidator(QtGui.QDoubleValidator())
        self.lineEditInt.setValidator(QtGui.QDoubleValidator())
        self.lineEditSettling.setValidator(QtGui.QDoubleValidator())

        ## load default settings into GUI
        self._on_load_default()

        # connect to call-backs
        self.pushButtonTransfer.clicked.connect(self._on_transfer_clicked)
        self.pushButtonOutput.clicked.connect(self._on_output_clicked)
        self.pushButtonAbort.clicked.connect(self._on_abort_clicked)

        self.comboBoxGateSMU.currentIndexChanged.connect(self._on_smu_gate_changed)
        self.comboBoxDrainSMU.currentIndexChanged.connect(self._on_smu_drain_changed)

        self.actionSettings.triggered.connect(self._on_settings_clicked)
        self.actionConnect.triggered.connect(self._on_connect_clicked)
        self.actionDisconnect.triggered.connect(self._on_disconnect_clicked)
        self.action_Exit.triggered.connect(self._on_exit_clicked)
        self.actionSaveSweepData.triggered.connect(self._on_save_clicked)
        self.actionLoad_data_from_file.triggered.connect(self._on_load_clicked)
        self.actionSaveDefaults.triggered.connect(self._on_save_default)
        self.actionLoadDefaults.triggered.connect(self._on_load_default)

        self.actionSaveSweepData.setEnabled(False)

        # update when keithley is connected
        self._update_Gui_connection()

        # create address dialog
        self.addressDialog = KeithleyAddressDialog(self.keithley)

        # connection update timer: check periodically if keithley is connected
        # and busy, act accordingly
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_connection_status)
        self.timer.start(10000)  # Call every 10 seconds

    def update_connection_status(self):
        # disconncet if keithley does not respond, test by querying model
        if self.keithley.connected and not self.keithley.busy:
            try:
                self.keithley.localnode.model
            except (InvalidSession, OSError):
                self.keithley.disconnect()
                self._update_Gui_connection()

    def setIntialPosition(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry(self)

        xPos = screen.left() + screen.width()/4
        yPos = screen.top() + screen.height()/3

        self.setGeometry(xPos, yPos, 900, 500)

    def _convert_to_Vd(self, string):
        try:
            return float(string)
        except ValueError:
            if string.find('trailing') > 0:
                return 'trailing'
            else:
                raise ValueError('Invalid drain voltage.')

    def _check_if_busy(self):
        if self.keithley.busy:
            msg = ('Keithley is currently used by antoher program. ' +
                   'Please try again later.')
            QtWidgets.QMessageBox.information(None, str('error'), msg)
# =============================================================================
# Measurement callbacks
# =============================================================================

    def _on_transfer_clicked(self):
        """ Start a transfer measurement with current settings."""
        self._check_if_busy()

        params = {'Measurement': 'transfer'}
        # get current settings
        # get current settings
        smugate = self.comboBoxGateSMU.currentText()
        params['smu_gate'] = getattr(self.keithley, smugate)
        smudrain = self.comboBoxDrainSMU.currentText()
        params['smu_drain'] = getattr(self.keithley, smudrain)

        params['VgStart'] = float(self.lineEditVgStart.text())
        params['VgStop'] = float(self.lineEditVgStop.text())
        params['VgStep'] = float(self.lineEditVgStep.text())
        VdListString = self.lineEditVdList.text()
        VdStringList = VdListString.split(',')
        params['VdList'] = [self._convert_to_Vd(x) for x in VdStringList]

        params['tInt'] = float(self.lineEditInt.text())
        params['delay'] = float(self.lineEditSettling.text())

        # get combo box status
        if self.comboBoxSweepType.currentIndex() == 0:
            params['pulsed'] = False
        elif self.comboBoxSweepType.currentIndex() == 1:
            params['pulsed'] = True

        # run measurement
        self.statusBar.showMessage('    Recording transfer curve.')

        self.measureThread = MeasureThread(self.keithley, params)
        self.measureThread.finishedSig.connect(self._on_measure_done)

        # reflect idle and busy states in GUI
        self._gui_state_busy()

        self.measureThread.start()

    def _on_output_clicked(self):
        """ Start an output measurement with current settings."""
        self._check_if_busy()

        params = {'Measurement': 'output'}
        # get current settings
        smugate = self.comboBoxGateSMU.currentText()
        params['smu_gate'] = getattr(self.keithley, smugate)
        smudrain = self.comboBoxDrainSMU.currentText()
        params['smu_drain'] = getattr(self.keithley, smudrain)

        params['VdStart'] = float(self.lineEditVdStart.text())
        params['VdStop'] = float(self.lineEditVdStop.text())
        params['VdStep'] = float(self.lineEditVdStep.text())
        VgListString = self.lineEditVgList.text()
        VgStringList = VgListString.split(',')
        params['VgList'] = [float(x) for x in VgStringList]

        params['tInt'] = float(self.lineEditInt.text())
        params['delay'] = float(self.lineEditSettling.text())

        # get combo box status
        if self.comboBoxSweepType.currentIndex() == 0:
            params['pulsed'] = False
        elif self.comboBoxSweepType.currentIndex() == 1:
            params['pulsed'] = True

        # run measurement
        self.statusBar.showMessage('    Recording output curve.')
        self.measureThread = MeasureThread(self.keithley, params)
        self.measureThread.finishedSig.connect(self._on_measure_done)

        self._gui_state_busy()
        self.measureThread.start()

    def _on_measure_done(self, sweepData):
        self.statusBar.showMessage('    Ready.')
        self._gui_state_idle()
        self.actionSaveSweepData.setEnabled(True)

        self.sweepData = sweepData
        self.plot_new_data()
        if not self.keithley.abort_event.is_set():
            self._on_save_clicked()

    def _on_abort_clicked(self):
        """
        Aborts current measurement.
        """
        self.keithley.abort_event.set()

# =============================================================================
# Interface callbacks
# =============================================================================

    def _on_smu_gate_changed(self, intSMU):
        """ Triggered when the user selects a different gate SMU. """

        if intSMU == 0 and len(self.keithley.SMU_LIST) < 3:
            self.comboBoxDrainSMU.setCurrentIndex(1)
        elif intSMU == 1 and len(self.keithley.SMU_LIST) < 3:
            self.comboBoxDrainSMU.setCurrentIndex(0)

    def _on_smu_drain_changed(self, intSMU):
        """ Triggered when the user selects a different drain SMU. """

        if intSMU == 0 and len(self.keithley.SMU_LIST) < 3:
            self.comboBoxGateSMU.setCurrentIndex(1)
        elif intSMU == 1 and len(self.keithley.SMU_LIST) < 3:
            self.comboBoxGateSMU.setCurrentIndex(0)

    def _on_connect_clicked(self):
        self.keithley.connect()
        self._update_Gui_connection()
        if not self.keithley.connected:
            msg = ('Keithley cannot be reached at %s. ' % self.keithley.visa_address
                   + 'Please check if address is correct and Keithley is ' +
                   'turned on.')
            QtWidgets.QMessageBox.information(None, str('error'), msg)

    def _on_disconnect_clicked(self):
        self.keithley.disconnect()
        self._update_Gui_connection()
        self.statusBar.showMessage('    No Keithley connected.')

    def _on_settings_clicked(self):
        self.addressDialog.show()

    def _on_save_clicked(self):
        """Show GUI to save current sweep data as text file."""
        prompt = 'Save as file'
        filename = 'untitled.txt'
        formats = 'Text file (*.txt)'
        filepath = QtWidgets.QFileDialog.getSaveFileName(self, prompt,
                                                         filename, formats)
        if len(filepath[0]) < 4:
            return
        self.sweepData.save(filepath[0])

    def _on_load_clicked(self):
        """Show GUI to load sweep data from file."""
        prompt = 'Load file'
        filepath = QtWidgets.QFileDialog.getOpenFileName(self, prompt)
        if len(filepath[0]) < 4:
            return
        self.sweepData = TransistorSweepData()
        self.sweepData.load(filepath[0])
        self.plot_new_data()
        self.actionSaveSweepData.setEnabled(True)

    def _on_exit_clicked(self):
        self.keithley.disconnect()
        self.timer.stop()
        self.deleteLater()

    def _update_Gui_connection(self):
        """Check if Keithley is connected and update GUI."""
        if self.keithley.connected and not self.keithley.busy:
            self._gui_state_idle()
            self.led.setChecked(True)

        elif self.keithley.connected and self.keithley.busy:
            self._gui_state_busy()
            self.led.setChecked(True)

        elif not self.keithley.connected:
            self._gui_state_disconnected()
            self.led.setChecked(False)

    def _gui_state_busy(self):
        """Set GUI to state for running measurement."""

        self.pushButtonTransfer.setEnabled(False)
        self.pushButtonOutput.setEnabled(False)
        self.pushButtonAbort.setEnabled(True)

        self.actionConnect.setEnabled(False)
        self.actionDisconnect.setEnabled(False)

        self.statusBar.showMessage('    Measuring.')

    def _gui_state_idle(self):
        """Set GUI to state for IDLE Keithley."""

        self.pushButtonTransfer.setEnabled(True)
        self.pushButtonOutput.setEnabled(True)
        self.pushButtonAbort.setEnabled(True)

        self.actionConnect.setEnabled(False)
        self.actionDisconnect.setEnabled(True)
        self.statusBar.showMessage('    Ready.')

    def _gui_state_disconnected(self):
        """Set GUI to state for disconnected Keithley."""

        self.pushButtonTransfer.setEnabled(False)
        self.pushButtonOutput.setEnabled(False)
        self.pushButtonAbort.setEnabled(False)

        self.actionConnect.setEnabled(True)
        self.actionDisconnect.setEnabled(False)
        self.statusBar.showMessage('    No Keithley connected.')

    def _on_save_default(self):
        """Saves current settings from GUI as defaults."""

        # save transfer settings
        CONF.set('Keithley', 'VgStart', float(self.lineEditVgStart.text()))
        CONF.set('Keithley', 'VgStop', float(self.lineEditVgStop.text()))
        CONF.set('Keithley', 'VgStep', float(self.lineEditVgStep.text()))

        VdListString = self.lineEditVdList.text()
        VdStringList = VdListString.split(',')
        CONF.set('Keithley', 'VdList', [self._convert_to_Vd(x) for x in VdStringList])

        # save output settings
        CONF.set('Keithley', 'VdStart', float(self.lineEditVdStart.text()))
        CONF.set('Keithley', 'VdStop', float(self.lineEditVdStop.text()))
        CONF.set('Keithley', 'VdStep', float(self.lineEditVdStep.text()))

        VgListString = self.lineEditVgList.text()
        VgStringList = VgListString.split(',')
        CONF.set('Keithley', 'VgList', [float(x) for x in VgStringList])

        # save general settings
        CONF.set('Keithley', 'tInt', float(self.lineEditInt.text()))
        CONF.set('Keithley', 'delay', float(self.lineEditSettling.text()))

        # get combo box status
        if self.comboBoxSweepType.currentIndex() == 0:
            CONF.set('Keithley', 'pulsed', False)
        elif self.comboBoxSweepType.currentIndex() == 1:
            CONF.set('Keithley', 'pulsed', True)

        CONF.set('Keithley', 'gate', self.comboBoxGateSMU.currentText())
        CONF.set('Keithley', 'drain', self.comboBoxDrainSMU.currentText())

    def _on_load_default(self):
        """Load default settings to interface."""

        ## set text box contents
        # transfer curve settings
        self.lineEditVgStart.setText(str(CONF.get('Keithley', 'VgStart')))
        self.lineEditVgStop.setText(str(CONF.get('Keithley', 'VgStop')))
        self.lineEditVgStep.setText(str(CONF.get('Keithley', 'VgStep')))
        self.lineEditVdList.setText(str(CONF.get('Keithley', 'VdList')).strip('[]'))
        # output curve settings
        self.lineEditVdStart.setText(str(CONF.get('Keithley', 'VdStart')))
        self.lineEditVdStop.setText(str(CONF.get('Keithley', 'VdStop')))
        self.lineEditVdStep.setText(str(CONF.get('Keithley', 'VdStep')))
        self.lineEditVgList.setText(str(CONF.get('Keithley', 'VgList')).strip('[]'))

        # other
        self.lineEditInt.setText(str(CONF.get('Keithley', 'tInt')))
        self.lineEditSettling.setText(str(CONF.get('Keithley', 'delay')))

        # set PULSED comboBox status
        pulsed = CONF.get('Keithley', 'pulsed')
        if pulsed is False:
            self.comboBoxSweepType.setCurrentIndex(0)
        elif pulsed is True:
            self.comboBoxSweepType.setCurrentIndex(1)

        # Set SMU selection comboBox status
        cmbList = list(self.keithley.SMU_LIST)  # get list of all SMUs
        # We have to comboBoxes. If there are less SMU's, extend list.
        while len(cmbList) < 2:
            cmbList.append('--')

        self.comboBoxGateSMU.clear()
        self.comboBoxDrainSMU.clear()
        self.comboBoxGateSMU.addItems(cmbList)
        self.comboBoxDrainSMU.addItems(cmbList)

        try:
            self.comboBoxGateSMU.setCurrentIndex(cmbList.index(CONF.get('Keithley', 'gate')))
            self.comboBoxDrainSMU.setCurrentIndex(cmbList.index(CONF.get('Keithley', 'drain')))
        except ValueError:
            self.comboBoxGateSMU.setCurrentIndex(0)
            self.comboBoxDrainSMU.setCurrentIndex(1)
            msg = 'Could not find last used SMUs in Keithley driver.'
            QtWidgets.QMessageBox.information(None, str('error'), msg)

# =============================================================================
# Plotting commands
# =============================================================================

    def _set_up_fig(self):

        # get figure frame to match window color
        color = QtGui.QPalette().window().color().getRgb()
        color = [x/255 for x in color]

        # set up figure itself
        self.fig = Figure(facecolor=color)
        self.fig.set_tight_layout('tight')
        self.ax = self.fig.add_subplot(111)

        self.ax.set_title('Sweep data', fontsize=10)
        self.ax.set_xlabel('Voltage [V]', fontsize=9)
        self.ax.set_ylabel('Current [A]', fontsize=9)
        self.ax.tick_params(axis='both', which='major', direction='out',
                            colors='black', color=[0.5, 0.5, 0.5, 1],
                            labelsize=9)

        self.canvas = FigureCanvas(self.fig)

        self.canvas.setMinimumWidth(530)
        self.canvas.draw()

        self.gridLayout2.addWidget(self.canvas)

    def plot_new_data(self):
        """
        Plots the transfer or output curves.
        """
        self.ax.clear()  # clear current plot

        if self.sweepData.sweepType == 'transfer':
            for v in self.sweepData.step_list():
                self.ax.semilogy(self.sweepData.vSweep[v], abs(self.sweepData.iDrain[v]),
                                 '-', label='Drain current, Vd = %s' % v)
                self.ax.semilogy(self.sweepData.vSweep[v], abs(self.sweepData.iGate[v]),
                                 '--', label='Gate current, Vd = %s' % v)
                self.ax.legend(loc=3)

            self.ax.autoscale(axis='x', tight=True)
            self.ax.set_title('Transfer data')
            self.ax.set_xlabel('Gate voltage [V]')
            self.ax.set_ylabel('Current [A]')

            self.canvas.draw()

        if self.sweepData.sweepType == 'output':
            for v in self.sweepData.step_list():
                self.ax.plot(self.sweepData.vSweep[v], abs(self.sweepData.iDrain[v]),
                             '-', label='Drain current, Vg = %s' % v)
                self.ax.plot(self.sweepData.vSweep[v], abs(self.sweepData.iGate[v]),
                             '--', label='Gate current, Vg = %s' % v)
                self.ax.legend()

            self.ax.autoscale(axis='x', tight=True)
            self.ax.set_title('Output data')
            self.ax.set_xlabel('Drain voltage [V]')
            self.ax.set_ylabel('Current [A]')
            self.canvas.draw()


class KeithleyAddressDialog(QtWidgets.QDialog):
    """
    Provides a user dialog to select the modules for the feed.
    """
    def __init__(self, keithley):
        super(self.__class__, self).__init__()
        # load user interface layout from .ui file
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'address_dialog.ui'), self)

        self.keithley = keithley
        self.lineEditAddress.setText(self.keithley.visa_address)

        self.buttonBox.accepted.connect(self._onAccept)

    def _onAccept(self):
        # update connection settings in mercury feed
        self.keithley.visa_address = self.lineEditAddress.text()
        CONF.set('Keithley', 'KEITHLEY_ADDRESS', self.keithley.visa_address)
        # reconnect to new IP address
        self.keithley.disconnect()
        self.keithley.connect()


class MeasureThread(QtCore.QThread):

    startedSig = QtCore.Signal()
    finishedSig = QtCore.Signal(object)

    def __init__(self, keithley, params):
        QtCore.QThread.__init__(self)
        self.keithley = keithley
        self.params = params

    def __del__(self):
        self.wait()

    def run(self):
        self.startedSig.emit()

        if self.params['Measurement'] == 'transfer':
            sweepData = self.keithley.transferMeasurement(self.params['smu_gate'], self.params['smu_drain'], self.params['VgStart'],
                                                          self.params['VgStop'], self.params['VgStep'], self.params['VdList'],
                                                          self.params['tInt'], self.params['delay'], self.params['pulsed'])
            self.finishedSig.emit(sweepData)

        elif self.params['Measurement'] == 'output':
            sweepData = self.keithley.outputMeasurement(self.params['smu_gate'], self.params['smu_drain'], self.params['VdStart'],
                                                        self.params['VdStop'], self.params['VdStep'], self.params['VgList'],
                                                        self.params['tInt'], self.params['delay'], self.params['pulsed'])
            self.finishedSig.emit(sweepData)
