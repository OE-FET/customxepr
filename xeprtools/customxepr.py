#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""

from __future__ import division, absolute_import

# system imports
import sys
import os
from threading import Event
from qtpy import QtCore
from decorator import decorator
import time
import numpy as np
import logging

__author__ = 'Sam Schott <ss2151@cam.ac.uk>'
__year__ = str(time.localtime().tm_year)
__version__ = 'v2.0.1'

# custom imports
from utils.mail import TlsSMTPHandler
from utils.py3compat import Queue
from xeprtools.mode_picture import ModePicture
from config.main import CONF

try:
    sys.path.insert(0, os.popen("Xepr --apipath").read())
    from XeprAPI import ParameterError, ExperimentError
except ImportError:
    logging.info('XeprAPI could not be located. Please make sure that ' +
                 'is installed on your system.')


# add logging level for status updates between DEBUG (10) and INFO (20)

logging.STATUS = 15
logging.addLevelName(logging.STATUS, 'STATUS')
logger = logging.getLogger(__name__)
logger.setLevel(logging.STATUS)
setattr(logger, 'status', lambda message,
        *args: logger._log(logging.STATUS, message, args))


# =============================================================================
# define queued excecution decorator which dumps a method call into a queue
# =============================================================================

def queued_exec(queue):
    """
    Wrapper that ads a method call with *args and **kwargs to a queue instead
    of excecuting in the main thread.
    """
    @decorator
    def put_to_queue(func, *args, **kwargs):
        queue.put((func, args, kwargs))

    return put_to_queue


# =============================================================================
# define worker that gets method calls from queue and performs them
# =============================================================================

class Excecutioner(QtCore.QObject):
    """
    Worker that gets all method calls with args from job_q and executes them.
    Results are then stored in the result_q.

    Arguments:
    job_q       -- Queue with jobs to be performed.
    result_q    -- Queue with results from completed jobs.
    pause       -- Event that causes the worker to pause between jobs if set.
    """

    def __init__(self, job_q, result_q, pause_event):
        super(self.__class__, self).__init__(None)
        self.job_q = job_q
        self.result_q = result_q
        self.pause_event = pause_event

    def process(self):
        while True:
            time.sleep(0.1)

            if self.pause_event.is_set():
                logger.status('PAUSED')

            while self.pause_event.is_set():
                time.sleep(0.1)

            if not self.job_q.empty():
                func, args, kwargs = self.job_q.get()
                # Try to perform a job. Any exceptions are logged.
                try:
                    result = func(*args, **kwargs)
                    if result is not None:
                        self.result_q.put(result)
                    logger.status('IDLE')

                except:
                    # log exception and pause excecution of jobs
                    logger.exception('EXCEPTION')
                    self.pause_event.set()
                    logger.status('PAUSED')

                self.job_q.task_done()


# =============================================================================
# define custom queue which emits PyQt signals
# =============================================================================

class SignalQueue(QtCore.QObject, Queue):

    put_signal = QtCore.Signal()
    pop_signal = QtCore.Signal()

    def __init__(self):
        super(SignalQueue, self).__init__()
        Queue.__init__(self)

    # Put a new item in the queue, emit put_signal
    def _put(self, item):
        self.queue.append(item)
        self.put_signal.emit()

    # Get an item from the queue, emit pop_signal
    def _get(self):
        item = self.queue.popleft()
        self.pop_signal.emit()
        return item


# =============================================================================
# define CustomXepr class
# =============================================================================

class CustomXepr(QtCore.QObject):
    """
    Custom Xepr routines such as tuning and setting the temperature, applying
    voltages and recording IV characteristics with an attached keithley SMU.
    All CustomXepr methods are executed in a worker thread in the order of
    their calls. To execute an external function in this thread, add it to the
    job queue:

    >>> job = (func, args, kwargs)
    >>> customXepr.job_queue.put(job)

    All results are added to the result queue and can be retrieved with:

    >>> result = customXepr.result_queue.get()

    To pause or resume the worker between jobs, do

    >>> customXepr.pause_event.set()

    or

    >>> customXepr.pause_event.clear()

    CustomXepr functions:
        customXepr.clear_all_jobs()
        customXepr.sendEmail(text)
        customXepr.pause(seconds)

    CustomXepr properties:
        customXepr.notify_address = 'ss2151@cam.ac.uk'
        customXepr.log_file_dir = '~/.CustomXepr/LOG_FILES'
        customXepr.email_handler_level = logging.WARNING

    ESR methods:
        customXepr.connectToESR()
        customXepr.tune()
        customXepr.finetune()
        customXepr.customtune()
        customXepr.getQValueFromXepr(direct=None, T=298)
        customXepr.getQValueCalc(direct=None, T=298)
        customXepr.runXeprExperiment(exp, **kwargs)
        customXepr.saveCurrentData(path, title=None, exp=None)
        customXepr.setStandby()
        customXepr.getCurrentLinewidth()

    MercuryiTC methods:
        customXepr.setTemperature(T_target)
        customXepr.setTempRamp(ramp)
        customXepr.heater_target(T)

    Keithley methods:
        customXepr.transferMeasurement(path=None, **kwargs)
        customXepr.outputMeasurement(path=None,  **kwargs)
        customXepr.setGateVoltage(Vg)
        customXepr.applyDrainCurrent(smu, curr)

    See output of help(CustomXepr) for full documentation.

    """

