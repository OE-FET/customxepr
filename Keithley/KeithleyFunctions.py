# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 20:19:05 2016

@author: Sam Schott (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""

# system imports
import visa
import time
import numpy as np
import logging
from threading import Event
from qtpy import QtCore, QtWidgets

# custom imports
from SweepDataClass import SweepData
from Utils import ping
from Config.main import CONF


logger = logging.getLogger(__name__)

# create new logging level for status updates
logging.STATUS = 15
logging.addLevelName(logging.STATUS, 'STATUS')
setattr(logger, 'status', lambda message, *args: logger._log(logging.STATUS,
                                                             message, args))


class Keithley(QtWidgets.QWidget):
    """
    Keithley driver to perform base functions such as voltage sweeps.
    Needs the NI-Visa to be installed and the pyvisa package to communicate
    with a Keithley probe station.
    """

    abort_event = Event()
    connectedSignal = QtCore.Signal(bool)
    busySig = QtCore.Signal()
    idleSig = QtCore.Signal()

    DEFAULTS = dict(CONF.items('Keithley'))

# =============================================================================
# Set up basic communication with Keithley
# =============================================================================

    def __init__(self, address=CONF.get('Keithley', 'KEITHLEY_IP')):
        super(self.__class__, self).__init__()
        # open Keithley Visa resource
        self.address = address
        self.rm = visa.ResourceManager()
        self.connect()

        # specify drain and gate electrodes
        self.gate = self.DEFAULTS['gate']
        self.drain = self.DEFAULTS['drain']

    def write(self, text):
        """
        Writes text to Keithley.
        """
        self._keithley.write(text)

    def query(self, text):
        """
        Queries and expects response from Keithley.
        """
        return self._keithley.query('print(%s)' % text)

    def connect(self, read_term='\n', bdrate=57600):
        """
        Connects to Keithley and opens pyvisa API.
        """
        # try to ping Keithley (quicker than opening a visa connection)
        if ping(self.address) is False:
            self._keithley = None
            # if not available, try again in 30 sec
            QtCore.QTimer.singleShot(30000, self.connect)
            return

        try:
            visaAddress = 'TCPIP0::%s::INSTR' % self.address
            self._keithley = self.rm.open_resource(visaAddress)
            self._keithley.read_termination = read_term
            self._keithley.baud_rate = bdrate
            self.connectedSignal.emit(True)

            self.reset()
            self.clearCaches()
        except OSError:
            logger.warning('NI Visa is not installed.')
            self._keithley = None
            return
        except visa.VisaIOError:
            self._keithley = None
            self.connectedSignal.emit(False)
            # if not available, try again in 30 sec
            QtCore.QTimer.singleShot(30000, self.connect)
            return

    def disconnect(self):
        """
        Disconnects from Keithley.
        """
        try:
            self._keithley.close()
            self._keithley = None
        except AttributeError:
            pass

    def beep(self, sec=0.3, Hz=2400):
        """
        Plays a beep for the give time (sec) at a specified frequency (Hz).
        """
        self.write('beeper.beep(%s,%s)' % (sec, Hz))

    def reset(self):
        """
        Resets the Keithley SMUs.
        """
        # reset all SMUs
        self.write('reset()')

        # beep for confirmation
        self.beep()

    def clearCaches(self):
        """
        Clears instrument buffers and caches.
        """
        # clears SMU buffers
        self.write('smua.nvbuffer1.clear()')
        self.write('smua.nvbuffer2.clear()')
        self.write('smub.nvbuffer1.clear()')
        self.write('smub.nvbuffer2.clear()')

        self.write('smua.nvbuffer1.clearcache()')
        self.write('smua.nvbuffer2.clearcache()')
        self.write('smub.nvbuffer1.clearcache()')
        self.write('smub.nvbuffer2.clearcache()')

# =============================================================================
# Define low level control functions
# =============================================================================

    def turnOn(self, SMU):
        """
        Turns on the specified SMU.
        """
        self.write('%s.source.output = smua.OUTPUT_ON' % SMU)

    def turnOff(self, SMU):
        """
        Turns off the specified SMU.
        """
        self.write('%s.source.output = smua.OUTPUT_OFF' % SMU)

    def setVoltage(self, SMU, voltage):
        """
        Turns on the specified SMU and applies a voltage.
        """
        self.turnOn(SMU)
        self.write('%s.source.levelv = %s' % (SMU, voltage))

    def getVoltage(self, SMU):
        """
        Gets voltage applied to specified SMU.
        """
        return float(self.query('%s.source.levelv' % SMU))

    def measureVoltage(self, SMU):
        return float(self.query('%s.measure.v()' % SMU))

    def setDisplay(self, SMU, display):
        """
        Sets the display of SMU.
        INPUTS:
            SMU - suma or smub
            display - 'MEASURE_DCAMPS', 'MEASURE_DCVOLTS',
                      'MEASURE_OHMS', 'MEASURE_WATTS'
        """
        DISPLAY_TYPES = ['MEASURE_DCAMPS', 'MEASURE_DCVOLTS',
                         'MEASURE_OHMS', 'MEASURE_WATTS']

        if display not in DISPLAY_TYPES:
            raise ValueError('Only values in %s allowed for display.' % DISPLAY_TYPES)
        else:
            self.write('display.%s.measure.func = display.%s' % (SMU, display))

    def getPowerLineFreq(self):
        """ Returns frequency of power supply in Hz. """
        freq = float(self.query('localnode.linefreq'))
        return freq

    def setIntegrationTime(self, SMU, tInt):
        """ Sets the integration time of SMU for measurements in sec. """
        freq = self.getPowerLineFreq()
        NPLC = tInt*freq  # number frequency cycles used for integration
        self.write('%s.measure.nplc = %f' % (SMU, NPLC))

    def setMeasureDelay(self, SMU, delay):
        """ Sets the settling time before measurement for SMU. """
        self.write('%s.measure.delay = %f' % (SMU, delay))

    def rampToVoltage(self, targetVolt, SMU, delay=0.1, stepSize=1):
        """
        Ramps up the voltage of the specified SMU.
        INPUT:
            targetVolt - target gate voltage
            stepSize - size of voltage ramp steps in Volts
            delay -  delay between steps in sec
        """
        logger.status('Setting %s voltage to %s V.' % (SMU, targetVolt))
        self.turnOn(SMU)

        # get current voltage
        Vcurr = self.getVoltage(SMU)
        if Vcurr == targetVolt:
            logger.status('Vg = %sV.' % targetVolt)
            return

        self.setDisplay(SMU, 'MEASURE_DCVOLTS')

        for V in np.arange(Vcurr, targetVolt, stepSize):
            self.setVoltage(SMU, V)
            self.measureVoltage(SMU)
            time.sleep(delay)

        self.setVoltage(SMU, targetVolt)
        targetVolt = self.measureVoltage(SMU)
        logger.info('Gate voltage set to Vg = %s V.' % round(targetVolt))

        self.beep()

    def readBuffer(self, bufferName='smua.nvbuffer1'):
        """
        Reads buffer values and returns them as a list.
        Clears buffer afterwards.
        """
        n = int(float(self.query('%s.n' % bufferName)))
        list_out = [0.00] * n
        for i in range(0, n):
            list_out[i] = float(self.query('%s[%d]' % (bufferName, i+1)))

        # clears buffer
        self.write('%s.clear()' % bufferName)
        self.write('%s.clearcache()' % bufferName)
        return list_out

    def voltageSweep(self, sweep='smua', VStart=10, VStop=-60, VStep=-1,
                     VFix=-60, tInt=0.1, delay=-1, pulsed=False):
        """
        Sweeps voltage at one terminal while keeping the second at a
        constant voltage.
        """
        self.busySig.emit()
        # define list containing results. If we abort early, we have something
        # to return
        Vg, Ig, Vd, Id = [], [], [], []

        if self.abort_event.is_set():
            self.idleSig.emit()
            self.clearCaches()
            return Vg, Vd, Ig, Id

        # Setup smua/smub for sweep measurement. The voltage is swept from
        # VStart to VStop in intervals of VStep with a measuremnt at each step.
        numPoints = 1 + abs((VStop-VStart)/VStep)

        if VFix == 'trailing':
            self.write('smub.trigger.source.linearv(%f,%f,%d)' % (VStart,
                       VStop, numPoints))
            self.write('smub.trigger.source.action = smub.ENABLE')

            # Setup smua to follow smub
            self.write('smua.trigger.source.linearv(%f,%f,%d)' % (VStart,
                       VStop, numPoints))
            self.write('smua.trigger.source.action = smua.ENABLE')

        elif sweep == 'smua':
            self.write('smua.trigger.source.linearv(%f,%f,%d)' % (VStart,
                       VStop, numPoints))
            self.write('smua.trigger.source.action = smua.ENABLE')

            # Setup smub to trigger at each smua step with a constant voltage
            self.write('smub.trigger.source.linearv(%f,%f,%d)' % (VFix, VFix,
                       numPoints))
            self.write('smub.trigger.source.action = smub.ENABLE')

        elif sweep == 'smub':
            self.write('smub.trigger.source.linearv(%f,%f,%d)' % (VStart,
                       VStop, numPoints))
            self.write('smub.trigger.source.action = smub.ENABLE')

            # Setup sma trigger at each step but apply a constant voltage VFix
            self.write('smua.trigger.source.linearv(%f,%f,%d)' % (VFix, VFix,
                       numPoints))
            self.write('smua.trigger.source.action = smua.ENABLE')

        else:
            logger.error('Please specify the sweep terminal "smua" or "smub".')
            return

        # CONFIGURE INTEGRATION TIME FOR EACH MEASUREMENT
        self.setIntegrationTime('smua', tInt)
        self.setIntegrationTime('smub', tInt)

        # CONFIGURE SETTLING TIME FOR GATE VOLTAGE, I-LIMIT, ETC...
        self.setMeasureDelay('smua', delay)
        self.setMeasureDelay('smub', delay)

        self.write('smua.measure.autorangei = smua.AUTORANGE_ON')
        self.write('smub.measure.autorangei = smub.AUTORANGE_ON')

        self.write('smua.trigger.source.limiti = 0.1')
        self.write('smub.trigger.source.limiti = 0.1')

        self.write('smua.source.func = smua.OUTPUT_DCVOLTS')
        self.write('smub.source.func = smub.OUTPUT_DCVOLTS')

        # 2-wire measurement, use SENSE_REMOTE for 4-wire
        self.write('smua.sense = smua.SENSE_LOCAL')
        self.write('smub.sense = smub.SENSE_LOCAL')

        # clears SMU buffers
        self.write('smua.nvbuffer1.clear()')
        self.write('smua.nvbuffer2.clear()')
        self.write('smub.nvbuffer1.clear()')
        self.write('smub.nvbuffer2.clear()')

        self.write('smua.nvbuffer1.clearcache()')
        self.write('smua.nvbuffer2.clearcache()')
        self.write('smub.nvbuffer1.clearcache()')
        self.write('smub.nvbuffer2.clearcache()')

        # diplay current during measurement
        self.write('display.smua.measure.func = display.MEASURE_DCAMPS')
        self.write('display.smub.measure.func = display.MEASURE_DCAMPS')

        # SETUP TRIGGER ARM AND COUNTS
        # trigger count = number of data points in measurement
        # arm count = number of times the measurement is repeater (set to 1)

        self.write('smua.trigger.count = %d' % numPoints)
        self.write('smub.trigger.count = %d' % numPoints)

        # SET THE MEASUREMENT TRIGGER ON BOTH SMU'S
        # Set measurment to trigger once a change in the gate value on
        # sweep smu is complete, i.e., a measurment will occur
        # after the voltage is stepped.
        # Both channels should be set to trigger on the sweep smu event
        # so the measurements occur at the same time.

        # enable smu
        self.write('smua.trigger.measure.action = smua.ENABLE')
        self.write('smub.trigger.measure.action = smub.ENABLE')
        # measure current on trigger
        self.write('smua.trigger.measure.iv(smua.nvbuffer1, smua.nvbuffer2)')
        self.write('smub.trigger.measure.iv(smub.nvbuffer1, smub.nvbuffer2)')
        # initiate measure trigger when source is complete
        self.write('smua.trigger.measure.stimulus = smua.trigger.SOURCE_COMPLETE_EVENT_ID')
        self.write('smub.trigger.measure.stimulus = smua.trigger.SOURCE_COMPLETE_EVENT_ID')

        # SET THE ENDPULSE ACTION TO HOLD
        # Options are SOURCE_HOLD AND SOURCE_IDLE, hold maintains same voltage
        # throughout step in sweep (typical IV sweep behavior). idle will allow
        # pulsed IV sweeps.

        if pulsed:
            endPulseAction = 'SOURCE_IDLE'
        elif not pulsed:
            endPulseAction = 'SOURCE_HOLD'

        self.write('smua.trigger.endpulse.action = smua.%s' % endPulseAction)
        self.write('smub.trigger.endpulse.action = smub.%s' % endPulseAction)

        # SET THE ENDSWEEP ACTION TO HOLD
        # Output voltage will be held after sweep is done.

        self.write('smua.trigger.endsweep.action = smua.%s' % endPulseAction)
        self.write('smub.trigger.endsweep.action = smub.%s' % endPulseAction)

        # SET THE EVENT TO TRIGGER THE SMU'S TO THE ARM LAYER
        # A typical measurement goes from idle -> arm -> trigger.
        # The 'trigger.event_id' option sets the transition arm -> trigger
        # to occur after sending *trg to the instrument.

        self.write('smua.trigger.arm.stimulus = trigger.EVENT_ID')

        # Prepare an event blender (blender #1) that triggers when
        # the smua enters the trigger layer or reaches the end of a
        # single trigger layer cycle.

        # triggers when either of the stimuli are true ('or enable')
        self.write('trigger.blender[1].orenable = true')
        self.write('trigger.blender[1].stimulus[1] = smua.trigger.ARMED_EVENT_ID')
        self.write('trigger.blender[1].stimulus[2] = smua.trigger.PULSE_COMPLETE_EVENT_ID')

        # SET THE SMUA SOURCE STIMULUS TO BE EVENT BLENDER #1
        # A source measure cycle within the trigger layer will occur when either
        # the trigger layer is entered (termed 'armed event') for the first time or a single cycle of the
        # trigger layer is complete (termed 'pulse complete event').

        self.write('smua.trigger.source.stimulus = trigger.blender[1].EVENT_ID')

        # PREPARE AN EVENT BLENDER (blender #2) THAT TRIGGERS WHEN BOTH SMU'S HAVE
        # COMPLETED A MEASUREMENT.
        # This is needed to prevent the next source measure cycle from occuring
        # before the measurement on both channels is complete.

        self.write('trigger.blender[2].orenable = false')  # triggers when both stimuli are true
        self.write('trigger.blender[2].stimulus[1] = smua.trigger.MEASURE_COMPLETE_EVENT_ID')
        self.write('trigger.blender[2].stimulus[2] = smub.trigger.MEASURE_COMPLETE_EVENT_ID')

        # SET THE SMUA ENDPULSE STIMULUS TO BE EVENT BLENDER #2
        self.write('smua.trigger.endpulse.stimulus = trigger.blender[2].EVENT_ID')

        # TURN ON SMUA AND SMUB
        self.write('smua.source.output = smua.OUTPUT_ON')
        self.write('smub.source.output = smub.OUTPUT_ON')

        # INITIATE MEASUREMENT
        # prepare SMUs to wait for trigger
        self.write('smua.trigger.initiate()')
        self.write('smub.trigger.initiate()')
        # send trigger
        self.write('*trg')

        # CHECK STATUS BUFFER FOR MEASUREMENT TO FINISH
        # Possible return values:
        # 6 = smua and smub sweeping
        # 4 = only smub sweeping
        # 2 = only smua sweeping
        # 0 = neither smu sweeping

        statusCheck = 0
        while statusCheck == 0:  # while loop that runs until the sweep begins
            status = self.query('status.operation.sweeping.condition')
            statusCheck = float(status)

        while statusCheck > 0:  # while loop that runs until the sweep ends
            status = self.query('status.operation.sweeping.condition')
            statusCheck = float(status)

        # EXTRACT DATA FROM SMU BUFFERS

        Vg = self.readBuffer('smua.nvbuffer2')
        Vd = self.readBuffer('smub.nvbuffer2')
        Ig = self.readBuffer('smua.nvbuffer1')
        Id = self.readBuffer('smub.nvbuffer1')

        self.clearCaches()
        self.idleSig.emit()

        return Vg, Vd, Ig, Id

# =============================================================================
# Define higher level control functions
# =============================================================================

    def applyCurrent(self, smu, curr):
        """
        Sources a current from the selected SMU.
        """

        SMUS = ['smua', 'smub']

        assert smu in SMUS, 'Please select a valid SMU.'

        self.write('%s.source.leveli = %s' % (smu, curr))
        self.turnOn(smu)

    def setGateVoltage(self, Vg, delay=0.1, stepSize=1):
        """
        Ramps up the voltage of the SMU specified as gate.
        INPUT:
            Vg - target gate voltage
            stepSize - size of voltage ramp steps in Volts
            delay -  delay between steps in sec
        """
        self.busySig.emit()
        logger.status('Setting gate voltage to %s V.' % round(Vg))
        self.turnOn(self.gate)
        self.turnOff(self.drain)

        self.rampToVoltage(targetVolt=Vg, SMU=self.gate)

        if Vg == 0:
            self.write('reset()')

        self.beep()
        self.idleSig.emit()

    def transferMeasurement(self, VgStart=DEFAULTS['VgStart'],
                            VgStop=DEFAULTS['VgStop'],
                            VgStep=DEFAULTS['VgStep'],
                            VdList=DEFAULTS['VdList'], filepath=None,
                            plot=True, tInt=DEFAULTS['tInt'],
                            delay=DEFAULTS['delay'],
                            pulsed=DEFAULTS['pulsed']):

        """
        Records a transfer curve and saves the results in a SweepData instance.
        """
        self.busySig.emit()
        self.abort_event.clear()
        logger.info('Recording transfer curve with Vg from %sV to %sV, Vd = %s V. ' % (VgStart, VgStop, VdList))

        # create SweepData instance
        self.sweepData = SweepData(sweepType='transfer')

        for Vdrain in VdList:
            if self.abort_event.is_set():
                self.reset()
                return self.sweepData

            logger.status('Vd = %sV.' % Vdrain)
            # conduct forward and reverse sweeps
            logger.status('Forward sweep.')
            VgFWD, VdFWD, IgFWD, IdFWD = self.voltageSweep(self.gate, VgStart, VgStop, -abs(VgStep), Vdrain, tInt, delay, pulsed)
            logger.status('Backward sweep.')
            VgRVS, VdRVS, IgRVS, IdRVS = self.voltageSweep(self.gate, VgStop, VgStart, abs(VgStep), Vdrain, tInt, delay, pulsed)

            if not self.abort_event.is_set():
                # add data to SweepData instance
                # discard data if aborted by user
                self.sweepData.append(VgFWD, VdFWD, IgFWD, IdFWD)
                self.sweepData.append(VgRVS, VdRVS, IgRVS, IdRVS)

        self.reset()

        # plot data
        if plot:
            self.sweepData.plot()
        # save data
        if filepath is not None:
            try:
                filepath = self.sweepData.save(filepath)
                logger.info('Transfer data saved to %s.' % filepath)
            except:
                logger.error('Data could not be saved.')

        self.idleSig.emit()
        return self.sweepData

    def outputMeasurement(self, VdStart=DEFAULTS['VdStart'],
                          VdStop=DEFAULTS['VdStop'],
                          VdStep=DEFAULTS['VdStep'],
                          VgList=DEFAULTS['VgList'], filepath=None,
                          plot=True, tInt=DEFAULTS['tInt'],
                          delay=DEFAULTS['delay'],
                          pulsed=DEFAULTS['pulsed']):
        """
        Records a output curve and saves the results in a SweepData instance.
        """
        self.busySig.emit()
        self.abort_event.clear()
        logger.info('Recording output curve with Vd from %sV to %sV, Vg = %s V. ' % (VdStart, VdStop, VgList))

        # create SweepData instance
        self.sweepData = SweepData(sweepType='output')

        for Vgate in VgList:
            if self.abort_event.is_set():
                self.reset()
                return self.sweepData

            logger.status('Vg = %sV.' % Vgate)
            # conduct forward and reverse sweeps
            logger.status('Forward sweep.')
            VgFWD, VdFWD, IgFWD, IdFWD = self.voltageSweep(self.drain, VdStart, VdStop, -abs(VdStep), Vgate, tInt, delay, pulsed)
            logger.status('Backward sweep.')
            VgRVS, VdRVS, IgRVS, IdRVS = self.voltageSweep(self.drain, VdStop, VdStart, abs(VdStep), Vgate, tInt, delay, pulsed)

            if not self.abort_event.is_set():
                # add data to SweepData instance
                # discard data if aborted by user
                self.sweepData.append(VgFWD, VdFWD, IgFWD, IdFWD)
                self.sweepData.append(VgRVS, VdRVS, IgRVS, IdRVS)

        self.reset()
        # plot data
        if plot:
            self.sweepData.plot()
        # save data
        if filepath is not None:
            try:
                filepath = self.sweepData.save(filepath)
                logger.info('Output data saved to %s.' % filepath)
            except:
                logger.error('Data could not be saved.')

        self.idleSig.emit()
        return self.sweepData
