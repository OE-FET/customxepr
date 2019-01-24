#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import
import sys
import os
import logging
import time
from threading import Event
import numpy as np
from qtpy import QtCore
from keithleygui import CONF as K_CONF

# local imports
from customxepr.utils.mail import TlsSMTPHandler, EmailSender
from customxepr.mode_picture import ModePicture
from customxepr.manager import ExperimentQueue, SignalQueue, Worker, queued_exec
from customxepr.config.main import CONF

try:
    sys.path.insert(0, os.popen("Xepr --apipath").read())
    from XeprAPI import ParameterError, ExperimentError
except ImportError:
    ParameterError = ExperimentError = RuntimeError
    logging.info('XeprAPI could not be located. Please make sure that ' +
                 'is installed on your system.')


__author__ = 'Sam Schott <ss2151@cam.ac.uk>'
__year__ = str(time.localtime().tm_year)
__version__ = 'v2.2.0'

PY2 = sys.version[0] == '2'

# add logging level for status updates between DEBUG (10) and INFO (20)
logging.STATUS = 15
logging.addLevelName(logging.STATUS, 'STATUS')
# noinspection PyProtectedMember
logger = logging.getLogger(__name__)
logger.setLevel(logging.STATUS)
setattr(logger, 'status', lambda message,
        *args: logger._log(logging.STATUS, message, args))


def cmp(a, b):
    """
    Definition of Python2 cmp function.
    """
    return bool(a > b) - bool(a < b)  # convert possible numpy-bool to bool


# noinspection PyUnresolvedReferences
class CustomXepr(QtCore.QObject):
    """
    CustomXepr defines routines such as tuning and setting the temperature,
    applying voltages and recording IV characteristics with attached Keithley
    SMUs.

    All CustomXepr methods are executed in a worker thread in the order of
    their calls. To execute your own function in this thread, you can use
    the `queued_exec` decorator provided by customxepr and query the
    `abort_event` to support CustomXepr's abort functionality:

    >>> import customxepr
    >>> from customxepr import queued_exec
    >>> customXepr = customxepr.run()
    >>> @queued_exec(customXepr.job_queue) ...
    ... def test_func(*args):
    ...     # do something
    ...     for i in range(0, 10):
    ...         time.sleep(1)
    ...         if customXepr.abort_event.is_set()
    ...             break
    ...     return args

    All results are added to the result queue and can be retrieved with:

    >>> result = customxepr.result_queue.get()

    To pause or resume the worker between jobs, run

    >>> customxepr.running.clear()

    or

    >>> customxepr.running.set()

    CustomXepr functions:
        customxepr.clear_all_jobs()
        customxepr.sendEmail(text)
        customxepr.pause(seconds)

    CustomXepr properties:
        customxepr.notify_address = 'ss2151@cam.ac.uk'
        customxepr.log_file_dir = '~/.CustomXepr/LOG_FILES'
        customxepr.email_handler_level = logging.WARNING
        customxepr.temp_wait_time = 120  # in sec
        customxepr.temperature_tolerance = 0.1  # in Kelvin

    ESR methods:
        customxepr.tune()
        customxepr.finetune()
        customxepr.customtune()
        customxepr.getQValueFromXepr(direct=None, T=298)
        customxepr.getQValueCalc(direct=None, T=298)
        customxepr.runXeprExperiment(exp, **kwargs)
        customxepr.saveCurrentData(path, title=None, exp=None)
        customxepr.setStandby()

    MercuryiTC methods:
        customxepr.setTemperature(target_temperature)
        customxepr.setTempRamp(ramp)
        customxepr.heater_target(temperature)

    Keithley methods:
        customxepr.transferMeasurement(path=None, **kwargs)
        customxepr.outputMeasurement(path=None,  **kwargs)
        customxepr.setGateVoltage(Vg)
        customxepr.applyDrainCurrent(smu, curr)

    See output of help(CustomXepr) for full documentation.

    Attributes:
        job_queue: Queue containing all pending jobs.
        result_queue: Queue containing all results returned from jobs.
        running: Event to pause / run job execution.
        abort_event: Event to abort current job.

    """