# =============================================================================
# set up basic customXepr functionality
# =============================================================================

    job_queue = SignalQueue()
    result_queue = SignalQueue()
    pause_event = Event()
    abort_event = Event()

    def __init__(self, Xepr=None, mercury_feed=None, keithley=None):

        super(CustomXepr, self).__init__()

        # =====================================================================
        # check if conections to Xepr, MercuryiTC and Keithley are present
        # =====================================================================

        self.Xepr = Xepr
        self.feed = mercury_feed
        self.keithley = keithley
        # hidden Xepr experiemnt, running when EPR is connected:
        self.hidden = None

        if not self.Xepr:
            logger.info('No Xepr instance supplied. Functions that ' +
                        'require Xepr will not work.')
        elif not self.Xepr.XeprActive():
            logger.info('XeprAPI not active. Please activate Xepr API.')
        else:
            self.XeprCmds = self.Xepr.XeprCmds
            self.connectToESR()

        if not self.feed or not self.feed.mercury:
            logger.info('No MercuryiTC instance supplied. Functions that' +
                        ' require a connected cryostat will not work.')

        if not self.keithley or not self.keithley._keithley:
            logger.info('No Keithley instance supplied. Functions that ' +
                        'require a connected Keithley SMU will not work.')

        # =====================================================================
        # create background thread to process all excecutions in queue
        # =====================================================================

        self.worker_thread = QtCore.QThread()
        self.worker_thread.setObjectName('CustomXeprThread')
        self.worker = Excecutioner(self.job_queue, self.result_queue,
                                   self.pause_event)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.process)
        self.worker_thread.start()
        logger.status('IDLE')

        # =====================================================================
        # define certain settings for customXepr functions
        # =====================================================================

        # waiting time for Xepr to process commands
        self.wait = 0.2
        # settling time for cryostat temperature
        self._temp_wait_time = CONF.get('CustomXepr', 'temp_wait_time')
        # temperature stability tolerance
        self._temperature_tolerance = CONF.get('CustomXepr',
                                               'temperature_tolerance')

# =============================================================================
# define basic functions for email notifictions, pausing, etc.
# =============================================================================

    def clear_all_jobs(self):
        """ Clears all pending jobs in job_queue."""
        for item in range(0, self.job_queue.qsize()):
            self.job_queue.get()

    @queued_exec(job_queue)
    def sendEmail(self, text):
        """
        Sends a text to the default email address.
        """
        logger.warning(text)

    @queued_exec(job_queue)
    def pause(self, seconds):
        """
        Pauses for the specified amount of seconds. This pause function checks
        for an abort signal every minute to prevent permanent blocking.
        """
        ETA = time.time() + seconds
        ETA_string = time.strftime('%H:%M', time.localtime(ETA))
        message = 'Waiting for %s seconds, ETA: %s.'
        logger.info(message % (int(seconds), ETA_string))

        # breack up into 1 sec sleep intervals, give option to abort
        if seconds > 1:
            for i in range(0, seconds):
                time.sleep(1)
                logger.status('Waiting %s/%s' % (i+1, seconds))
                # check for abort event
                if self.abort_event.is_set():
                    self.abort_event.clear()
                    logger.info('Aborted by user.')
                    return
        # use a single sleep command for less than one second pause
        else:
            time.sleep(seconds)

    @property
    def temp_wait_time(self):
        """Wait time until temperature is considered stable."""
        return self._temp_wait_time

    @temp_wait_time.setter
    def temp_wait_time(self, newtime):
        """Setter: Wait time until temperature is considered stable."""
        self._temp_wait_time = newtime
        # update config file
        CONF.set('CustomXepr', 'temp_wait_time', newtime)

    @property
    def temperature_tolerance(self):
        """Temperature fluctuation tolerance."""
        return self._temperature_tolerance

    @temperature_tolerance.setter
    def temperature_tolerance(self, newtol):
        """Setter: Temperature fluctuation tolerance."""
        self._temperature_tolerance = newtol
        # update config file
        CONF.set('CustomXepr', 'temperature_tolerance', newtol)

    @property
    def notify_address(self):
        """Address list for email notifications."""
        # get root logger
        root_logger = logging.getLogger()
        # find all email handlers (there should be only one)
        eh = [x for x in root_logger.handlers if type(x) == TlsSMTPHandler]

        if len(eh) == 0:
            logging.warning('No email handler could be found.')

        elif len(eh) > 0:
            # get emails from all handlers
            email_list = []
            for handler in eh:
                email_list += handler.toaddrs
            # remove duplicates and return
            return list(set(email_list))

    @notify_address.setter
    def notify_address(self, email_list):
        """ Setter: address list for email notifications."""
        # get root logger
        root_logger = logging.getLogger()
        # find all email handlers (there should be only one)
        eh = [x for x in root_logger.handlers if type(x) == TlsSMTPHandler]

        if len(eh) == 0:
            logging.warning('No email handler could be found.')
        elif len(eh) > 0:
            for handler in eh:
                handler.toaddrs = email_list

        email_list_str = ', '.join(email_list)
        logger.info('Email notifications will be sent to '
                    + email_list_str + '.')

        # update conf file
        CONF.set('CustomXepr', 'notify_address', email_list)

    @property
    def log_file_dir(self):
        """Directory for log files."""
        # get root logger
        root_log = logging.getLogger()
        # find all email handlers (there should be only one)
        fh = [x for x in root_log.handlers if type(x) == logging.FileHandler]

        if len(fh) == 0:
            logging.warning('No file handler could be found.')
        else:
            fileName = fh[0].baseFilename
            return os.path.dirname(fileName)

    @property
    def email_handler_level(self):
        """ Setter: logging level for email notifications."""
        # get root logger
        root_logger = logging.getLogger()
        # find all email handlers (there should be only one)
        eh = [x for x in root_logger.handlers if type(x) == TlsSMTPHandler]

        if len(eh) == 0:
            logging.warning('No email handler could be found.')
        else:
            return eh[0].level

    @email_handler_level.setter
    def email_handler_level(self, level=logging.WARNING):
        """Logging level for email notifications."""
        # get root logger
        root_logger = logging.getLogger()
        # find all email handlers (there should be only one)
        eh = [x for x in root_logger.handlers if type(x) == TlsSMTPHandler]

        if len(eh) == 0:
            logging.warning('No email handler could be found.')
        else:
            eh[0].setLevel(level)
        # update conf file
        CONF.set('CustomXepr', 'email_handler_level', level)

