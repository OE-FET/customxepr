#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:01:18 2018

@author: SamSchott
"""

# system imports
import os
from qtpy import QtGui, QtCore, QtWidgets, uic
from matplotlib.figure import Figure
if QtCore.PYQT_VERSION_STR[0] == '5':
    from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg
                                                    as FigureCanvas)

elif QtCore.PYQT_VERSION_STR[0] == '4':
    from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg
                                                    as FigureCanvas)

# custom imports
from HelpFunctions import LedIndicator
from SweepDataClass import SweepData


class KeithleyGuiApp(QtWidgets.QMainWindow):
    """ Provides a GUI for transfer and output sweeps on the Keithley 2600."""
    def __init__(self, keithley):
        super(self.__class__, self).__init__()
        # load user interface layout from .ui file
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'KeithleyGUI.ui'), self)
        self.keithley = keithley

        # create figure area
        self._set_up_fig()

        # create LED indicator
        self.led = LedIndicator(self)
        self.led.setDisabled(True)  # Make the led non clickable
        self.statusBar.addPermanentWidget(self.led)
        self.led.setChecked(False)

        # set validators for lineEdit fields
        self.lineEditVgStart.setValidator(QtGui.QDoubleValidator())
        self.lineEditVgStop.setValidator(QtGui.QDoubleValidator())
        self.lineEditVgStep.setValidator(QtGui.QDoubleValidator())
        self.lineEditVdStart.setValidator(QtGui.QDoubleValidator())
        self.lineEditVdStop.setValidator(QtGui.QDoubleValidator())
        self.lineEditVdStep.setValidator(QtGui.QDoubleValidator())
        self.lineEditInt.setValidator(QtGui.QDoubleValidator())
        self.lineEditSettling.setValidator(QtGui.QDoubleValidator())

        ## set text box contents
        # transfer curve settings
        self.lineEditVgStart.setText(str(self.keithley.DEFAULTS['VgStart']))
        self.lineEditVgStop.setText(str(self.keithley.DEFAULTS['VgStop']))
        self.lineEditVgStep.setText(str(self.keithley.DEFAULTS['VgStep']))
        self.lineEditVdList.setText(str(self.keithley.DEFAULTS['VdList']).strip('[]'))
        # output curve settings
        self.lineEditVdStart.setText(str(self.keithley.DEFAULTS['VdStart']))
        self.lineEditVdStop.setText(str(self.keithley.DEFAULTS['VdStop']))
        self.lineEditVdStep.setText(str(self.keithley.DEFAULTS['VdStep']))
        self.lineEditVgList.setText(str(self.keithley.DEFAULTS['VgList']).strip('[]'))

        # other
        self.lineEditInt.setText(str(self.keithley.DEFAULTS['tInt']))
        self.lineEditSettling.setText(str(self.keithley.DEFAULTS['delay']))

        ## set combo box status
        if self.keithley.DEFAULTS['pulsed'] is False:
            self.comboBoxSweepType.setCurrentIndex(0)
        elif self.keithley.DEFAULTS['pulsed'] is True:
            self.comboBoxSweepType.setCurrentIndex(1)

        if self.keithley.gate == 'smua':
            self.comboBoxSweepType.setCurrentIndex(0)
        elif self.keithley.gate == 'smub':
            self.comboBoxSweepType.setCurrentIndex(1)

        # connect to call-backs
        self.pushButtonTransfer.clicked.connect(self._on_transfer_clicked)
        self.pushButtonOutput.clicked.connect(self._on_output_clicked)
        self.pushButtonAbort.clicked.connect(self._on_abort_clicked)

        self.actionSettings.triggered.connect(self._on_settings_clicked)
        self.actionConnect.triggered.connect(self._on_connect_clicked)
        self.actionDisconnect.triggered.connect(self._on_disconnect_clicked)
        self.action_Exit.triggered.connect(self._on_exit_clicked)
        self.actionSave_last_sweep.triggered.connect(self._on_save_clicked)
        self.actionLoad_data_from_file.triggered.connect(self._on_load_clicked)

        self.actionSave_last_sweep.setEnabled(False)

        self.comboBoxSMU.currentIndexChanged.connect(self._on_smu_changed)

        # update when keithley is connected
        self._update_Gui_connection()
        self.keithley.connectedSignal.connect(self._update_Gui_connection)

        # create address dialog
        self.addressDialog = KeithleyAddressDialog(self.keithley)

        # reflect idle  and busy states in GUI
        self.keithley.busySig.connect(self._gui_state_busy)
        self.keithley.idleSig.connect(self._gui_state_idle)

    def setIntialPosition(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry(self)

        xPos = screen.left() + screen.width()/4
        yPos = screen.top() + screen.height()/3

        self.setGeometry(xPos, yPos, 900, 500)

# =============================================================================
# Measurement callbacks
# =============================================================================

    def _on_transfer_clicked(self):
        """ Start a transfer measurement with current settings."""
        params = {'Measurement': 'transfer'}
        # get current settings
        params['VgStart'] = float(self.lineEditVgStart.text())
        params['VgStop'] = float(self.lineEditVgStop.text())
        params['VgStep'] = float(self.lineEditVgStep.text())
        VdListString = self.lineEditVdList.text()
        VdStringList = VdListString.split(',')
        params['VdList'] = [float(x) for x in VdStringList]

        params['tInt'] = float(self.lineEditInt.text())
        params['delay'] = float(self.lineEditSettling.text())

        # get combo box status
        if self.comboBoxSweepType.currentIndex() == 0:
            params['pulsed'] = False
        elif self.comboBoxSweepType.currentIndex() == 1:
            params['pulsed'] = True

        if self.comboBoxTrailing.currentIndex() == 1:
            params['VdList'][-1] = 'trailing'

        # run measurement
        self.statusBar.showMessage('    Recording transfer curve.')

        self.measureThread = MeasureThread(self.keithley, params)
        self.measureThread.finishedSig.connect(self._on_measure_done)

        self.measureThread.start()

    def _on_output_clicked(self):
        """ Start an output measurement with current settings."""
        params = {'Measurement': 'output'}
        # get current settings
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

        self.measureThread.start()

    def _on_measure_done(self, sweepData):
        self.statusBar.showMessage('    Ready.')
        self.actionSave_last_sweep.setEnabled(True)

        self.sweepData = sweepData
        self.plot_new_data()
        if not self.keithley.abort_event.is_set():
            self.sweepData.save()

    def _on_abort_clicked(self):
        """
        Aborts current measurement.
        """
        self.keithley.abort_event.set()

# =============================================================================
# Interface callbacks
# =============================================================================

    def _on_smu_changed(self, intSMU):
        """
        Triggered when the user selects a different SMU as gate. Will
        propagate changes to Keithley instance.
        """

        if intSMU == 0:
            self.keithley.gate = 'smua'
            self.keithley.drain = 'smub'
        elif intSMU == 1:
            self.keithley.gate = 'smub'
            self.keithley.drain = 'smua'

    def _on_connect_clicked(self):
        self.keithley.connect()
        self._update_Gui_connection()

    def _on_disconnect_clicked(self):
        self.keithley.disconnect()
        self._update_Gui_connection()
        self.statusBar.showMessage('    No Keithley connected.')

    def _on_settings_clicked(self):
        self.addressDialog.show()

    def _on_save_clicked(self):
        self.sweepData.save()

    def _on_load_clicked(self):
        self.sweepData = SweepData()
        self.sweepData.load()
        self.plot_new_data()

    def _on_exit_clicked(self):
        self.keithley.disconnect()
        self.deleteLater()

    def _update_Gui_connection(self):
        """Check if Keithley is connected and update GUI"""

        if self.keithley._keithley is None:
            self._gui_state_disconnected()
            self.led.setChecked(False)
        else:
            self._gui_state_idle()
            self.show()
            self.led.setChecked(True)

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

# =============================================================================
# Plotting commands
# =============================================================================

    def _set_up_fig(self):

        # get figure frame to match window color
        color = QtGui.QPalette().window().color().getRgb()
        color = [x/255.0 for x in color]

        # set up figure itself
        self.fig = Figure(facecolor=color)
        self.fig.set_tight_layout('tight')
        self.ax = self.fig.add_subplot(111)

        self.ax.set_title('Sweep data', fontsize=10)
        self.ax.set_xlabel('Voltage [V]', fontsize=9)
        self.ax.set_ylabel('Current [A]', fontsize=9)
        self.ax.tick_params(axis='both', which='major', labelsize=9)

        self.canvas = FigureCanvas(self.fig)

        self.canvas.setMinimumWidth(530)
        self.canvas.draw()

        # set up plotting controls for self.canvas
#        self.plotControlWidget = mplToolbar(self.canvas, self)
#        self.plotControlWidget.setMaximumWidth(380)

        # add to layout
#        self.gridLayout2.addWidget(self.plotControlWidget)
#        self.gridLayout2.setAlignment(self.plotControlWidget, QtCore.Qt.AlignHCenter)
        self.gridLayout2.addWidget(self.canvas)

    def plot_new_data(self):
        """
        Plots the transfer or output curves.
        """
        self.ax.clear()  # clear current plot

        if self.sweepData.sweepType == 'transfer':

            for i in range(0, self.sweepData.nStep):
                nPoints = len(self.sweepData.Vg)/self.sweepData.nStep
                select = slice(i*nPoints, (i+1)*nPoints)

                self.ax.semilogy(self.sweepData.Vg[select], abs(self.sweepData.Id[select]), '-',
                                 label='Drain current, Vd = %s' % self.sweepData.vStep[i])
                self.ax.semilogy(self.sweepData.Vg[select], abs(self.sweepData.Ig[select]), '--',
                                 label='Gate current, Vd = %s' % self.sweepData.vStep[i])
                self.ax.legend(loc=3)

            self.ax.autoscale(axis='x', tight=True)
            self.ax.set_title('Transfer data')
            self.ax.set_xlabel('Gate voltage [V]')
            self.ax.set_ylabel('Current [A]')

            self.canvas.draw()

        if self.sweepData.sweepType == 'output':

            for i in range(0, self.sweepData.nStep):
                nPoints = len(self.sweepData.Vg)/self.sweepData.nStep
                select = slice(i*nPoints, (i+1)*nPoints)

                self.ax.plot(self.sweepData.Vd[select], abs(self.sweepData.Id[select]), '-',
                             label='Drain current, Vg = %s' % self.sweepData.vStep[i])
                self.ax.plot(self.sweepData.Vd[select], abs(self.sweepData.Ig[select]), '--',
                             label='Gate current, Vg = %s' % self.sweepData.vStep[i])
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
                                'KeithleyAddressDialog.ui'), self)

        self.keithley = keithley
        self.lineEditIP.setText(self.keithley.address)

        self.buttonBox.accepted.connect(self._onAccept)

    def _onAccept(self):
        # update connection settings in mercury feed
        self.keithley.address = str(self.lineEditIP.text())
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
            sweepData = self.keithley.transferMeasurement(VgStart=self.params['VgStart'], VgStop=self.params['VgStop'],
                                                          VgStep=self.params['VgStep'], Vd=self.params['VdList'], filepath=None,
                                                          plot=False, tInt=self.params['tInt'], delay=self.params['delay'],
                                                          pulsed=self.params['pulsed'])
            self.finishedSig.emit(sweepData)

        elif self.params['Measurement'] == 'output':
            sweepData = self.keithley.outputMeasurement(VdStart=self.params['VdStart'], VdStop=self.params['VdStop'],
                                                        VdStep=self.params['VdStep'], Vg=self.params['VgList'], filepath=None,
                                                        plot=False, tInt=self.params['tInt'], delay=self.params['delay'],
                                                        pulsed=self.params['pulsed'])
            self.finishedSig.emit(sweepData)