# =============================================================================
# Set up basic CustomXepr functionality
# =============================================================================

    job_queue = ExperimentQueue()
    result_queue = SignalQueue()
    running = Event()
    abort = Event()

    def __init__(self, xepr=None, mercury_feed=None, keithley=None):

        super(CustomXepr, self).__init__()

        self.emailSender = EmailSender('ss2151@cam.ac.uk', 'localhost')

        # =====================================================================
        # check if connections to Xepr, MercuryiTC and Keithley are present
        # =====================================================================

        self.xepr = xepr
        self.feed = mercury_feed
        self.keithley = keithley

        # hidden Xepr experiment, created when EPR is connected:
        self.hidden = None
        # target temperature, set during first use
        self._temperature_target = None

        self._check_for_xepr()
        self._check_for_mercury()
        self._check_for_keithley()

        # =====================================================================
        # create background thread to process all executions in queue
        # =====================================================================

        self.worker_thread = QtCore.QThread()
        self.worker_thread.setObjectName('CustomXeprWorker')
        self.worker = Worker(self.job_queue, self.result_queue, self.running, self.abort)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.process)
        self.worker_thread.start()
        self.running.set()
        logger.status('IDLE')

        # =====================================================================
        # define / load certain settings for customxepr functions
        # =====================================================================

        # waiting time for Xepr to process commands, prevent memory error
        self.wait = 0.1
        # settling time for cryostat temperature
        self._temp_wait_time = CONF.get('CustomXepr', 'temp_wait_time')
        # temperature stability tolerance
        self._temperature_tolerance = CONF.get('CustomXepr',
                                               'temperature_tolerance')

