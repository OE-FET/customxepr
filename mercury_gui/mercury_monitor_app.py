# -*- coding: utf-8 -*-

"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""

# system imports
import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor

# custom imports
from mercury_gui.readings_overview import ReadingsOverview
from mercury_gui.mercury_feed import MercuryFeed
from mercury_gui.mercury_window import Ui_MainWindow
from mercury_gui.mercury_address_dialog import AddressDialog

if QtCore.PYQT_VERSION_STR[0] == '5':
    from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg
                                                    as FigureCanvas)
elif QtCore.PYQT_VERSION_STR[0] == '4':
    from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg
                                                    as FigureCanvas)

logger = logging.getLogger(__name__)


class MercuryMonitorApp(QtWidgets.QMainWindow, Ui_MainWindow):

    # signals carrying converted data to GUI
    heater_volt_Signal = QtCore.Signal(str)
    heater_auto_Signal = QtCore.Signal(bool)
    heater_percent_Signal = QtCore.Signal(str)
    flow_auto_Signal = QtCore.Signal(bool)
    flow_Signal = QtCore.Signal(str)
    flow_min_Signal = QtCore.Signal(str)
    flow_setpoint_Signal = QtCore.Signal(str)
    t_Signal = QtCore.Signal(str)
    t_setpoint_Signal = QtCore.Signal(str)
    t_ramp_Signal = QtCore.Signal(str)
    t_ramp_enable_Signal = QtCore.Signal(bool)

    def __init__(self, feed):
        super(self.__class__, self).__init__()

        self.feed = feed

        # create popup Widgets
        self.addressDialog = AddressDialog(feed)
        self.readingsWindow = None

        # Set up layout and widgets that are defined in MercuryMonitorGUI.py
        self.setupUi(self)
        self._setup_figure()
        self._set_up_menubar()
        self._display_message('Looking for Mercury at %s...'
                              % self.feed.address)
        self.setIntialPosition()

        # accept only numbers as input for fields
        self._set_input_validators()

        # connect slots if mercury is not None
        if self.feed.mercury is not None:
            self._connect_slots()
            # set LED indicator to green
            self.led.setChecked(True)

        # get new readings when available, send as out signals
        self.feed.newReadingsSignal.connect(self.fetch_readings)
        # update plot when new data arrives
        self.feed.newReadingsSignal.connect(self._update_plot)
        # check for overheating when new data arrives
        self.feed.newReadingsSignal.connect(self._check_overheat)

        # start (stop) updates of GUI when mercury is connected (disconnected)
        # adjust clickable buttons upon connect / disconnect
        self.feed.connectedSignal.connect(self._update_GUI_connection)

        # set up logging to file
        self._setup_log_files()

