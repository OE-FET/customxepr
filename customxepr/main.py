# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import
import sys
import os
import logging
import time
import numpy as np
import tempfile
from qtpy import QtCore
from keithleygui import CONF as K_CONF

from customxepr.utils import EmailSender
from customxepr.experiment import ModePicture, XeprData, XeprParam
from customxepr.experiment.xepr_dataset import ParamGroupDSL
from customxepr.manager import Manager, queued_exec
from customxepr.config import CONF

try:
    sys.path.insert(0, os.popen('Xepr --apipath').read())
    from XeprAPI import ExperimentError
except ImportError:
    ExperimentError = RuntimeError


PY2 = sys.version[0] == '2'

__author__ = 'Sam Schott <ss2151@cam.ac.uk>'
__year__ = str(time.localtime().tm_year)
__version__ = 'v2.3.0'
__url__ = 'https://customxepr.readthedocs.io'


logger = logging.getLogger('customxepr')


def cmp(a, b):
    return bool(a > b) - bool(a < b)  # convert possible numpy-bool to bool


# noinspection PyUnresolvedReferences
class CustomXepr(QtCore.QObject):
    """
    CustomXepr defines routines to control the Bruker Xepr software and run
    full ESR measurement cycles. This includes tuning and setting the temperature,
    applying voltages and recording IV characteristics with attached Keithley
    SMUs.

    All CustomXepr methods are executed in a worker thread in the order of
    their calls. To execute your own function in this thread, you can use
    the :func:`queued_exec` decorator provided by customxepr and query the
    :attr:`abort_event` to support CustomXepr's abort functionality (see
    :class:`manager.Manager`).

    All results are added to the result queue and can be retrieved with:

    >>> manager = customxepr.manager
    >>> result = manager.result_queue.get()  # blocks until result is available

    To pause or resume the worker between jobs, run

    >>> manager.pause_worker()

    or

    >>> manager.resume_worker()

    To abort a job, run:

    >>> manager.abort_job()

    You can use :class:`CustomXepr` on its own, but it is recommended to start
    it with the :func:`run` function in the :mod:`startup` module. This will
    automatically connect to available instruments and start the graphical user
    interfaces.

    :param xepr: Xepr instance from the Bruker Python XeprAPI. Defaults
        to `None` if not provided.
    :param mercuryfeed: :class:`mercurygui.MercuryFeed` instance for live feed from
        MercuryiTC temperature controller. Defaults to `None` if not provided.
    :param keithley: :class:`keithley2600.Keithley2600` instance from keithley2600
        driver. Defaults to `None` if not provided.

    :cvar manager: Manages execution of queued experiments.

    :ivar hidden: Xepr's hidden experiment.
    :ivar xepr: Connected Xepr instance.
    :ivar keithley: Connected :class:`keithley2600.Keithley2600` instance.
    :ivar feed: Connected :class:`mercurygui.MercuryFeed` instance.
    :ivar wait: Delay between commands sent to Xepr.
    """

    manager = Manager()

# ========================================================================================
# Set up basic CustomXepr functionality
# ========================================================================================

    def __init__(self, xepr=None, mercuryfeed=None, keithley=None):

        super(self.__class__, self).__init__()
        self.emailSender = EmailSender('ss2151@cam.ac.uk', 'localhost',
                                       displayname='Sam Schott')

        # =====================================================================
        # check if connections to Xepr, MercuryiTC and Keithley are present
        # =====================================================================

        self.xepr = xepr
        self.feed = mercuryfeed
        self.keithley = keithley

        # hidden Xepr experiment, created when EPR is connected:
        self.hidden = None
        # target temperature, set during first use
        self._temperature_target = None

        self._check_for_xepr()
        self._check_for_mercury()
        self._check_for_keithley()

        # =====================================================================
        # define / load certain settings for customxepr functions
        # =====================================================================

        # waiting time for Xepr to process commands, prevent memory error
        self.wait = 0.1
        # timeout for phase tuning
        self._tuning_timeout = 60
        # last measured Q-value
        self._last_qvalue = None
        # settling time for cryostat temperature
        self._temp_wait_time = CONF.get('CustomXepr', 'temp_wait_time')
        # temperature stability tolerance
        self._temperature_tolerance = CONF.get('CustomXepr',
                                               'temperature_tolerance')

        # =====================================================================
        # interaction with manager
        # =====================================================================
        self.abort = self.manager.abort

        if keithley is not None:
            self.manager.abort_events = [self.keithley.abort_event]