# =============================================================================
# define basic functions for email notifications, pausing, etc.
# =============================================================================

    def clear_all_jobs(self):
        """ Clears all pending jobs in job_queue."""
        for item in range(0, self.job_queue.qsize()):
            self.job_queue.get()

    @queued_exec(job_queue)
    def sendEmail(self, body):
        """
        Sends a text to the default email address.
        """
        self.emailSender.sendmail(self.notify_address,
                                  'CustomXepr Notification', body)

    @queued_exec(job_queue)
    def pause(self, seconds):
        """
        Pauses for the specified amount of seconds. This pause function checks
        for an abort signal every minute to prevent permanent blocking.
        """
        eta = time.time() + seconds
        eta_string = time.strftime('%H:%M', time.localtime(eta))
        message = 'Waiting for %s seconds, ETA: %s.'
        logger.info(message % (int(seconds), eta_string))

        # brake up into 1 sec sleep intervals, give option to abort
        if seconds > 1:
            for i in range(0, seconds):
                time.sleep(1)
                logger.status('Waiting %s/%s' % (i+1, seconds))
                # check for abort event
                if self.abort.is_set():
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
    def temp_wait_time(self, new_time):
        """Setter: Wait time until temperature is considered stable."""
        self._temp_wait_time = new_time
        # update config file
        CONF.set('CustomXepr', 'temp_wait_time', new_time)

    @property
    def temperature_tolerance(self):
        """Temperature fluctuation tolerance."""
        return self._temperature_tolerance

    @temperature_tolerance.setter
    def temperature_tolerance(self, new_tol):
        """Setter: Temperature fluctuation tolerance."""
        self._temperature_tolerance = new_tol
        # update config file
        CONF.set('CustomXepr', 'temperature_tolerance', new_tol)

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
        """Setter: Address list for email notifications."""
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
            file_name = fh[0].baseFilename
            return os.path.dirname(file_name)

    @property
    def email_handler_level(self):
        """Logging level for email notifications."""
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
        """Setter: Logging level for email notifications."""
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
    def tune(self):
        """
        Runs Xepr's built-in tuning routine.
        """

        if not self._check_for_xepr():
            return

        self.XeprCmds.aqParSet('AcqHidden', '*cwBridge.OpMode', 'Tune')
        self.XeprCmds.aqParSet('AcqHidden', '*cwBridge.Tune', 'Up')

    @queued_exec(job_queue)
    def finetune(self):
        """
        Runs Xepr's built-in fine-tuning routine.
        """

        if not self._check_for_xepr():
            return

        self.XeprCmds.aqParSet('AcqHidden', '*cwBridge.Tune', 'Fine')

    @queued_exec(job_queue)
    def customtune(self):
        """
        Custom tuning routine with better accuracy. It takes longer than tune()
        and requires the spectrometer to be be already close to tuned.
        """

        if not self._check_for_xepr():
            return

        logger.info('Tuning')

        # save current operation mode and attenuation
        mode = self.hidden['OpMode'].value
        time.sleep(self.wait)
        atten_start = self.hidden['PowerAtten'].value
        time.sleep(self.wait)

        # switch mode to 'Operate'
        if not mode == 'Operate':
            self.hidden['OpMode'].value = 'Operate'
            time.sleep(self.wait)

        # tune frequency at 30 dB
        self.hidden['PowerAtten'].value = 30
        time.sleep(self.wait)
        self._tuneFreq()
        time.sleep(self.wait)

        # tune bias of reference arm at 50 dB
        # (where diode current is determined by reference arm)
        self.hidden['PowerAtten'].value = 50
        time.sleep(self.wait)
        self._tuneBias()
        time.sleep(self.wait)

        # tune iris at 40 dB and 30 dB
        for atten in [40, 30]:
            # check for abort event
            if self.abort.is_set():
                self.hidden['PowerAtten'].value = atten_start
                time.sleep(self.wait)
                logger.info('Aborted by user.')
                return

            self.hidden['PowerAtten'].value = atten
            time.sleep(self.wait)

            self._tuneIris()
            time.sleep(self.wait)

        # tune iris and phase and frequency at 20 dB and 10 dB
        for atten in [20, 10]:
            # check for abort event, clear event
            if self.abort.is_set():
                self.hidden['PowerAtten'].value = atten_start
                time.sleep(self.wait)
                logger.info('Aborted by user.')
                return

            self.hidden['PowerAtten'].value = atten
            time.sleep(self.wait)
            self._tunePhase()
            time.sleep(self.wait)
            self._tuneIris()
            time.sleep(self.wait)
            self._tuneFreq()
            time.sleep(self.wait)

        # tune bias at 50 dB
        self.hidden['PowerAtten'].value = 50
        time.sleep(self.wait)
        self._tuneBias()
        time.sleep(self.wait)

        # tune iris at 15 dB
        self.hidden['PowerAtten'].value = 20
        time.sleep(self.wait)
        self._tuneIris()
        time.sleep(self.wait)

        # tune bias at 50 dB
        self.hidden['PowerAtten'].value = 50
        time.sleep(self.wait)
        self._tuneBias()
        time.sleep(self.wait)

        # tune iris at 10 dB
        self.hidden['PowerAtten'].value = 10
        time.sleep(self.wait)
        self._tuneIris()
        time.sleep(self.wait)

        # reset attenuation to original value, tune frequency again
        self.hidden['PowerAtten'].value = atten_start
        time.sleep(self.wait)
        self._tuneFreq()
        time.sleep(self.wait)

        logger.status('Tuning done.')

    def _tuneBias(self):
        """
        Tunes the diode bias. A perfectly tuned bias results in a diode
        current of 200 mA for all microwave powers.
        """

        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Bias)')
        time.sleep(self.wait)

        # get offset from 200 mA
        diff = self.hidden['DiodeCurrent'].value - 200
        time.sleep(self.wait)
        tolerance1 = 10  # tolerance for fast tuning
        tolerance2 = 1  # tolerance for second fine tuning

        # rapid tuning with high tolerance and large steps
        while abs(diff) > tolerance1:
            # check for abort event
            if self.abort.is_set():
                return

            step = 1*cmp(0, diff)  # coarse step of 1
            self.XeprCmds.aqParStep('AcqHidden', '*cwBridge.SignalBias',
                                    'Coarse %s' % step)
            time.sleep(0.5)
            diff = self.hidden['DiodeCurrent'].value - 200
            time.sleep(self.wait)

        # fine tuning with low tolerance and small steps
        while abs(diff) > tolerance2:
            # check for abort event
            if self.abort.is_set():
                return

            step = 5*cmp(0, diff)  # fine step of 5
            self.XeprCmds.aqParStep('AcqHidden', '*cwBridge.SignalBias',
                                    'Fine %s' % step)
            time.sleep(0.5)
            diff = self.hidden['DiodeCurrent'].value - 200
            time.sleep(self.wait)

    def _tuneIris(self, tolerance=1):
        """
        Tunes the cavity's iris. A perfectly tuned iris results in a diode
        current of 200 mA for all microwave powers.

        Args:
            tolerance (int): Minimum diode current offset that must be achieved
                before `_tuneIris` returns.
        """
        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Iris)')
        time.sleep(self.wait)

        diff = self.hidden['DiodeCurrent'].value - 200

        while abs(diff) > tolerance:
            # check for abort event
            if self.abort.is_set():
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
            time.sleep(self.wait)

    def _tuneFreq(self, tolerance=3):
        """
        Tunes the microwave frequency to a lock offset of zero.

        Args:
            tolerance (int): Minimum frequency offset that must be achieved
                before `_tuneFreq` returns.
        """
        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Freq)')
        time.sleep(self.wait)

        fq_offset = self.hidden['LockOffset'].value
        time.sleep(self.wait)

        while abs(fq_offset) > tolerance:
            # check for abort event
            if self.abort.is_set():
                return

            step = 1 * cmp(0, fq_offset) * max(abs(int(fq_offset/10)), 1)
            self.XeprCmds.aqParStep('AcqHidden', '*cwBridge.Frequency',
                                    'Fine %s' % step)
            time.sleep(1)
            fq_offset = self.hidden['LockOffset'].value
            time.sleep(self.wait)

    def _tunePhase(self):
        """
        Tunes the phase of the MW reference arm to maximise the diode current.
        """
        # timeout for phase tuning
        self._tuning_timeout = 60
        # check for abort event
        if self.abort.is_set():
                return

        logger.status('Tuning (Phase)')
        time.sleep(self.wait)

        t0 = time.time()

        # get current phase and range
        phase0 = self.hidden['SignalPhase'].value
        time.sleep(self.wait)
        phase_min = self.hidden['SignalPhase'].aqGetParMinValue()
        time.sleep(self.wait)
        phase_max = self.hidden['SignalPhase'].aqGetParMaxValue()
        time.sleep(self.wait)
        phase_step = self.hidden['SignalPhase'].aqGetParCoarseSteps()
        time.sleep(self.wait)

        # determine direction of increasing diode current
        diode_curr_array = np.array([])
        interval_min = max(phase0-2*phase_step, phase_min)
        interval_max = min(phase0+2*phase_step, phase_max)
        phase_array = np.arange(interval_min, interval_max, phase_step)

        for phase in phase_array:
            # check for abort event
            if self.abort.is_set():
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
            if self.abort.is_set():
                return
            # check for limits of diode range, readjust iris if necessary
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
    def getQValueFromXepr(self, direct=None, temperature=298):
        """Gets Q-Value determined by Xepr

        Reads out the resonator Q-value, averaged over 20 sec, and saves it
        in the specified file.

        Args:
            direct (str): Directory where Q-Value reading is saved with
                corresponding temperature and time-stamp.
            temperature (float): Temperature in Kelvin during Q-Value measurement.

        Returns:
            Measured Q-Value.
        """

        if not self._check_for_xepr():
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

        q_values = np.array([])

        time.sleep(1)

        for iteration in range(0, 40):
            q_values = np.append(q_values, self.hidden['QValue'].value)
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
        q_mean = q_values.mean()
        q_stderr = q_values.std()

        if direct is not None:
            path = os.path.join(direct, 'QValues.txt')
            self._saveQValue2File(temperature, q_mean, q_stderr, path)

        if q_mean > 3000:
            logger.info('Q = %i±%i.' % (q_mean, q_stderr))
        elif q_mean <= 3000:
            logger.warning('Q = %i±%i is very small. ' % (q_mean, q_stderr) +
                           'Please check on experiment.')

        self.wait = wait_old

        return q_mean

    @queued_exec(job_queue)
    def getQValueCalc(self, direct=None, temperature=None):
        """Calculates Q-Value from cavity mode pictures

        Calculated Q-Value by fitting the cavity mode picture to a Lorentzian
        dip.

        Args:
            direct (str): Directory where Q-Value reading is saved with
                corresponding temperature and time-stamp.
            temperature (float): Temperature in Kelvin during a Q-value
                 measurement. Tries to get temperature reading from MercuryiTC
                 if not given.

        Returns:
            ModePicture instance.
        """

        if not self._check_for_xepr():
            return

        # get temperature from MercuryiTC if connected, else use T = 298K
        if not temperature:
            if self._check_for_mercury():
                temperature = self.feed.readings['Temp']
            else:
                temperature = 298

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
        mode_pic_data = {}

        for mode_zoom in [1, 2, 4, 8]:
            y_data = np.array([])

            self.hidden['ModeZoom'].value = mode_zoom
            time.sleep(2)

            n_points = int(self.hidden['DataRange'][1])
            time.sleep(self.wait)

            for i in range(0, n_points):
                y_data = np.append(y_data, self.hidden['Data'][i])

            mode_pic_data[mode_zoom] = y_data

        mp = ModePicture(mode_pic_data, freq)

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

        if mp.qvalue > 3000:
            logger.info('Q = %i±%i.' % (mp.qvalue, mp.qvalue_stderr))
        elif mp.qvalue <= 3000:
            logger.warning('Q = %i±%i is very small. ' % (mp.qvalue, mp.qvalue_stderr) +
                           'Please check on experiment.')

        if direct is None:
            pass
        elif os.path.isdir(direct):
            path = os.path.join(direct, 'QValues.txt')
            self._saveQValue2File(temperature, mp.qvalue, mp.qvalue_stderr, path)
            path = os.path.join(direct, 'ModePicture{0:03d}K.txt'.format(temperature))
            mp.save(path)

        self.wait = wait_old

        return mp

    @staticmethod
    def _saveQValue2File(temperature, qvalue, qvalue_stderr, path):

        time_str = time.strftime('%Y-%m-%d %H:%M')
        string = '%s\t%d\t%s\t%s\n' % (time_str, temperature, qvalue, qvalue_stderr)

        if os.path.isfile(path):
            with open(path, 'a') as f:
                f.write(string)
        else:
            header = 'Time stamp\tTemperature [K]\tQValue\tStandard error\n'
            with open(path, 'a') as f:
                f.write(header)
                f.write(string)

    @queued_exec(job_queue)
    def runXeprExperiment(self, exp, **kwargs):
        """Runs an Xepr experiment

        Runs the Xepr experiment given by "exp". Keyword arguments (kwargs)
        allow the user to pass experiment parameters. If multiple scans are
        performed, the frequency is tuned between scans.

        If connected to a temperature controller, the temperature during the
        measurements is monitored.

        Args:
            exp: Xepr experiment instance.
            **kwargs: Keyword arguments corresponding to measurement
                parameters.

        Returns:
            Xepr data set object.
        """

        if not self._check_for_xepr():
            return

        # -----------set experiment parameters if given in kwargs--------------
        for key in kwargs:
            exp[key].value = kwargs[key]
            time.sleep(self.wait)

        message = ('Measurement "%s" is running. ' % exp.aqGetExpName())

        logger.info(message)

        # -------------------start experiment----------------------------------

        if self.feed is not None and self.feed.mercury is not None:
            temperature_history = np.array([])
        else:
            temperature_history = None

        exp.select()
        time.sleep(self.wait)
        exp.aqExpRun()
        time.sleep(self.wait)

        # wait for experiment to start
        while not exp.isRunning:
            time.sleep(self.wait)

        time.sleep(1)
        exp.aqExpPause()
        time.sleep(self.wait)

        # count the number of temperature stability violations
        n_out = 0  # start at n_out = 0

        while exp.isRunning or exp.isPaused:

            # check for abort event
            if self.abort.is_set():
                exp.aqExpPause()
                logger.info('Aborted by user.')
                return

            nb_scans_done = exp['NbScansDone'].value
            time.sleep(self.wait)
            nb_scans_to_do = exp['NbScansToDo'].value
            time.sleep(self.wait)
            logger.status('Recording scan %i of %i'
                          % (nb_scans_done + 1, nb_scans_to_do))

            # tune frequency and iris when a new slice scan starts
            if exp.isPaused and not nb_scans_done == nb_scans_to_do:
                logger.status('Checking tuned.')

                self._tuneFreq(tolerance=3)
                time.sleep(1)
                self._tuneFreq(tolerance=3)
                time.sleep(self.wait)

                self._tuneIris(tolerance=7)
                time.sleep(self.wait)
                exp.aqExpRun()
                time.sleep(self.wait)

                while not exp.isRunning:
                    time.sleep(self.wait)

                time.sleep(1)
                exp.aqExpPause()
                time.sleep(self.wait)

            # record temperature and warn if fluctuations exceed the tolerance
            if temperature_history:
                temperature_curr = self.feed.readings['Temp']
                temperature_history = np.append(temperature_history, temperature_curr)
                # increment the number of violations n_out if temperature unstable
                n_out += (abs(temperature_history[-1] - temperature_history[0]) >
                          2 * self.temperature_tolerance)
                # warn once for every 120 violations
                if np.mod(n_out, 120) == 1:
                    logger.warning(u'Temperature fluctuations > ±%sK.'
                                   % (2*self.temperature_tolerance))
                    n_out += 1  # prevent from warning again next second

                # Pause measurement and suspend all pending jobs after 15 min
                # of temperature instability
                if n_out > 60 * 15:
                    logger.error('Temperature could not be stabilized for ' +
                                 '15 min. Pausing current measurement and ' +
                                 'all pending jobs.')
                    exp.aqExpPause()
                    self.running.clear()
                    return

            time.sleep(1)

        # get temperature stability over scan if mercury was connected
        if temperature_history:
            temperature_var = max(temperature_history) - min(temperature_history)
            temperature_mean = float(np.mean(temperature_history))
            logger.info(u'Temperature stable at (%.2f±%.2f)K during scans.'
                        % (temperature_mean, temperature_var / 2))

        logger.info('All scans complete.')

        # -----------------get acquired data set from Xepr and return----------
        # switch viewpoint to experiment which just finished running
        exp_title = exp.aqGetExpName()
        time.sleep(self.wait)
        self.XeprCmds.aqExpSelect(1, exp_title)
        time.sleep(self.wait)

        # get data set
        dset = self.xepr.XeprDataset()
        time.sleep(self.wait)

        return dset

    @queued_exec(job_queue)
    def saveCurrentData(self, path, title=None, exp=None):
        """
        Saves the data from given experiment in Xepr to the specified path. If
        exp == None the currently displayed data set is saved.

        Xepr only allows file paths shorter than 128 characters.
        """

        if not self._check_for_xepr():
            return

        directory, filename = os.path.split(path)

        # check if path is valid
        if not os.path.isdir(directory):
            logger.error('The directory "%s" does not exist.' % directory)
            self.running.clear()
            return

        # check if path is valid
        if len(path) > 128:
            logger.error('Invalid path. Full path must be shorter than 110 ' +
                         'characters.')
            self.running.clear()
            return

        # switch viewpoint to experiment if given
        if exp is not None:
            exp_title = exp.aqGetExpName()
            time.sleep(self.wait)
            self.XeprCmds.aqExpSelect(1, exp_title)
            time.sleep(self.wait)

        # title = filename if no title given
        if title is None:
            title = filename

        # save data
        self.XeprCmds.ddPath(path)
        time.sleep(self.wait)
        self.XeprCmds.vpSave('Current Primary', title,  path)
        time.sleep(self.wait)
        logger.info('Data saved to %s.' % path)

    @queued_exec(job_queue)
    def setStandby(self):
        """
        Sets the magnetic field to zero and the MW bridge to standby.
        """

        if not self._check_for_xepr():
            return

        # check if WindDown experiment already exists, otherwise create
        try:
            wd = self.xepr.XeprExperiment('WindDown')
            time.sleep(self.wait)
        except ExperimentError:
            wd = self.xepr.XeprExperiment('WindDown', exptype='C.W.',
                                          axs1='Field', ordaxs='Signal channel')
        time.sleep(self.wait)

        wd.aqExpActivate()
        time.sleep(self.wait)
        wd['CenterField'].value = 0
        time.sleep(self.wait)
        wd['AtCenter'].value = True
        time.sleep(self.wait)

        self.hidden['OpMode'].value = 'Tune'
        time.sleep(3)
        self.hidden['OpMode'].value = 'Stand By'
        time.sleep(self.wait)

        logger.info('EPR set to standby.')