# =============================================================================
# set up Xepr functions
# =============================================================================

    @queued_exec(job_queue)
    def connectToESR(self):
        """
        Establishes connection to acquisition server if a spectrometer is
        connected.
        """
        try:
            self.hidden = self.Xepr.XeprExperiment('AcqHidden')
        except ExperimentError:
            try:
                logger.info('Connecting to spectrometer.')
                self.XeprCmds.aqSetServer('localhost')
                self.hidden = self.Xepr.XeprExperiment('AcqHidden')
            except ValueError:
                logger.warning('Cannot find spectrometer: timeout.')

    @queued_exec(job_queue)
    def tune(self):
        """
        Performs the Xepr built-in tuning routine.
        """

        if not self.hidden:
            logger.info('Bruker ESR is not connected. Functions that ' +
                        'require a connected ESR will not work.')
            return

        self.XeprCmds.aqParSet('AcqHidden', '*cwBridge.OpMode', 'Tune')
        self.XeprCmds.aqParSet('AcqHidden', '*cwBridge.Tune', 'Up')

    @queued_exec(job_queue)
    def finetune(self):
        """
        Performs the Xepr built-in fine-tuning routine.
        """

        if not self.hidden:
            logger.info('Bruker ESR is not connected. Functions that ' +
                        'require a connected ESR will not work.')
            return

        self.XeprCmds.aqParSet('AcqHidden', '*cwBridge.Tune', 'Fine')

    @queued_exec(job_queue)
    def customtune(self):
        """
        Custom tuning routine with better accuracy.
        Takes longer than tune() and requires the spectrometer to
        be already close to tuned.
        """

        if not self.hidden:
            logger.info('Bruker ESR is not connected. Functions that ' +
                        'require a connected ESR will not work.')
            return

        logger.info('Tuning')

        self.hidden = self.Xepr.XeprExperiment('AcqHidden')
        time.sleep(self.wait)
        mode = self.hidden['OpMode'].value
        time.sleep(self.wait)
        atten_start = self.hidden['PowerAtten'].value
        time.sleep(self.wait)
        if not mode == 'Operate':
            self.hidden['OpMode'].value = 'Operate'
            time.sleep(self.wait)

        self.hidden['PowerAtten'].value = 30
        time.sleep(self.wait)
        self._tuneFreq()
        time.sleep(self.wait)

        self.hidden['PowerAtten'].value = 50
        self._tuneBias()

        for atten in range(40, 0, -10):
            # check for abort event, clear event
            if self.abort_event.is_set():
                self.abort_event.clear()
                self.hidden['PowerAtten'].value = atten_start
                time.sleep(self.wait)
                logger.info('Aborted by user.')
                return

            self.hidden['PowerAtten'].value = atten

            self._tunePhase()
            self._tuneIris()

        self._tuneFreq()
        self.hidden['PowerAtten'].value = 45
        self._tuneBias()

        self.hidden['PowerAtten'].value = 20
        self._tunePhase()
        self._tuneIris()

        self.hidden['PowerAtten'].value = 45
        self._tuneBias()

        self.hidden['PowerAtten'].value = 10
        self._tuneIris()

        self.hidden['PowerAtten'].value = atten_start
        time.sleep(self.wait)

        # check for abort event, clear event
        if self.abort_event.is_set():
            self.abort_event.clear()
            logger.info('Aborted by user.')
            return

        logger.status('Tuning done.')

    def _tuneBias(self):
        """Tunes the diode bias. A perfectly tuned bias results in a diode
        current of 200 mA for all microwave powers."""

        # check for abort event
        if self.abort_event.is_set():
            return

        logger.status('Tuning (Bias)')
        time.sleep(self.wait)

        # get offset from 200 mA
        diff = self.hidden['DiodeCurrent'].value - 200
        tolerance1 = 10  # tolerance for fast tuning
        tolerance2 = 1  # tolerance for second fine tuning

        # rapid tuning with high tolerance and large steps
        while abs(diff) > tolerance1:
            # check for abort event
            if self.abort_event.is_set():
                return

            step = 1*cmp(0, diff)  # coarse step of 1
            self.XeprCmds.aqParStep('AcqHidden', '*cwBridge.SignalBias',
                                    'Coarse %s' % step)
            time.sleep(0.5)
            diff = self.hidden['DiodeCurrent'].value - 200

        # fine tuning with low tolerance and small steps
        while abs(diff) > tolerance2:
            # check for abort event
            if self.abort_event.is_set():
                return

            step = 5*cmp(0, diff)  # fine step of 5
            self.XeprCmds.aqParStep('AcqHidden', '*cwBridge.SignalBias',
                                    'Fine %s' % step)
            time.sleep(0.5)
            diff = self.hidden['DiodeCurrent'].value - 200

    def _tuneIris(self, tolerance=1):
        """Tunes the cavity's iris. A perfectly tuned iris results in a diode
        current of 200 mA for all microwave powers."""
        # check for abort event
        if self.abort_event.is_set():
            return

        logger.status('Tuning (Iris)')
        time.sleep(self.wait)

        diff = self.hidden['DiodeCurrent'].value - 200

        while abs(diff) > tolerance:
            # check for abort event
            if self.abort_event.is_set():
                return

            if diff < 0:
                cmd = '*cwBridge.IrisUp'
            elif diff > 0:
                cmd = '*cwBridge.IrisDown'
            else:
                return

            # determine step size for iris adjustment: slower adjustment when
            # close to a diode current of 200, minimum step size of 0.3
            step_size = max(abs(diff), 30) * 0.01
            # scale step size for MW power: smaller steps at higher power
            step = step_size * (self.hidden['PowerAtten'].value**2)/400
            # set value to 0.1 if step is smaller
            # (usually only happens below 10dB)
            step = max(step, 0.1)
            # increase waiting time between steps when close to tuned
            # with a maximum waiting of 1 sec
            wait = min(5/(abs(diff) + 0.1), 1)
            self.XeprCmds.aqParSet('AcqHidden', cmd, 'True')
            time.sleep(step)
            self.XeprCmds.aqParSet('AcqHidden', cmd, 'False')
            time.sleep(wait)
            diff = self.hidden['DiodeCurrent'].value - 200

    def _tuneFreq(self, tolerance=3):
        """Tunes the microwave frequency to a lock offset of zero."""
        # check for abort event
        if self.abort_event.is_set():
            return

        logger.status('Tuning (Freq)')
        time.sleep(self.wait)

        fq_offset = self.hidden['LockOffset'].value

        while abs(fq_offset) > tolerance:
            # check for abort event
            if self.abort_event.is_set():
                return

            step = 1 * cmp(0, fq_offset) * max(abs(int(fq_offset/10)), 1)
            self.XeprCmds.aqParStep('AcqHidden', '*cwBridge.Frequency',
                                    'Fine %s' % step)
            time.sleep(1)
            fq_offset = self.hidden['LockOffset'].value

    def _tunePhase(self):
        """
        Tunes the phase of the MW reference arm to maximise the diode current.
        """
        # timeout for phase tuning
        self._tuning_timeout = 60
        # check for abort event
        if self.abort_event.is_set():
                return

        logger.status('Tuning (Phase)')
        time.sleep(self.wait)

        t0 = time.time()

        # get current phase and range
        phase0 = self.hidden['SignalPhase'].value
        phase_min = self.hidden['SignalPhase'].aqGetParMinValue()
        phase_max = self.hidden['SignalPhase'].aqGetParMaxValue()
        phase_step = self.hidden['SignalPhase'].aqGetParCoarseSteps()

        # determine direction of increasing diode current
        diode_curr_array = np.array([])
        interval_min = max(phase0-2*phase_step, phase_min)
        interval_max = min(phase0+2*phase_step, phase_max)
        phase_array = np.arange(interval_min, interval_max, phase_step)

        for phase in phase_array:
            # check for abort event
            if self.abort_event.is_set():
                return
            self.hidden['SignalPhase'].value = phase
            time.sleep(self.wait)
            diode_curr = self.hidden['DiodeCurrent'].value
            time.sleep(self.wait)
            diode_curr_array = np.append(diode_curr_array, diode_curr)
            if time.time() - t0 > self._tuning_timeout:
                logger.warning('Phase tuning timeout.')
                break

        # Determine position of maximum phase by stepping the phase until it
        # decreases again. Shift by 360° if maximum or minimum is encountered.

        self.hidden['SignalPhase'].value = phase0
        time.sleep(self.wait)

        upper = np.mean(diode_curr_array[phase_array > phase0])
        lower = np.mean(diode_curr_array[phase_array < phase0])

        direction = cmp(upper, lower)
        diode_curr_array = phase_array = np.array([])

        new_phase = phase0 + direction*phase_step

        # Check if phase is within limits, then step. otherwise shift phase
        # and return.
        deg_step = 6.5  # approximate step of 1 deg
        if new_phase > phase_max:
            logger.info('Phase at upper limit, reducing by 360 deg.')
            self.hidden['SignalPhase'].value = phase0 - 360*deg_step
            time.sleep(4)
            return
        elif new_phase < phase_min:
            logger.info('Phase at lower limit, increasing by 360 deg.')
            self.hidden['SignalPhase'].value = phase0 + 360*deg_step
            time.sleep(4)
            return
        else:
            self.hidden['SignalPhase'].value = new_phase
            time.sleep(self.wait)

        diode_curr_new = self.hidden['DiodeCurrent'].value
        time.sleep(self.wait)
        diode_curr_array = np.append(diode_curr_array, diode_curr_new)
        phase_array = np.append(phase_array, new_phase)

        while diode_curr_new > np.max(diode_curr_array) - 5:
            # check for abort event
            if self.abort_event.is_set():
                return
            # check for limits of diode range, reajust iris if necessary
            if diode_curr_new in [0, 400]:
                self._tuneIris()

            # calculate phase after step
            new_phase = new_phase + direction*phase_step
            # Check if phase is within limits, then step. otherwise shift phase
            # and return.
            if new_phase > phase_max or new_phase < phase_min:
                if new_phase > phase_max:
                    logger.info('Phase at upper limit, reducing by 360 deg.')
                    self.hidden['SignalPhase'].value = new_phase - 360*deg_step
                    time.sleep(4)
                    return
                elif new_phase < phase_min:
                    logger.info('Phase at lower limit, increasing by 360 deg.')
                    self.hidden['SignalPhase'].value = new_phase + 360*deg_step
                    time.sleep(4)
                    return
                else:
                    self.hidden['SignalPhase'].value = new_phase
                    time.sleep(self.wait)
            else:
                self.hidden['SignalPhase'].value = new_phase
                time.sleep(self.wait)

            diode_curr_new = self.hidden['DiodeCurrent'].value
            time.sleep(self.wait)
            diode_curr_array = np.append(diode_curr_array, diode_curr_new)
            phase_array = np.append(phase_array, new_phase)

            # set a tuning timeout if Xepr is not responsive
            if time.time() - t0 > self._tuning_timeout:
                logger.info('Phase tuning timeout.')
                break

        # set phase to best value
        phase_max = phase_array[np.argmax(diode_curr_array)]
        self.hidden['SignalPhase'].value = phase_max
        time.sleep(self.wait)

    @queued_exec(job_queue)
    def getQValueFromXepr(self, direct=None, T=298):
        """
        Reads out the resonator Q-value, averaged over 20 sec, and saves it
        in the specified file.
        """

        if not self.hidden:
            logger.info('Bruker ESR is not connected. Functions that ' +
                        'require a connected ESR will not work.')
            return

        wait_old = self.wait
        self.wait = 1

        logger.info('Reading Q-value.')

        att = self.hidden['PowerAtten'].value  # remember current attenuation
        time.sleep(self.wait)
        self.hidden['OpMode'].value = 'Tune'
        time.sleep(self.wait)
        self.hidden['RefArm'].value = 'On'
        time.sleep(self.wait)
        self.hidden['PowerAtten'].value = 33
        time.sleep(self.wait)
        self.hidden['ModeZoom'].value = 2
        time.sleep(self.wait)

        QValues = np.array([])

        time.sleep(1)

        for iteration in range(0, 40):
            QValues = np.append(QValues, self.hidden['QValue'].value)
            time.sleep(1)

        self.hidden['PowerAtten'].value = 32
        time.sleep(self.wait)
        self.hidden['ModeZoom'].value = 1
        time.sleep(self.wait)
        self.hidden['RefArm'].value = 'On'
        time.sleep(self.wait)
        self.hidden['OpMode'].value = 'Operate'

        time.sleep(3)

        self._tuneFreq()
        self._tuneFreq()
        self._tuneBias()
        self._tuneFreq()

        self.hidden['PowerAtten'].value = att
        time.sleep(self.wait)
        Qmean = QValues.mean()

        if direct is not None:
            path = os.path.join(direct, 'QValues.txt')
            self._saveQValue2File(T, Qmean, path)

        logger.info('Q = %i.' % Qmean)

        self.wait = wait_old

        return Qmean

    @queued_exec(job_queue)
    def getQValueCalc(self, direct=None, T=None):
        """
        Calculates Q-Value from tuning picture.
        """

        if not self.hidden:
            logger.info('Bruker ESR is not connected. Functions that ' +
                        'require a connected ESR will not work.')
            return

        # get temperature from MercuryiTC if connected, else use T = 298K
        if not T:
            try:
                T = self.feed.readings['Temp']
            except AttributeError:
                T = 298

        wait_old = self.wait
        self.wait = 1

        logger.info('Reading Q-value.')
        att = self.hidden['PowerAtten'].value  # remember current attenuation
        time.sleep(self.wait)
        freq = self.hidden['FrequencyMon'].value  # get current frequency
        time.sleep(self.wait)

        self.hidden['OpMode'].value = 'Tune'
        time.sleep(self.wait)
        self.hidden['RefArm'].value = 'Off'
        time.sleep(self.wait)
        self.hidden['PowerAtten'].value = 33
        time.sleep(1)

        self.hidden['PowerAtten'].value = 20
        time.sleep(2)

        # collect mode pictures for different zoom levels
        self.modePicData = {}

        for modeZoom in [1, 2, 4, 8]:
            yData = np.array([])

            self.hidden['ModeZoom'].value = modeZoom
            time.sleep(2)

            nPoints = int(self.hidden['DataRange'][1])
            time.sleep(self.wait)

            for i in range(0, nPoints):
                yData = np.append(yData, self.hidden['Data'][i])

            self.modePicData[modeZoom] = yData

        self.modePictureObj = ModePicture(self.modePicData, freq)
        QValue = self.modePictureObj.QValue

        self.hidden['PowerAtten'].value = 30
        time.sleep(self.wait)
        self.hidden['ModeZoom'].value = 1
        time.sleep(self.wait)
        self.hidden['RefArm'].value = 'On'
        time.sleep(self.wait)
        self.hidden['OpMode'].value = 'Operate'

        time.sleep(3)

        self._tuneFreq()
        self._tuneFreq()
        self._tuneBias()
        self._tuneFreq()

        self.hidden['PowerAtten'].value = att
        time.sleep(self.wait)

        if QValue > 3000:
            logger.info('Q = %i.' % QValue)
        elif QValue <= 3000:
            logger.warning('Q = %i is very small. Please check-up ' % QValue +
                           'on experiment.')

        if direct is None:
            pass
        elif os.path.isdir(direct):
            path = os.path.join(direct, 'QValues.txt')
            self._saveQValue2File(T, QValue, path)
            path = os.path.join(direct, 'ModePicture' +
                                str(int(T)).zfill(3) + 'K.txt')
            self.modePictureObj.save(path)
        else:
            raise RuntimeError('No such directory "%s"' % direct)

        self.wait = wait_old

        return self.modePictureObj

    def _saveQValue2File(self, T, QValue, path):

        time_str = time.strftime('%Y-%m-%d %H:%M')
        string = '%s\t%d\t%s\n' % (time_str, T, QValue)

        if os.path.isfile(path):
            with open(path, 'a') as file_handle:
                file_handle.write(string)
        else:
            header = 'Time stamp\tTemperature [K]\tQValue\n'
            with open(path, 'a') as file_handle:
                file_handle.write(header)
                file_handle.write(string)

    @queued_exec(job_queue)
    def runXeprExperiment(self, exp, **kwargs):
        """
        Runs the Xepr experiment given by "exp". Keyword arguments (kwargs)
        allow the user to pass experiment parameters. If multiple scans are
        performed, the frequency is tuned between scans.
        """

        if not self.hidden:
            logger.info('Bruker ESR is not connected. Functions that ' +
                        'require a connected ESR will not work.')
            return

        # -----------set experiment parameters if given in kwargs--------------
        for key in kwargs:
            exp[key].value = kwargs[key]

        # -------------- estimate running time --------------------------------
        sweepTime = exp['SweepTime'].value
        time.sleep(self.wait)
        nScans = exp['NbScansToDo'].value
        time.sleep(self.wait)

        try:
            # get number of second axis steps
            self.exp = exp
            self.sweepData = exp['SweepData'].value
            time.sleep(self.wait)
            self.sweepData = exp['SweepData'].value
            time.sleep(self.wait)
            ypts = len(self.sweepData.split())

            # get NbPoints if SweepData is empty string
            if ypts == 0:
                ypts = exp['NbPoints'].value
                time.sleep(self.wait)
            # get settling time between steps in seconds
            delay = exp['Delay'].value / 1000
        # catch exception in case of 1D experiment
        except ParameterError:
            ypts = 1
            delay = 0

        experiment_sec = sweepTime*nScans*ypts + delay

        ETA = time.time() + experiment_sec
        ETA_string = time.strftime('%H:%M', time.localtime(ETA))
        message = 'Measurement "%s" running. Estimated time: %s min, ETA: %s.'
        logger.info(message % (exp.aqGetExpName(), int(experiment_sec/60),
                               ETA_string))

        # -------------------start experiment----------------------------------

        if self.feed is not None and self.feed.mercury is not None:
            self.T_history = np.array([])

        exp.select()
        time.sleep(self.wait)
        exp.aqExpRun()
        time.sleep(self.wait)

        # wait for expriment to start
        while not exp.isRunning:
            time.sleep(self.wait)

        time.sleep(1)
        exp.aqExpPause()
        time.sleep(self.wait)

        while (exp.isRunning or exp.isPaused):

            # check for abort event
            if self.abort_event.is_set():
                exp.aqExpPause()
                self.abort_event.clear()
                logger.info('Aborted by user.')
                return

            NbScansDone = exp['NbScansDone'].value
            NbScansToDo = exp['NbScansToDo'].value
            logger.status('Recording scan %i of %i'
                          % (NbScansDone+1, NbScansToDo))

            # tune frequency when a new slice scan starts
            if (exp.isPaused and not NbScansDone == NbScansToDo):
                logger.status('Checking tuned.')

                self._tuneFreq(tolerance=3)
                time.sleep(1)
                self._tuneFreq(tolerance=3)
                time.sleep(self.wait)

                self._tuneIris(tolerance=5)
                time.sleep(self.wait)
                exp.aqExpRun()
                time.sleep(self.wait)
                while not exp.isRunning:
                    time.sleep(self.wait)

                time.sleep(1)
                exp.aqExpPause()
                time.sleep(self.wait)

            # record temperature and warn if fluctuations exceed the tolerance
            if self.feed is not None and self.feed.mercury is not None:
                T_curr = self.feed.readings['Temp']
                self.T_history = np.append(self.T_history, T_curr)
                # if temperature unstable, increment the number of violations
                # don't look at all historic data since temperature_tolerance
                # may have changed during the scan
                self.n_out += (abs(self.T_history[-1] - self.T_history[0]) >
                               2*self.temperature_tolerance)
                # warn once for every 120 violations
                if np.mod(self.n_out, 120) == 1:
                    logger.warning(u'Tempearature fluctuations > \xb1%sK.'
                                   % (2*self.temperature_tolerance))
                    self.n_out += 1  # prevent from warning again next second

                # Pause measurement and suspend all pending jobs after 15 min
                # of temperature instability
                if self.n_out > 60*15:
                    logger.error('Temperature could not be stabilized for ' +
                                 '15 min. Pausing current measurement and ' +
                                 'all pending jobs.')
                    exp.aqExpPause()
                    self.pause_event.set()
                    return

            time.sleep(1)

        # get temperature stability over scan if mercury was connected
        if self.feed is not None and self.feed.mercury is not None:
            T_var = max(self.T_history) - min(self.T_history)
            T_mean = np.mean(self.T_history)
            logger.info(u'Temperature stable at (%.2f\xb1%.2f)K during scans.'
                        % (T_mean, T_var/2))

        logger.info('All scans complete.')

        # -----------------get aquired dataset from Xepr and return------------
        # switch viewpoint to expriment which just finished running
        expTitle = exp.aqGetExpName()
        self.XeprCmds.aqExpSelect(1, expTitle)

        # get data set
        dset = self.Xepr.XeprDataset()

        return dset

    @queued_exec(job_queue)
    def saveCurrentData(self, path, title=None, exp=None):
        """
        Saves the data from given experiment in Xepr to the specified path. If
        exp = None the currently displayed dataset is saved.

        """

        if not self.hidden:
            logger.info('Bruker ESR is not connected. Functions that ' +
                        'require a connected ESR will not work.')
            return

        # switch viewpoint to experiment if given
        if exp is not None:
            expTitle = exp.aqGetExpName()
            self.XeprCmds.aqExpSelect(1, expTitle)

        # title = fileName if no title given
        if title is None:
            title = os.path.split(path)[1]

        # save data
        self.XeprCmds.ddPath(path)
        self.XeprCmds.vpSave('Current Primary', title,  path)
        logger.info('Data saved to %s.' % path)

    @queued_exec(job_queue)
    def setStandby(self):
        """
        Sets the magnetic field to zero and the MW bridge to standby.
        """

        if not self.hidden:
            logger.info('Bruker ESR is not connected. Functions that ' +
                        'require a connected ESR will not work.')
            return

        # check if WindDown experiment already exists, otherwise create
        try:
            self.wd = self.Xepr.XeprExperiment('WindDown')
        except ExperimentError:
            self.wd = self.Xepr.XeprExperiment('WindDown', exptype='C.W.',
                                               axs1='Field',
                                               ordaxs='Signal channel')
        time.sleep(self.wait)

        self.wd.aqExpActivate()
        time.sleep(self.wait)
        self.wd['CenterField'].value = 0
        time.sleep(self.wait)
        self.wd['AtCenter'].value = True
        time.sleep(self.wait)

        self.hidden['OpMode'].value = 'Tune'
        time.sleep(3)
        self.hidden['OpMode'].value = 'Stand By'
        time.sleep(self.wait)

        logger.info('EPR set to standby.')

    @queued_exec(job_queue)
    def getCurrentLinewidth(self):
        """
        Gets the peak-to-peak line width of the dataset currently displayed in
        Xepr.
        """

        if not self.hidden:
            logger.info('Bruker ESR is not connected. Functions that ' +
                        'require a connected ESR will not work.')
            return

        # get current dataset
        dset = self.Xepr.XeprDataset()
        time.sleep(self.wait)
        # determine peak to peak line width
        xData = dset.X
        yData = dset.O

        x2 = float(xData[yData == min(yData)])
        x1 = float(xData[yData == max(yData)])

        self.currentLineWidth = round(x2 - x1, 3)
        self.currentCenterRes = round(x1 + (x2 - x1)/2, 3)

        return self.currentLineWidth, self.currentCenterRes