# ========================================================================================
# define basic functions for email notifications, pausing, etc.
# ========================================================================================

    @queued_exec(manager.job_queue)
    def sendEmail(self, body):
        """
        Sends a text to the default email address.

        :param str body: Text to send.
        """
        self.emailSender.sendmail(self.manager.notify_address,
                                  'CustomXepr Notification', body)

    @queued_exec(manager.job_queue)
    def sleep(self, seconds):
        """
        Pauses for the specified amount of seconds. This sleep function checks
        for an abort signal every minute to prevent permanent blocking.

        :param int seconds: Number of seconds to pause.
        """
        eta = time.time() + seconds
        eta_string = time.strftime('%H:%M', time.localtime(eta))
        message = 'Waiting for %s seconds, ETA: %s.'
        logger.info(message % (int(seconds), eta_string))

        # brake up into 1 sec sleep intervals, give option to abort
        if seconds > 1:
            for i in range(0, seconds):
                time.sleep(1)
                logger.status('Waiting %s/%s.' % (i+1, seconds))
                # check for abort event
                if self.abort.is_set():
                    logger.info('Aborted by user.')
                    return
        # use a single sleep command for less than one second pause
        else:
            time.sleep(seconds)

    @property
    def temp_wait_time(self):
        """Wait time until temperature is considered stable. Defaults to 120 sec."""
        return self._temp_wait_time

    @temp_wait_time.setter
    def temp_wait_time(self, new_time):
        """Setter: Wait time until temperature is considered stable."""
        self._temp_wait_time = new_time
        # update config file
        CONF.set('CustomXepr', 'temp_wait_time', new_time)

    @property
    def temperature_tolerance(self):
        """Temperature fluctuation tolerance. Defaults to 0.1 Kelvin."""
        return self._temperature_tolerance

    @temperature_tolerance.setter
    def temperature_tolerance(self, new_tol):
        """Setter: Temperature fluctuation tolerance."""
        self._temperature_tolerance = new_tol
        # update config file
        CONF.set('CustomXepr', 'temperature_tolerance', new_tol)