# =============================================================================
# set up cryostat functions
# =============================================================================

    @queued_exec(job_queue)
    def setTemperature(self, temperature_target):
        """
        Sets the target temperature for the ESR900 cryostat and waits for it to
        stabilize within `self.temp_wait_time` with fluctuations below
        `self.temperature_tolerance`.

        Warns the user if this takes too long.
        """

        if not self._check_for_mercury():
            return

        # create instance variable here to allow outside access
        self._temperature_target = temperature_target
        logger.info('Setting target temperature to %sK.' % self._temperature_target)

        # set temperature and wait to stabilize
        self.feed.control.t_setpoint = self._temperature_target
        self._waitStable()

        # check if gas flow is too high for temperature set point
        # if yes, reduce minimum value until target is reached
        ht = self.heater_target(self._temperature_target)
        fmin = self.feed.readings['FlowMin']

        heater_too_strong = (self.feed.readings['HeaterVolt'] > 1.2*ht)
        flow_at_min = (self.feed.readings['FlowPercent'] == fmin)

        if heater_too_strong and flow_at_min:

            logger.warning('Gas flow is too high, trying to reduce.')
            self.feed.control.flow_auto = 'ON'
            self.feed.gasflow.gmin = max(self.feed.readings['FlowMin'] - 1, 1)

    def _waitStable(self):
        """
        Waits for the cryostat temperature to stabilize within the specified
        tolerance `self.temperature_tolerance`. Releases after it has been
        stable for `self.temp_wait_time` seconds (default of 120 sec).
        """

        # time in sec after which a timeout warning is issued
        self._temperature_timeout = (self._ramp_time() + 30*60)  # in sec
        # counter for elapsed seconds since temperature has been stable
        stable_counter = 0
        # counter for setting gas flow to manual
        gasflow_man_counter = 0
        # starting time
        t0 = time.time()

        logger.info('Waiting for temperature to stabilize.')

        while stable_counter < self.temp_wait_time:
            # check for abort command
            if self.abort.is_set():
                logger.info('Aborted by user.')
                return

            # set gas flow to minimum for temperatures above 247K, this improves
            # the PID control and speeds up stabilization
            if gasflow_man_counter == 0:
                if self.feed.readings['Temp'] > 247 and self._temperature_target > 247:
                    self.feed.control.flow_auto = 'OFF'
                    self.feed.control.flow = self.feed.readings['FlowMin']
                else:
                    self.feed.control.flow_auto = 'ON'
                gasflow_man_counter += 1

            # check temperature deviation
            self.T_diff = abs(self._temperature_target - self.feed.readings['Temp'])
            if self.T_diff > self.temperature_tolerance:
                stable_counter = 0
                time.sleep(self.feed.refresh)
                logger.status('Waiting for temperature to stabilize.')
            else:
                stable_counter += self.feed.refresh
                logger.status('Stable for %s/%s sec.' % (stable_counter,
                                                         self.temp_wait_time))
                time.sleep(self.feed.refresh)

            # warn once if stabilization is taking longer than expected
            if time.time() - t0 > self._temperature_timeout:
                t0 = time.time()
                logger.warning('Temperature is taking too long to stabilize.')

        message = 'Mercury iTC: Temperature is stable at %sK.' % self._temperature_target
        logger.info(message)

    @staticmethod
    def heater_target(temperature):
        """Calculates the ideal heater voltage for a given temperature."""
        return 4.5 * np.log(temperature) - 5.5

    def _ramp_time(self):
        """
        Calculates the expected time in sec to reach the target temperature.
        Assumes a max ramping speed of 5 K/min if "ramp" is turned off.
        """
        if self.feed.readings['TempRampEnable'] == 'ON':
            expected_time = (abs(self._temperature_target - self.feed.readings['Temp']) /
                             self.feed.readings['TempRamp'])  # in min
        else:  # assume ramp of 5 K/min
            expected_time = (abs(self._temperature_target - self.feed.readings['Temp']) / 5)
        return expected_time * 60  # return value in sec

    @queued_exec(job_queue)
    def setTempRamp(self, ramp):
        """Sets the temperature ramp for the ESR900 cryostat in K/min."""

        if not self._check_for_mercury():
            return

        # set temperature and wait to stabilize
        self.feed.control.ramp = ramp
        logger.info('Setting temperature ramp to %s K/min.' % ramp)