# =============================================================================
# set up cryostat functions
# =============================================================================

    @queued_exec(job_queue)
    def setTemperature(self, T_target):
        """
        Sets the temperature for the ESR900 cryostat and waits for it to
        stabilize.
        """

        if not self.feed or not self.feed.mercury:
            logger.info('No MercuryiTC instance supplied. Functions that' +
                        ' require a connected cryostat will not work.')
            return

        self.T_target = T_target

        logger.info('Setting target temperature to %sK.' % self.T_target)

        # set temperature and wait to stabalize
        self.feed.control.t_setpoint = self.T_target
        self._waitStable()

        # check if gasflow is too high for temperature setpoint
        # if yes, reduce minimum value until target is reached
        ht = self.heater_target(self.T_target)
        fmin = self.feed.readings['FlowMin']

        heater_too_strong = (self.feed.readings['HeaterVolt'] > 1.2*ht)
        flow_at_min = (self.feed.readings['FlowPercent'] == fmin)

        if (heater_too_strong and flow_at_min):

            logger.warning('Gas flow is too high, trying to reduce.')
            self.feed.control.flow_auto = 'ON'
            self.feed.gasflow.gmin = max(self.feed.readings['FlowMin'] - 1, 1)

    def _waitStable(self):
        """
        Waits for the cryostat temperature to stabilize within the specified
        tolerance. Releases after it has been stable for 120 seconds.
        """

        # time in sec after which a timout warning is issued
        self._temperature_timeout = (self._ramp_time() + 30*60)  # in sec
        # counter for elapsed seconds since temperature has been stable
        stable_counter = 0
        # counter for setting gasflow to manual
        gasflow_man_counter = 0
        # starting time
        t0 = time.time()

        logger.info('Waiting for temperature to stabilize.')

        while stable_counter < self.temp_wait_time:
            # check for abort command
            if self.abort_event.is_set():
                self.abort_event.clear()
                logger.info('Aborted by user.')
                return

            # set gasflow to minimum for temperatures above 247K, this improves
            # the PID control and speeds up stabilization
            if gasflow_man_counter == 0:
                if self.feed.readings['Temp'] > 247 and self.T_target > 247:
                    self.feed.control.flow_auto = 'OFF'
                    self.feed.control.flow = self.feed.readings['FlowMin']
                else:
                    self.feed.control.flow_auto = 'ON'
                gasflow_man_counter += 1

            # check temperature deviation
            self.T_diff = abs(self.T_target - self.feed.readings['Temp'])
            if self.T_diff > self.temperature_tolerance:
                stable_counter = 0
                time.sleep(self.feed.refresh)
                logger.status('Waiting for temperature to stabilize.')
            else:
                stable_counter += self.feed.refresh
                logger.status('Stable for %s/%s sec.' % (stable_counter,
                                                         self.temp_wait_time))
                time.sleep(self.feed.refresh)

            # warn once if stabelization is taking longer than expected
            if time.time() - t0 > self._temperature_timeout:
                t0 = time.time()
                logger.warning('Temperature is taking too long to stablize.')

        message = 'Mercury iTC: Temperature is stable at %sK.' % self.T_target
        logger.warning(message)

    def heater_target(self, T):
        """
        Calculates the ideal heater voltage for a given temperature.
        """
        return 4.5*np.log(T)-5.5

    def _ramp_time(self):
        """
        Calculates the expected time in sec to reach the target temperature.
        Assumes a max ramping speed of 5 K/min if "ramp" is turned off.
        """
        if self.feed.readings['TempRampEnable'] == 'ON':
            expectedTime = (abs(self.T_target - self.feed.readings['Temp']) /
                            self.feed.readings['TempRamp'])  # in min
        elif self.feed.readings['TempRampEnable'] == 'OFF':
            expectedTime = (abs(self.T_target - self.feed.readings['Temp']) /
                            5)  # in min
        return expectedTime*60

    @queued_exec(job_queue)
    def setTempRamp(self, ramp):
        """
        Sets the temperature ramp for the ESR900 cryostat in K/min.
        """

        if not self.feed or not self.feed.mercury:
            logger.info('No MercuryiTC instance supplied. Functions that' +
                        ' require a connected cryostat will not work.')
            return

        # set temperature and wait to stabalize
        self.feed.control.ramp = ramp
        logger.info('Setting temperature ramp to %s K/min.' % ramp)