# =================== BASIC UI SETUP ==========================================

    def setIntialPosition(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry(self)

        xPos = screen.left() + screen.width()*2/3
        yPos = screen.top()
        width = 600
        height = screen.height()*2/3

        self.setGeometry(xPos, yPos, width, height)

    def exit_(self):
        self.feed.exit_
        self.deleteLater()

    def _set_up_menubar(self):
        """
        Connects menu bar items to functions, sets the initialactivated status.
        """
        # connect to callbacks
        self.showLogAction.triggered.connect(self._on_log_clicked)
        self.exitAction.triggered.connect(self.exit_)
        self.readingsAction.triggered.connect(self._on_readings_clicked)
        self.connectAction.triggered.connect(self.feed.resume)
        self.disconnectAction.triggered.connect(self.feed.pause)
        self.updateAddressAction.triggered.connect(self.addressDialog.show)

        # initially disable menu bar items, will be enabled later individually
        self.connectAction.setEnabled(False)
        self.disconnectAction.setEnabled(False)
        self.modulesAction.setEnabled(False)
        self.readingsAction.setEnabled(False)

    def _setup_figure(self):
        """Sets up figure for temperature plot."""

        # get figure frame to match window color
        color = QtGui.QPalette().window().color().getRgb()
        color = [x/255.0 for x in color]

        # create figure and set axis labels
        self.fig = Figure(facecolor=color)
        self.fig.set_tight_layout('tight')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Time [min]', fontsize=9)
        self.ax.set_ylabel('Temperature [K]', fontsize=9)
        self.ax.tick_params(axis='both', which='major', labelsize=9)

        self.xLim, self.yLim = [-1, 1.0/60], [0, 300]
        self.ax.axis(self.xLim + self.yLim)

        # create line object for temperature graph
        self.line1, = self.ax.plot(0, 295, '-')

        # create canvas, add to main window, and draw canvas
        self.canvas = FigureCanvas(self.fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

        # set up data vectors for plot
        self.xData = []
        self.xDataMinZero = []
        self.yData = []

        # set update_plot to be executed every time the slider position changes
        self.horizontalSlider.valueChanged.connect(self._update_slider)

    def _update_GUI_connection(self, connected):
        if connected:
            self._display_message('Connection established.')
            logger.info('Connection to MercuryiTC established.')
            self._connect_slots()
            self.connectAction.setEnabled(False)
            self.disconnectAction.setEnabled(True)
            self.modulesAction.setEnabled(True)
            self.readingsAction.setEnabled(True)

            self.led.setChecked(True)

            self.show()

        elif not connected:
            self._display_error('Connection lost.')
            logger.info('Connection to MercuryiTC lost.')
            self._disconnect_slots()

            self.connectAction.setEnabled(True)
            self.disconnectAction.setEnabled(False)
            self.modulesAction.setEnabled(False)
            self.readingsAction.setEnabled(False)

            self.led.setChecked(False)

    def _set_input_validators(self):
        """ Sets validators for input fields"""
        self.t2_edit.setValidator(QtGui.QDoubleValidator())
        self.r1_edit.setValidator(QtGui.QDoubleValidator())
        self.gf1_edit.setValidator(QtGui.QDoubleValidator())
        self.h1_edit.setValidator(QtGui.QDoubleValidator())

    def _connect_slots(self):

        self._display_message('Connection established.')

        self.connectAction.setEnabled(False)
        self.disconnectAction.setEnabled(True)
        self.modulesAction.setEnabled(True)
        self.readingsAction.setEnabled(True)

        # connect GUI slots to emitted data from worker
        self.heater_volt_Signal.connect(self.h1_label.setText)
        self.heater_auto_Signal.connect(self.h2_checkbox.setChecked)
        self.heater_auto_Signal.connect(lambda b: self.h1_edit.setEnabled(not b))
        self.heater_auto_Signal.connect(self.h1_edit.setReadOnly)
        self.heater_percent_Signal.connect(self.h1_edit.updateText)

        self.flow_auto_Signal.connect(self.gf2_checkbox.setChecked)
        self.flow_auto_Signal.connect(lambda b: self.gf1_edit.setEnabled(not b))
        self.flow_auto_Signal.connect(self.gf1_edit.setReadOnly)
        self.flow_Signal.connect(self.gf1_edit.updateText)
        self.flow_min_Signal.connect(self.gf1_label.setText)

        self.t_Signal.connect(self.t1_reading.setText)
        self.t_setpoint_Signal.connect(self.t2_edit.updateText)
        self.t_ramp_Signal.connect(self.r1_edit.updateText)
        self.t_ramp_enable_Signal.connect(self.r2_checkbox.setChecked)

        # connect user input to change mercury settings
        self.t2_edit.returnPressed.connect(self.change_t_setpoint)
        self.r1_edit.returnPressed.connect(self.change_ramp)
        self.r2_checkbox.clicked.connect(self.change_ramp_auto)
        self.gf1_edit.returnPressed.connect(self.change_flow)
        self.gf2_checkbox.clicked.connect(self.change_flow_auto)
        self.h1_edit.returnPressed.connect(self.change_heater)
        self.h2_checkbox.clicked.connect(self.change_heater_auto)

        # conect menu bar item to show module dialog if mercury is running
        self.modulesAction.triggered.connect(self.feed.dialog.show)

    def _disconnect_slots(self):
        self._display_error('Connection lost.')

        self.connectAction.setEnabled(True)
        self.disconnectAction.setEnabled(False)
        self.modulesAction.setEnabled(False)
        self.readingsAction.setEnabled(False)

        # disconnect GUI slots from worker
        self.heater_volt_Signal.disconnect(self.h1_label.setText)
        self.heater_auto_Signal.disconnect(self.h2_checkbox.setChecked)
        self.heater_auto_Signal.disconnect(lambda b: self.h1_edit.setEnabled(not b))
        self.heater_auto_Signal.disconnect(self.h1_edit.setReadOnly)
        self.heater_percent_Signal.disconnect(self.h1_edit.updateText)

        self.flow_auto_Signal.disconnect(self.gf2_checkbox.setChecked)
        self.flow_auto_Signal.disconnect(lambda b: self.gf1_edit.setEnabled(not b))
        self.flow_auto_Signal.disconnect(self.gf1_edit.setReadOnly)
        self.flow_Signal.disconnect(self.gf1_edit.updateText)
        self.flow_min_Signal.disconnect(self.gf1_label.setText)

        self.t_Signal.disconnect(self.t1_reading.setText)
        self.t_setpoint_Signal.disconnect(self.t2_edit.updateText)
        self.t_ramp_Signal.disconnect(self.r1_edit.updateText)
        self.t_ramp_enable_Signal.disconnect(self.r2_checkbox.setChecked)

        # disconnect user input from mercury
        self.t2_edit.returnPressed.disconnect(self.change_t_setpoint)
        self.r1_edit.returnPressed.disconnect(self.change_ramp)
        self.r2_checkbox.clicked.disconnect(self.change_ramp_auto)
        self.gf1_edit.returnPressed.disconnect(self.change_flow)
        self.gf2_checkbox.clicked.disconnect(self.change_flow_auto)
        self.h1_edit.returnPressed.disconnect(self.change_heater)
        self.h2_checkbox.clicked.disconnect(self.change_heater_auto)

    def _display_message(self, text):
        self.statusBar.showMessage('    %s' % text, 5000)

    def _display_error(self, text):
        self.statusBar.showMessage('    %s' % text)

#    def _clear_display(self):
#        self.labelMessages.setStyleSheet('QLabel { color : green; }')
#        self.labelMessages.setText('')

    def fetch_readings(self, readings):
        """
        Parses readings for the MercuryMonitorApp and emits resulting
        strings as signals.
        """
        # emit heater signals
        self.heater_volt_Signal.emit('Heater, %s V:' % readings['HeaterVolt'])
        if readings['HeaterAuto'] == 'ON':
            self.heater_auto_Signal.emit(True)
        elif readings['HeaterAuto'] == 'OFF':
            self.heater_auto_Signal.emit(False)
        self.heater_percent_Signal.emit(str(round(readings['HeaterPercent'], 1)))

        # emit gas flow signals
        if readings['FlowAuto'] == 'ON':
            self.flow_auto_Signal.emit(True)
        elif readings['FlowAuto'] == 'OFF':
            self.flow_auto_Signal.emit(False)
        self.flow_Signal.emit(str(round(readings['FlowPercent'], 1)))
        self.flow_min_Signal.emit('Gas flow (min = %s%%):' % readings['FlowMin'])

        # emit temperature signals
        self.t_Signal.emit(str(round(readings['Temp'], 3)))
        self.t_setpoint_Signal.emit(str(readings['TempSetpoint']))
        self.t_ramp_Signal.emit(str(readings['TempRamp']))
        if readings['TempRampEnable'] == 'ON':
            self.t_ramp_enable_Signal.emit(True)
        elif readings['TempRampEnable'] == 'OFF':
            self.t_ramp_enable_Signal.emit(False)

    def _update_plot(self, readings):
        # append data for plotting
        self.xData.append(time.time())
        self.yData.append(readings['Temp'])

        # prevent data vector from exceeding 86400 entries
        self.xData = self.xData[-86400:]
        self.yData = self.yData[-86400:]

        # convert yData to minutes and set current time to t = 0
        xDataZero = list(map(operator.sub, self.xData,
                             [max(self.xData)] * len(self.xData)))
        self.xDataMinZero = list(map(operator.div, xDataZero,
                                     [60.0] * len(xDataZero)))

        self._update_slider()

    def _update_slider(self):
        # get number of entries that are within the slider value
        numberDP = sum(abs(x) < self.horizontalSlider.value()
                       for x in self.xDataMinZero) + 5

        # select data to be plotted
        self.CurrentXData = self.xDataMinZero[-numberDP:]
        self.CurrentYData = self.yData[-numberDP:]

        # update axis limits
        if not self.CurrentXData == []:
            xLimNew = [max(-self.horizontalSlider.value(), self.CurrentXData[0]), 1.0/60]
            yLimNew = [floor(min(self.CurrentYData)), ceil(max(self.CurrentYData)) + 0.1]

        # In the rare instance that floor(min(x)) == ceil(max(x)), we avoid
        # throwing an error by taking floor(min(x)) == ceil(max(x) + 0.1)

        # redraw the whole plot if axis limits have changed
        if xLimNew + yLimNew == self.xLim + self.yLim:
            self.line1.remove()
            self.line1, = self.ax.plot(self.CurrentXData, self.CurrentYData, '-')
            self.ax.draw_artist(self.line1)
            self.canvas.flush_events()
            self.fig.canvas.update()
        else:
            self.line1.set_data(self.CurrentXData, self.CurrentYData)
            self.ax.axis(xLimNew + yLimNew)
            self.canvas.draw()

        # update label
        self.label.setText('Time interval to display : %s min'
                           % self.horizontalSlider.value())

# =================== LOGGING AND SAVIBG OF DATA ==============================

    def _setup_log_files(self):
        """
        Set up logging of temperature history to files.
        Save temperature history to log file at '~/.CustomXepr/LOG_FILES/'
        after every 10 min.
        """
        # find user home directory
        homePath = os.path.expanduser('~')
        self.loggingPath = os.path.join(homePath, '.CustomXepr', 'LOG_FILES')

        # create folder '~/.CustomXepr/LOG_FILES' if not present
        if not os.path.exists(self.loggingPath):
            os.makedirs(self.loggingPath)
        # set logging file path
        self.logFile = os.path.join(self.loggingPath, '/temperature_log ' +
                                    time.strftime("%Y-%m-%d_%H-%M-%S"))

        t_save = 10  # time interval to save temperature data in min
        self.newFile = True  # create new log file for every new start
        self.save_timer = QtCore.QTimer()
        self.save_timer.setInterval(t_save*60*1000)
        self.save_timer.setSingleShot(False)  # set to reoccur
        self.save_timer.timeout.connect(self.log_temperature_data)
        self.save_timer.start()

    def save_temperature_data(self, filePath=None):
        # promt user for file path if not given
        if filePath is None:
            text = 'Select path for temperature data file:'
            filePath = QtWidgets.QFileDialog.getSaveFileName(caption=text)
            filePath = filePath[0]

        if filePath[-4:] is not '.txt':
            filePath.join('.txt')

        title = '# temperature trace, saved on '+time.strftime('%d/%m/%Y')+'\n'
        header = '\t'.join(['Time (sec)', 'Temperature (K)'])

        xData = np.array(self.xData)
        yData = np.array(self.yData)
        data_matrix = np.concatenate((xData[:, np.newaxis],
                                      yData[:, np.newaxis]), axis=1)

        np.savetxt(filePath, data_matrix, fmt='%.9E', delimiter='\t',
                   newline='\n', header=header, comments=title)

    def log_temperature_data(self):
        # save temperature data to log file
        self.save_temperature_data(self.logFile)


# =================== CALLBACKS FOR SETTING CHANGES ===========================

    def change_t_setpoint(self):
        newT = float(self.t2_edit.text())

        if newT < 310 and newT > 3.5:
            self._display_message('T_setpoint = %s K' % newT)
            self.feed.control.t_setpoint = newT
        else:
            self._display_error('Error: Only temperature setpoints between ' +
                                '3.5 K and 300 K allowed.')

    def change_ramp(self):
        self.feed.control.ramp = float(self.r1_edit.text())
        self._display_message('Ramp = ' + self.r1_edit.text() + ' K/min')

    def change_ramp_auto(self, checked):
        if checked:
            self.feed.control.ramp_enable = 'ON'
            self._display_message('Ramp is turned ON')
        elif not checked:
            self.feed.control.ramp_enable = 'OFF'
            self._display_message('Ramp is turned OFF')

    def change_flow(self):
        self.feed.control.flow = float(self.gf1_edit.text())
        self._display_message('Gas flow  = ' + self.gf1_edit.text() + '%')

    def change_flow_auto(self, checked):
        if checked:
            self.feed.control.flow_auto = 'ON'
            self._display_message('Gas flow is automatically controlled.')
            self.gf1_edit.setReadOnly(True)
            self.gf1_edit.setEnabled(False)
        elif not checked:
            self.feed.control.flow_auto = 'OFF'
            self._display_message('Gas flow is manually controlled.')
            self.gf1_edit.setReadOnly(False)
            self.gf1_edit.setEnabled(True)

    def change_heater(self):
        self.feed.control.heater = float(self.h1_edit.text())
        self._display_message('Heater power  = ' + self.h1_edit.text() + '%')

    def change_heater_auto(self, checked):
        if checked:
            self.feed.control.heater_auto = 'ON'
            self._display_message('Heater is automatically controlled.')
            self.h1_edit.setReadOnly(True)
            self.h1_edit.setEnabled(False)
        elif not checked:
            self.feed.control.heater_auto = 'OFF'
            self._display_message('Heater is manually controlled.')
            self.h1_edit.setReadOnly(False)
            self.h1_edit.setEnabled(True)

    def _check_overheat(self, readings):
        if readings['Temp'] > 310:
            self._display_error('Over temperature!')
            self.feed.control.heater_auto = 'OFF'
            self.feed.control.heater = 0

# ========================== CALLBACKS FOR MENU BAR ===========================

    def _on_readings_clicked(self):
        # create readings overview window if not present
        if self.readingsWindow is None:
            self.readingsWindow = ReadingsOverview(self.feed.mercury)
        # show it
        self.readingsWindow.show()

    def _on_log_clicked(self):
        """
        Opens directory with log files with current log file selected.
        """

        if platform.system() == 'Windows':
            os.startfile(self.loggingPath)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', self.loggingPath])
        else:
            subprocess.Popen(['xdg-open', self.loggingPath])


if __name__ == '__main__':
    # check if event loop is already running (e.g. in IPython),
    # otherwise create a new one
    created = False
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        created = True

    # Connect to MercuryiTC and start data feed
    if 'feed' not in locals():
        feed = MercuryFeed('172.20.91.41')

    # create GUI
    monitor = MercuryMonitorApp(feed)
    monitor.show()
    if created:
        sys.exit(app.exec_())