# =============================================================================
# set up Keithley functions
# =============================================================================

    @queued_exec(job_queue)
    def transferMeasurement(self, smu_gate=K_CONF.get('Sweep', 'gate'),
                            smu_drain=K_CONF.get('Sweep', 'drain'),
                            vg_start=K_CONF.get('Sweep', 'VgStart'),
                            vg_stop=K_CONF.get('Sweep', 'VgStop'),
                            vg_step=K_CONF.get('Sweep', 'VgStep'),
                            vd_list=K_CONF.get('Sweep', 'VdList'),
                            t_int=K_CONF.get('Sweep', 'tInt'),
                            delay=K_CONF.get('Sweep', 'delay'),
                            pulsed=K_CONF.get('Sweep', 'pulsed'),
                            path=None):
        """
        Records a transfer curve and saves the results in a TransistorSweepData
        instance.

        Args:
            smu_gate: SMU attached to gate electrode of FET for transfer
                measurement (keithley smu object).
            smu_drain: SMU attached to drain electrode of FET for transfer
                measurement (keithley smu object).
            vg_start (float): Start voltage of transfer sweep in Volts .
            vg_stop (float): End voltage of transfer sweep in Volts.
            vg_step (float): Voltage step size for transfer sweep in Volts.
            vd_list (list): List of drain voltage steps in Volts.
            t_int (float): Integration time in sec for every data point.
            delay (float): Settling time in sec before every measurement. Set
                to -1 for for automatic delay.
            pulsed (bool): True or False for pulsed or continuous measurements.
            path (str): File path to save transfer curve data as .txt file.

        Returns:
            Returns a TransistorSweepData object containing sweep data.
        """

        if not self._check_for_keithley():
            return

        smu_gate = getattr(self.keithley, smu_gate)
        smu_drain = getattr(self.keithley, smu_drain)

        sd = self.keithley.transferMeasurement(smu_gate, smu_drain, vg_start,
                                               vg_stop, vg_step, vd_list, t_int,
                                               delay, pulsed)
        if path is not None:
            sd.save(path)

        return sd

    @queued_exec(job_queue)
    def outputMeasurement(self, smu_gate=K_CONF.get('Sweep', 'gate'),
                          smu_drain=K_CONF.get('Sweep', 'drain'),
                          vd_start=K_CONF.get('Sweep', 'VdStart'),
                          vd_stop=K_CONF.get('Sweep', 'VdStop'),
                          vd_step=K_CONF.get('Sweep', 'VdStep'),
                          vg_list=K_CONF.get('Sweep', 'VgList'),
                          t_int=K_CONF.get('Sweep', 'tInt'),
                          delay=K_CONF.get('Sweep', 'delay'),
                          pulsed=K_CONF.get('Sweep', 'pulsed'),
                          path=None):
        """
        Records an output curve and saves the results in a TransistorSweepData
        instance.

        Args:
            smu_gate: SMU attached to gate electrode of FET for transfer
                measurement (keithley smu object).
            smu_drain: SMU attached to drain electrode of FET for transfer
                measurement (keithley smu object).
            vd_start (float): Start voltage of output sweep in Volts .
            vd_stop (float): End voltage of output sweep in Volts.
            vd_step (float): Voltage step size for output sweep in Volts.
            vg_list (list): List of gate voltage steps in Volts.
            t_int (float): Integration time in sec for every data point.
            delay (float): Settling time in sec before every measurement. Set
                to -1 for for automatic delay.
            pulsed (bool): True or False for pulsed or continuous measurements.
            path (str): File path to save output curve data as .txt file.

        Returns:
            Returns a TransistorSweepData object containing sweep data.
        """

        if not self._check_for_keithley():
            return

        smu_gate = getattr(self.keithley, smu_gate)
        smu_drain = getattr(self.keithley, smu_drain)

        sd = self.keithley.outputMeasurement(smu_gate, smu_drain, vd_start,
                                             vd_stop, vd_step, vg_list, t_int,
                                             delay, pulsed)
        if path is not None:
            sd.save(path)

        return sd

    @queued_exec(job_queue)
    def setGateVoltage(self, vg, smu_gate=K_CONF.get('Sweep', 'gate')):
        """Sets the gate bias of the given keithley, grounds other SMUs."""

        if not self._check_for_keithley():
            return

        gate = getattr(self.keithley, smu_gate)

        # turn off all remaining SMUs
        other_smus = filter(lambda a: a != smu_gate, self.keithley.SMU_LIST)
        for smu_name in other_smus:
            smu = getattr(self.keithley, smu_name)
            smu.source.output = self.keithley.OUTPUT_OFF

        self.keithley.rampToVoltage(gate, targetVolt=vg, delay=0.1, stepSize=1)

        if vg == 0:
            self.keithley.reset()

    @queued_exec(job_queue)
    def applyDrainCurrent(self, i, smu=K_CONF.get('Sweep', 'drain')):
        """Applies a specified current to the selected Keithley SMU."""

        if not self._check_for_keithley():
            return

        smu = getattr(self.keithley, smu)

        self.keithley.applyCurrent(smu, i)
        self.keithley.beep(0.3, 2400)