# =============================================================================
# set up Keithley functions
# =============================================================================

    @queued_exec(job_queue)
    def transferMeasurement(self, smu_gate=CONF.get('Keithley', 'gate'),
                            smu_drain=CONF.get('Keithley', 'drain'),
                            VgStart=CONF.get('Keithley', 'VgStart'),
                            VgStop=CONF.get('Keithley', 'VgStop'),
                            VgStep=CONF.get('Keithley', 'VgStep'),
                            VdList=CONF.get('Keithley', 'VdList'),
                            tInt=CONF.get('Keithley', 'tInt'),
                            delay=CONF.get('Keithley', 'delay'),
                            pulsed=CONF.get('Keithley', 'pulsed'),
                            path=None):
        """
        Performs a transfer measurement and returns a data instance.
        Saves the data in a .txt file if a path is specified.
        """

        if not self.keithley or not self.keithley.connected:
            logger.info('Keithley is not connnected. Functions that ' +
                        'require a connected Keithley SMU will not work.')
            return

        smu_gate = getattr(self.keithley, smu_gate)
        smu_drain = getattr(self.keithley, smu_drain)

        sd = self.keithley.transferMeasurement(smu_gate, smu_drain, VgStart,
                                               VgStop, VgStep, VdList, tInt,
                                               delay, pulsed)
        if path is not None:
            sd.save(path)

        return sd

    @queued_exec(job_queue)
    def outputMeasurement(self, smu_gate=CONF.get('Keithley', 'gate'),
                          smu_drain=CONF.get('Keithley', 'drain'),
                          VdStart=CONF.get('Keithley', 'VdStart'),
                          VdStop=CONF.get('Keithley', 'VdStop'),
                          VdStep=CONF.get('Keithley', 'VdStep'),
                          VgList=CONF.get('Keithley', 'VgList'),
                          tInt=CONF.get('Keithley', 'tInt'),
                          delay=CONF.get('Keithley', 'delay'),
                          pulsed=CONF.get('Keithley', 'pulsed'),
                          path=None):
        """
        Performs an output measurement and returns a data instance.
        Saves the data in a .txt file if a path is specified.
        """

        if not self.keithley or not self.keithley.connected:
            logger.info('Keithley is not connnected. Functions that ' +
                        'require a connected Keithley SMU will not work.')
            return

        smu_gate = getattr(self.keithley, smu_gate)
        smu_drain = getattr(self.keithley, smu_drain)

        sd = self.keithley.outputMeasurement(smu_gate, smu_drain, VdStart,
                                             VdStop, VdStep, VgList, tInt,
                                             delay, pulsed)
        if path is not None:
            sd.save(path)

        return sd

    @queued_exec(job_queue)
    def setGateVoltage(self, Vg, smu_gate=CONF.get('Keithley', 'gate')):
        """
        Sets the gate bias of the given keithley, grounds other SMUs.
        """

        if not self.keithley or not self.keithley.connected:
            logger.info('Keithley is not connnected. Functions that ' +
                        'require a connected Keithley SMU will not work.')
            return

        gate = getattr(self.keithley, smu_gate)

        # turn off all remaining SMUs
        other_smus = filter(lambda a: a != smu_gate, self.keithley.SMU_LIST)
        for smu_name in other_smus:
            smu = getattr(self.keithley, smu_name)
            smu.source.output = self.keithley.OUTPUT_OFF

        self.keithley.rampToVoltage(gate, targetVolt=Vg, delay=0.1, stepSize=1)

        if Vg == 0:
            self.keithley.reset()

    @queued_exec(job_queue)
    def applyDrainCurrent(self, I, smu=CONF.get('Keithley', 'drain')):
        """
        Sets a spcified current to the selected Keithley SMU.
        """

        if not self.keithley or not self.keithley.connected:
            logger.info('Keithley is not connnected. Functions that ' +
                        'require a connected Keithley SMU will not work.')
            return

        smu = getattr(self.keithley, smu)

        self.keithley.applyCurrent(smu, I)
        self.keithley.beep(0.3, 2400)

    @queued_exec(job_queue)
    def playChord(self):

        if not self.keithley or not self.keithley.connected:
            logger.info('Keithley is not connnected. Functions that ' +
                        'require a connected Keithley SMU will not work.')
            return

        self.keithley.beeper.beep(0.3, 1046.5)
        self.keithley.beeper.beep(0.3, 1318.5)
        self.keithley.beeper.beep(0.3, 1568)