# ========================================================================================
# set up Xepr functions
# ========================================================================================

    @queued_exec(manager.job_queue)
    def tune(self):
        """
        Runs Xepr's built-in tuning routine.
        """

        if not self._check_for_xepr():
            raise RuntimeError('Not connected to Xepr.')

        self.XeprCmds.aqParSet('AcqHidden', '*cwBridge.OpMode', 'Tune')
        self.XeprCmds.aqParSet('AcqHidden', '*cwBridge.Tune', 'Up')

    @queued_exec(manager.job_queue)
    def finetune(self):
        """
        Runs Xepr's built-in finetuning routine.
        """

        if not self._check_for_xepr():
            raise RuntimeError('Not connected to Xepr.')

        self.XeprCmds.aqParSet('AcqHidden', '*cwBridge.Tune', 'Fine')

    @queued_exec(manager.job_queue)
    def customtune(self, low_q=False):
        """
        Custom tuning routine with higher accuracy. It takes longer than :meth:`tune`
        and requires the spectrometer to be already close to tuned. In case of Q-values
        < 4500, you can set :param:`lowQ` to `True` so that the tuning routine will cycle
        through a smaller range of microwave powers. If Q < 3000, it is recommended to
        tune the spectrometer manually.

        :param bool low_q: If True, the tuning routine will be adjusted for low Q-value
            conditions. This is recommended for 3000 < Q < 5000.
        """

        if not self._check_for_xepr():
            raise RuntimeError('Not connected to Xepr.')

        logger.info('Tuning.')

        # save current operation mode and attenuation
        mode = self.hidden['OpMode'].value
        time.sleep(self.wait)
        atten_start = self.hidden['PowerAtten'].value
        time.sleep(self.wait)

        # switch mode to 'Operate'
        if not mode == 'Operate':
            self.hidden['OpMode'].value = 'Operate'
            time.sleep(self.wait)

        dB_min = 10 if not low_q else 20
        dB_max = 50 if not low_q else 45

        # tune frequency and phase at 30 dB
        self.hidden['PowerAtten'].value = 30
        time.sleep(self.wait)
        self._tuneFreq()
        time.sleep(self.wait)
        self._tunePhase()
        time.sleep(self.wait)

        # tune bias of reference arm at dB_max
        # (where diode current is determined by reference arm)
        self.hidden['PowerAtten'].value = dB_max
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
        for atten in [20, dB_min]:
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

        # tune bias at dB_max
        self.hidden['PowerAtten'].value = dB_max
        time.sleep(self.wait)
        self._tuneBias()
        time.sleep(self.wait)

        # tune iris at 15 dB
        self.hidden['PowerAtten'].value = 20
        time.sleep(self.wait)
        self._tuneIris()
        time.sleep(self.wait)

        # tune bias at dB_max
        self.hidden['PowerAtten'].value = dB_max
        time.sleep(self.wait)
        self._tuneBias()
        time.sleep(self.wait)

        # tune iris at dB_min
        self.hidden['PowerAtten'].value = dB_min
        time.sleep(self.wait)
        self._tuneIris()
        time.sleep(self.wait)

        # reset attenuation to original value, tune frequency again
        self.hidden['PowerAtten'].value = atten_start
        time.sleep(self.wait)
        self._tuneFreq()
        time.sleep(self.wait)

        logger.status('Tuning done.')

    @queued_exec(manager.job_queue)
    def tuneBias(self):
        """
        Tunes the diode bias. A perfectly tuned bias results in a diode
        current of 200 mA for all microwave powers.
        """

        self._tuneBias()

    @queued_exec(manager.job_queue)
    def tuneIris(self, tolerance=1):
        """
        Tunes the cavity's iris. A perfectly tuned iris results in a diode
        current of 200 mA for all microwave powers.

        :param int tolerance: Minimum diode current offset that must be achieved
            before :meth:`tuneIris` returns.
        """
        self._tuneIris(tolerance)

    @queued_exec(manager.job_queue)
    def tuneFreq(self, tolerance=3):
        """
        Tunes the microwave frequency to a lock offset close to zero.

        :param int tolerance: Minimum lock offset that must be achieved
            before :meth:`tuneFreq` returns.
        """
        self._tuneFreq(tolerance)

    @queued_exec(manager.job_queue)
    def tunePhase(self):
        """
        Tunes the phase of the MW reference arm to maximise the diode current.
        """
        self._tunePhase()

    @queued_exec(manager.job_queue)
    def getQValueFromXepr(self, path=None, temperature=298):
        """
        Gets the Q-Value as determined by Xepr, averaged over 20 readouts, and saves it
        in the specified file.

        :param str path: Directory where Q-Value reading is saved with
            corresponding temperature and time-stamp.
        :param float temperature: Temperature in Kelvin during Q-Value measurement.

        :returns: Measured Q-Value.
        :rtype: float
        """

        if not self._check_for_xepr():
            raise RuntimeError('Not connected to Xepr.')

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

        if path is not None:
            path = os.path.join(path, 'QValues.txt')
            self._saveQValue2File(temperature, q_mean, q_stderr, path)

        if q_mean > 3000:
            logger.info('Q = %i+/-%i.' % (q_mean, q_stderr))
        elif q_mean <= 3000:
            logger.warning('Q = %i+/-%i is very small. ' % (q_mean, q_stderr) +
                           'Please check on experiment.')

        self.wait = wait_old

        return q_mean

    @queued_exec(manager.job_queue)
    def getQValueCalc(self, path=None, temperature=298):
        """
        Calculates the Q-value by fitting the cavity mode picture to a Lorentzian
        resonance with a polynomial baseline. It uses all available zoom factors
        to resolve both sharp and broad resonances (high and low Q-values, respectively)
        and is therefore more accurate than :meth:`getQValueFromXepr`.

        :param str path: Directory where Q-Value reading is saved with
            corresponding temperature and time-stamp.
        :param float temperature: Temperature in Kelvin during a Q-value
            measurement. Defaults to room temperature.

        :returns: Mode picture instance.
        :rtype: :class:`mode_picture.ModePicture`
        """

        if not self._check_for_xepr():
            raise RuntimeError('Not connected to Xepr.')

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
        self._last_qvalue = mp.qvalue

        self.hidden['PowerAtten'].value = 30
        time.sleep(self.wait)
        self.hidden['ModeZoom'].value = 1
        time.sleep(self.wait)
        self.hidden['RefArm'].value = 'On'
        time.sleep(self.wait)
        self.hidden['OpMode'].value = 'Operate'

        time.sleep(2)

        self._tuneFreq()
        self._tuneFreq()
        self._tuneBias()
        self._tuneFreq()

        self.hidden['PowerAtten'].value = att
        time.sleep(self.wait)

        if mp.qvalue > 3000:
            logger.info('Q = %i+/-%i.' % (mp.qvalue, mp.qvalue_stderr))
        elif mp.qvalue <= 3000:
            logger.warning('Q = %i+/-%i is very small. ' % (mp.qvalue, mp.qvalue_stderr) +
                           'Please check on experiment.')

        if path is None:
            pass
        elif os.path.isdir(path):
            path1 = os.path.join(path, 'QValues.txt')
            path2 = os.path.join(path, 'ModePicture{0:03d}K.txt'.format(int(temperature)))

            self._saveQValue2File(temperature, mp.qvalue, mp.qvalue_stderr, path1)
            mp.save(path2)

        self.wait = wait_old

        return mp

    @staticmethod
    def _saveQValue2File(tmpr, qval, qval_stderr, path):

        delim = '\t'
        newline = '\n'

        column_titles = ['Time stamp', 'Temperature [K]', 'QValue', 'Standard error']
        header = delim.join(column_titles + [newline])

        time_str = time.strftime('%Y-%m-%d %H:%M')
        line = delim.join([time_str, str(tmpr), str(qval), str(qval_stderr), newline])

        is_newfile = not os.path.isfile(path)

        with open(path, 'a') as f:
            if is_newfile:
                f.write(header)
            f.write(line)

    @queued_exec(manager.job_queue)
    def runXeprExperiment(self, exp, retune=False, path=None, **kwargs):
        """
        Runs the Xepr experiment ``exp`. Keyword arguments (kwargs)
        allow the user to pass experiment setting to Xepr. If multiple scans
        are performed, frequency and iris can be tuned between scans.

        If connected to a temperature controller, the temperature during the
        measurements is monitored.

        If the ``path`` argument is given, the resulting data set is saved
        to the drive and the last-measured Q-value and the measurement
        temperature (if available) are stored in the Bruker '.DSC' file.

        :param exp: Xepr experiment object.
        :param bool retune: Retune iris and freq between scans (default: False).
        :param str path: Path to file. If given, the data set will be saved to this path,
            otherwise, it will just be kept in memory. Xepr only allows file paths
            shorter than 128 characters.
        :param kwargs: Keyword arguments corresponding to measurement Xepr
            parameters (e.g., modulation amplitude).
        """

        if not self._check_for_xepr():
            raise RuntimeError('Not connected to Xepr.')

        # -----------set experiment parameters if given in kwargs--------------
        for key in kwargs:
            exp[key].value = kwargs[key]
            time.sleep(self.wait)

        message = ('Measurement "%s" is running. ' % exp.aqGetExpName())

        logger.info(message)

        # -------------------start experiment----------------------------------
        temperature_mean = None
        if self._check_for_mercury():
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

        if retune:  # schedule pause after scan to retune
            time.sleep(1)
            exp.aqExpPause()
            time.sleep(self.wait)

        # count the number of temperature stability violations
        n_out = 0  # start at n_out = 0

        def is_running_or_paused():
            running = exp.isRunning
            time.sleep(self.wait)
            paused = exp.isPaused
            time.sleep(self.wait)
            return running or paused

        while is_running_or_paused():

            # check for abort event
            if self.abort.is_set():
                exp.aqExpPause()
                time.sleep(self.wait)
                logger.info('Aborted by user.')
                return

            nb_scans_done = exp['NbScansDone'].value
            time.sleep(self.wait)
            nb_scans_to_do = exp['NbScansToDo'].value
            time.sleep(self.wait)
            logger.status('Recording scan %i/%i.' % (nb_scans_done + 1, nb_scans_to_do))

            if retune:
                # tune frequency and iris when a new slice scan starts
                if exp.isPaused and not nb_scans_done == nb_scans_to_do:
                    logger.status('Checking tuned.')
                    self._tuneFreq(tolerance=3)
                    self._tuneFreq(tolerance=3)
                    self._tuneIris(tolerance=7)

                    # start next scan
                    exp.aqExpRun()
                    time.sleep(self.wait)

                    # wait for scan to start and schedule next pause
                    while not exp.isRunning:
                        time.sleep(1)
                    exp.aqExpPause()
                    time.sleep(self.wait)

            # record temperature and warn if fluctuations exceed the tolerance
            if temperature_history is not None:
                temperature_curr = self.feed.readings['Temp']
                temperature_history = np.append(temperature_history, temperature_curr)
                # increment the number of violations n_out if temperature unstable
                n_out += (abs(temperature_history[-1] - temperature_history[0]) >
                          2 * self.temperature_tolerance)
                # warn once for every 120 violations
                if np.mod(n_out, 120) == 1:
                    logger.warning(u'Temperature fluctuations > +/-%sK.'
                                   % (2*self.temperature_tolerance))
                    n_out += 1  # prevent from warning again next second

                # Pause measurement and suspend all pending jobs after 15 min
                # of temperature instability
                if n_out > 60 * 15:
                    logger.warning('Temperature could not be stabilized for ' +
                                   '15 min. Pausing current measurement and ' +
                                   'all pending jobs.')
                    exp.aqExpPause()
                    self.manager.running.clear()
                    return

            time.sleep(1)

        # get temperature stability during scan if mercury was connected
        if temperature_history is not None:
            temperature_var = max(temperature_history) - min(temperature_history)
            temperature_mean = float(np.mean(temperature_history))
            logger.info(u'Temperature stable at (%.2f+/-%.2f)K during scans.'
                        % (temperature_mean, temperature_var / 2))

        logger.info('All scans complete.')

        # -----------------show and save data----------
        # switch viewpoint to experiment which just finished running
        time.sleep(self.wait)
        exp_title = exp.aqGetExpName()
        time.sleep(self.wait)
        self.XeprCmds.aqExpSelect(1, exp_title)
        time.sleep(self.wait)

        # save the data if path is given
        # add temperature data and Q-value if available
        if path is None:
            path = os.path.join(tempfile.gettempdir(), 'autosave_' +
                                next(tempfile._get_candidate_names()))

        self._saveCurrentData(path, exp)
        time.sleep(self.wait)

        basename = path.split('.')[0]
        dsc_path = basename + '.DSC'

        dset = XeprData(dsc_path)

        if self._last_qvalue is not None:
            try:
                dset.set_par('QValue', self._last_qvalue)
            except ValueError:
                mw_bridge_layer = dset.dsl.groups['mwBridge']
                mw_bridge_layer.pars['QValue'] = XeprParam(self._last_qvalue)

        if temperature_history is not None:
            param_list = dict()
            param_list['AcqWaitTime'] = XeprParam(self._temp_wait_time, 's')
            param_list['Temperature'] = XeprParam(self.feed.control.t_setpoint, 'K')
            param_list['Tolerance'] = XeprParam(self._temperature_tolerance, 'K')
            param_list['Stability'] = XeprParam(round(temperature_var, 4), 'K')
            param_list['Mean'] = XeprParam(round(temperature_mean, 4), 'K')
            tg = ParamGroupDSL(name='tempCtrl', pars=param_list)
            dset.dsl.groups['tempCtrl'] = tg

        dset.save(path)

        return dset

    @queued_exec(manager.job_queue)
    def saveCurrentData(self, path, exp=None):
        """
        Saves the data from a given experiment in Xepr to the specified path. If
       ``exp`` is `None` the currently displayed data set is saved.

        Xepr only allows file paths shorter than 128 characters.

        :param str path: Absolute path to save data file. Must be shorter than 128
            characters.
        :param exp: Xepr experiment instance associated with data set. Defaults
            to currently selected experiment if not given.
        """

        print('To save a just completed measurement, please use the "path" argument ' +
              'of "runXeprExperiment". This will automatically add temperature ' +
              'stability and Q-value information to your data files.')

        self._saveCurrentData(path, exp)

    @queued_exec(manager.job_queue)
    def setStandby(self):
        """
        Sets the magnetic field to zero and the MW bridge to standby.
        """

        if not self._check_for_xepr():
            raise RuntimeError('Not connected to Xepr.')

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

    def _saveCurrentData(self, path, exp=None):
        """
        Saves the data from a given experiment in Xepr to the specified path. If
       ``exp`` is `None` the currently displayed data set is saved.

        Xepr only allows file paths shorter than 128 characters.

        :param str path: Absolute path to save data file. Must be shorter than 128
            characters.
        :param exp: Xepr experiment instance associated with data set. Defaults
            to currently selected experiment if not given.
        """

        if not self._check_for_xepr():
            raise RuntimeError('Not connected to Xepr.')

        path = os.path.expanduser(path)

        if len(path) > 128:
            raise ValueError('Only paths with with 128 characters or less are ' +
                             'by Xepr.')

        directory, filename = os.path.split(path)

        # check if directory is valid, create otherwise
        if not os.path.isdir(directory):
            os.makedirs(directory)

        # switch viewpoint to experiment if given
        if exp is not None:
            exp_title = exp.aqGetExpName()
            time.sleep(self.wait)
            self.XeprCmds.aqExpSelect(1, exp_title)
            time.sleep(self.wait)

        # tell Xepr to save data
        self.XeprCmds.ddPath(path)
        time.sleep(self.wait)
        self.XeprCmds.vpSave('Current Primary', filename,  path)
        time.sleep(self.wait)
        logger.info('Data saved to %s.' % path)

    def _tuneBias(self):
        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Bias).')
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
        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Iris).')
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
            time.sleep(self.wait)
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
        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Freq).')
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
        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Phase).')
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

        # determine the direction of increasing diode current
        diode_curr_array = np.array([])
        interval_min = max(phase0-3*phase_step, phase_min)
        interval_max = min(phase0+4*phase_step, phase_max)
        phase_array = np.arange(interval_min, interval_max, phase_step)

        for phase in phase_array:
            # Check for abort event
            if self.abort.is_set():
                return
            # Abort if phase at limit
            if self._phase_at_limit(phase, phase_min, phase_max):
                return
            self.hidden['SignalPhase'].value = phase
            time.sleep(1)
            diode_curr = self.hidden['DiodeCurrent'].value
            time.sleep(self.wait)
            diode_curr_array = np.append(diode_curr_array, diode_curr)
            if time.time() - t0 > self._tuning_timeout:
                logger.warning('Phase tuning timeout.')
                break

        upper = np.mean(diode_curr_array[phase_array > phase0])
        lower = np.mean(diode_curr_array[phase_array < phase0])
        direction = cmp(upper, lower)

        # determine position of maximum phase by stepping until phase deceases again
        self.hidden['SignalPhase'].value = phase0
        time.sleep(1)
        diode_curr_new = self.hidden['DiodeCurrent'].value
        time.sleep(self.wait)

        phase_array = np.array([phase0])
        diode_curr_array = np.array([diode_curr_new])

        new_phase = phase0

        while diode_curr_new > np.max(diode_curr_array) - 15:
            # get next phase step
            new_phase += direction*phase_step

            # check for abort event
            if self.abort.is_set():
                return

            # check for limits of diode range, readjust iris if necessary and abort
            if diode_curr_new in [0, 400]:
                self._tuneIris()
                return

            # abort if phase at limit
            if self._phase_at_limit(new_phase, phase_min, phase_max):
                return

            # get new reading
            self.hidden['SignalPhase'].value = new_phase
            time.sleep(1)
            diode_curr_new = self.hidden['DiodeCurrent'].value
            time.sleep(self.wait)

            diode_curr_array = np.append(diode_curr_array, diode_curr_new)
            phase_array = np.append(phase_array, new_phase)

            # timeout if Xepr is not responsive
            if time.time() - t0 > self._tuning_timeout:
                logger.warning('Phase tuning timeout.')
                break

        # set phase to the best value
        best_phase = phase_array[np.argmax(diode_curr_array)]
        self.hidden['SignalPhase'].value = best_phase
        time.sleep(self.wait)

    def _phase_at_limit(self, phase, phase_min, phase_max):

        assert phase_max > phase_min

        deg_step = 6.5  # approximate step of 1 deg

        if phase_min < phase < phase_max:
            return False
        else:
            # shift by 360° if maximum or minimum is encountered
            direction = int(phase < phase_min) - int(phase > phase_max)
            self.hidden['SignalPhase'].value = phase + direction*360*deg_step
            logger.info('Phase at limit, cycling by 360 deg.')
            time.sleep(4)
            return True