# =============================================================================
# Helper methods
# =============================================================================

    def _check_for_mercury(self):
        """
        Checks if a mercury instance has been passed and is connected to an
        an actual instrument.
        """
        if not self.feed or not self.feed.mercury:
            logger.info('No Mercury instance supplied. Functions that ' +
                        'require a connected cryostat will not work.')
            return False
        elif not self.feed.mercury.connected:
            logger.info('MercuryiTC is not connected. Functions that ' +
                        'require a connected cryostat will not work.')
            return False
        else:
            return True

    def _check_for_keithley(self):
        """
        Checks if a keithley instance has been passed and is connected to an
        an actual instrument.
        """

        if not self.keithley:
            logger.info('No Keithley instance supplied. Functions that ' +
                        'require a connected Keithley SMU will not work.')
            return False
        elif not self.keithley.connected:
            logger.info('Keithley is not connected. Functions that ' +
                        'require a connected Keithley will not work.')
            return False
        else:
            return True

    def _check_for_xepr(self):
        if not self.xepr:
            logger.info('No Xepr instance supplied. Functions that ' +
                        'require Xepr will not work.')
            return False
        elif not self.xepr.XeprActive():
            logger.info('Xepr API not active. Please activate Xepr API by ' +
                        'pressing "Processing > XeprAPI > Enable Xepr API"')
            return False

        self.XeprCmds = self.xepr.XeprCmds

        if not self.hidden:
            try:
                self.hidden = self.xepr.XeprExperiment('AcqHidden')
                return True
            except ExperimentError:
                logger.info('Xepr is not connected to the spectrometer.' +
                            'Please connect by pressing "Acquisition > ' +
                            'Connect To Spectrometer..."')
                return False
        else:
            return True


# =============================================================================
# Set up loggers to send emails and write to log files
# =============================================================================

def setup_root_logger(to_address):

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
                                       to_address, 'Xepr logger')
        email_handler.setFormatter(f)
        email_handler.setLevel(CONF.get('CustomXepr', 'email_handler_level'))

        root_logger.addHandler(email_handler)

    # =========================================================================
    # Set up logging to file
    # =========================================================================
    if len(fh) == 0:
        home_path = os.path.expanduser('~')
        logging_path = os.path.join(home_path, '.CustomXepr', 'LOG_FILES')

        if not os.path.exists(logging_path):
            os.makedirs(logging_path)

        log_file = os.path.join(logging_path, 'root_logger '
                                + time.strftime("%Y-%m-%d_%H-%M-%S"))
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(f)
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)


setup_root_logger(CONF.get('CustomXepr', 'notify_address'))