# =============================================================================
# Set up loggers to send emails and write to log files
# =============================================================================

def setup_root_logger(NOTIFY):

    # Set up email notification handler for WARNING messages and above
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.STATUS)

    # find all email handlers (there should be none)
    eh = [x for x in root_logger.handlers if type(x) == TlsSMTPHandler]
    # find all file handlers (there should be none)
    fh = [x for x in root_logger.handlers if type(x) == logging.FileHandler]

    # define standard format of logging messages
    f = logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)s: ' +
                          '%(message)s', datefmt='%H:%M')

    if len(eh) == 0:
        # create and add email handler

        email_handler = TlsSMTPHandler('localhost', 'ss2151@cam.ac.uk',
                                       NOTIFY, 'Xepr logger')
        email_handler.setFormatter(f)
        email_handler.setLevel(CONF.get('CustomXepr', 'email_handler_level'))

        root_logger.addHandler(email_handler)

    # =========================================================================
    # Steptup logging to file
    # =========================================================================
    if len(fh) == 0:
        homePath = os.path.expanduser('~')
        loggingPath = os.path.join(homePath, '.CustomXepr', 'LOG_FILES')

        if not os.path.exists(loggingPath):
            os.makedirs(loggingPath)

        logFile = os.path.join(loggingPath, 'root_logger '
                               + time.strftime("%Y-%m-%d_%H-%M-%S"))
        file_handler = logging.FileHandler(logFile)
        file_handler.setFormatter(f)
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)


setup_root_logger(CONF.get('CustomXepr', 'notify_address'))