# ========================================================================================
# set up cryostat functions
# ========================================================================================

    @queued_exec(manager.job_queue)
    def setTemperature(self, target, auto_gf=True):
        """
        Sets the target temperature for the ESR900 cryostat and waits for it to
        stabilize within :attr:`temp_wait_time` with fluctuations below
        :attr:`temperature_tolerance`.

        Warns the user if this takes too long.

        :param float target: Target temperature in Kelvin.
        :param bool auto_gf: If `True`, the gasflow will be controlled automatically by the Mercury.
        """

        if not self._check_for_mercury():
            raise RuntimeError('Not connected to MercuryITC.')

        # create instance variable here to allow outside access
        self._temperature_target = target
        logger.info('Setting target temperature to %sK.' % self._temperature_target)

        # set temperature and wait to stabilize
        self.feed.control.t_setpoint = self._temperature_target
        self._waitStable(auto_gf=auto_gf)

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

    def _waitStable(self, auto_gf=True):
        """
        Waits for the cryostat temperature to stabilize within the specified
        tolerance :attr:`temperature_tolerance`. Releases after it has been
        stable for :attr:`temp_wait_time` seconds (default of 120 sec).
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
            if not auto_gf:
                if gasflow_man_counter == 0:
                    self.feed.control.flow_auto = 'OFF'
                    if self._temperature_target > 247:
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
        """
        Calculates the ideal heater voltage for a given temperature. This function
        can be used to check the current gas flow: If the heater voltage exceeds its
        target value, the gas flow likely too high (and vice versa).

        :param float temperature: Temperature in Kelvin.
        """
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
            expected_time = abs(self._temperature_target - self.feed.readings['Temp']) / 5
        return expected_time * 60  # return value in sec

    @queued_exec(manager.job_queue)
    def setTempRamp(self, ramp):
        """
        Sets the temperature ramp for the ESR900 cryostat in K/min.

        :param float ramp: Ramp in Kelvin per minute.
        """

        if not self._check_for_mercury():
            raise RuntimeError('Not connected to MercuryITC.')

        # set temperature and wait to stabilize
        self.feed.control.ramp = ramp
        logger.info('Temperature ramp set to %s K/min.' % ramp)

# ========================================================================================
# set up Keithley functions
# ========================================================================================

    @queued_exec(manager.job_queue)
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
        Records a transfer curve and saves returns the resulting data. If a valid
        path is given, the data is also saved as a .txt file.

        :param smu_gate: Name of SMU attached to the gate electrode of an FET.
        :param smu_drain: Name of SMU attached to the drain electrode of an FET.
        :param float vg_start: Start voltage of transfer sweep in Volts.
        :param float vg_stop: End voltage of transfer sweep in Volts.
        :param float vg_step: Voltage step size for transfer sweep in Volts.
        :param list vd_list: List of drain voltage steps in Volts.
        :param float t_int: Integration time in sec for every data point.
        :param float delay: Settling time in sec before every measurement. Set
            to -1 for for automatic delay.
        :param bool pulsed: True or False for pulsed or continuous measurements.
        :param str path: File path to save transfer curve data as .txt file.

        :returns: Transfer curve data.
        :rtype: :class:`keithley2600.TransistorSweepData`
        """

        if not self._check_for_keithley():
            raise RuntimeError('Not connected to Keithley.')

        smu_gate = getattr(self.keithley, smu_gate)
        smu_drain = getattr(self.keithley, smu_drain)

        sd = self.keithley.transferMeasurement(smu_gate, smu_drain, vg_start,
                                               vg_stop, vg_step, vd_list, t_int,
                                               delay, pulsed)
        if path is not None:
            sd.save(path)

        return sd

    @queued_exec(manager.job_queue)
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
        Records an output curve and returns the resulting data. If a valid
        path is given, the data is also saved as a .txt file.

        :param smu_gate: Name of SMU attached to the gate electrode of an FET.
        :param smu_drain: Name of SMU attached to the drain electrode of an FET.
        :param float vd_start: Start voltage of output sweep in Volts .
        :param float vd_stop: End voltage of output sweep in Volts.
        :param float vd_step: Voltage step size for output sweep in Volts.
        :param list vg_list: List of gate voltage steps in Volts.
        :param float t_int: Integration time in sec for every data point.
        :param float delay: Settling time in sec before every measurement. Set
            to -1 for for automatic delay.
        :param bool pulsed: True or False for pulsed or continuous measurements.
        :param str path: File path to save output curve data as .txt file.

        :returns: Output curve data.
        :rtype: :class:`keithley2600.TransistorSweepData`
        """

        if not self._check_for_keithley():
            raise RuntimeError('Not connected to Keithley.')

        smu_gate = getattr(self.keithley, smu_gate)
        smu_drain = getattr(self.keithley, smu_drain)

        sd = self.keithley.outputMeasurement(smu_gate, smu_drain, vd_start,
                                             vd_stop, vd_step, vg_list, t_int,
                                             delay, pulsed)
        if path is not None:
            sd.save(path)

        return sd

    @queued_exec(manager.job_queue)
    def setGateVoltage(self, v, smu_gate=K_CONF.get('Sweep', 'gate')):
        """
        Sets the gate bias of the given keithley, grounds other SMUs.

        :param float v: Gate voltage in Volts.
        :param str smu_gate: Name of SMU. Defaults to the SMU saved as gate.
        """

        if not self._check_for_keithley():
            raise RuntimeError('Not connected to Keithley.')

        gate = getattr(self.keithley, smu_gate)

        # turn off all remaining SMUs
        other_smus = filter(lambda a: a != smu_gate, self.keithley.SMU_LIST)
        for smu_name in other_smus:
            smu = getattr(self.keithley, smu_name)
            smu.source.output = self.keithley.OUTPUT_OFF

        self.keithley.rampToVoltage(gate, target_volt=v, delay=0.1, step_size=1)

        if v == 0:
            self.keithley.reset()

    @queued_exec(manager.job_queue)
    def applyDrainCurrent(self, i, smu=K_CONF.get('Sweep', 'drain')):
        """
        Applies a specified current to the selected Keithley SMU.

        :param float i: Drain current in Ampere.
        :param str smu: Name of SMU. Defaults to the SMU saved as drain.
        """

        if not self._check_for_keithley():
            raise RuntimeError('Not connected to Keithley.')

        smu = getattr(self.keithley, smu)

        self.keithley.applyCurrent(smu, i)
        self.keithley.beep(0.3, 2400)

# ========================================================================================
# Helper methods
# ========================================================================================

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
