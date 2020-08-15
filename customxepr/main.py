# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.
"""
import os
import logging
import time
import types
from datetime import timedelta, datetime
import numpy as np
import tempfile

from pint import UnitRegistry
from keithleygui.config.main import CONF as KCONF
from mercuryitc.mercury_driver import MercuryITC_TEMP

from customxepr.utils import EmailSender
from customxepr.experiment import ModePicture, XeprData, XeprParam
from customxepr.experiment.xepr_dataset import ParamGroupDSL
from customxepr.manager import Manager
from customxepr.config import CONF

try:
    from XeprAPI import ExperimentError
except ImportError:
    ExperimentError = RuntimeError

_root = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('customxepr')

ureg = UnitRegistry()
Q_ = ureg.Quantity


def cmp(a, b):
    return bool(a > b) - bool(a < b)  # convert possible numpy-bool to bool


# noinspection PyUnresolvedReferences
class CustomXepr(object):
    """
    CustomXepr defines routines to control Bruker's Xepr software and to run full ESR
    measurement cycles. When creating an instance of CustomXepr, you can pass instances of
    :class:`XeprAPI.XeprAPI`, :class:`mercurygui.MercuryFeed` and
    :py:class:`keithley2600.Keithley2600` to handle interactions with the respective
    instruments.

    All CustomXepr methods that do not end with '_sync' are executed in a worker thread in
    the order of their calls. Scheduling of jobs and retrieval of results is handled by
    :class:`manager.Manager`. For instructions on how to schedule your own experiments,
    please refer to the documentation of :mod:`manager`.

    Every asynchronous method has an equivalent method ending with '_sync' which will be
    called immediately and block until it is done. Those synchronous equivalents are
    generated at runtime and not documented here.

    You can use :class:`CustomXepr` on its own, but it is recommended to start it with the
    function :func:`startup.run` in the :mod:`startup` module. This will automatically
    connect to available instruments and start CustomXepr's graphical user interfaces.

    :param xepr: Xepr instance from the Bruker Python XeprAPI. Defaults to `None` if not
        provided.
    :param mercuryfeed: :class:`mercurygui.MercuryFeed` instance for live feed from
        MercuryiTC temperature controller. Defaults to `None` if not provided.
    :param keithley: :class:`keithley2600.Keithley2600` instance from keithley2600 driver.
        Defaults to `None` if not provided.
    """

    manager = Manager()

# ========================================================================================
# Set up basic CustomXepr functionality
# ========================================================================================

    def __init__(self, xepr=None, mercury=None, keithley=None):

        super(self.__class__, self).__init__()
        self.emailSender = EmailSender(
            mailhost=(CONF.get('SMTP', 'mailhost'), CONF.get('SMTP', 'port')),
            fromaddr=CONF.get('SMTP', 'fromaddr'),
            credentials=CONF.get('SMTP', 'credentials'),
            secure=CONF.get('SMTP', 'secure'),
        )

        # =====================================================================
        # check if connections to Xepr, MercuryiTC and Keithley are present
        # =====================================================================

        self.xepr = xepr
        self.mercury = mercury
        self.keithley = keithley

        # hidden Xepr experiment, created when EPR is connected:
        self.hidden = None

        self._check_for_xepr(raise_error=False)
        self._check_for_keithley(raise_error=False)

        if self._check_for_mercury(raise_error=False):

            temperature_module_name = CONF.get('CustomXepr', 'esr_temperature_nick')
            cooling_module_name = CONF.get('CustomXepr', 'cooling_temperature_nick')

            self.esr_temperature, self.esr_gasflow, self.esr_heater = \
                self._select_temp_sensor(temperature_module_name)

            self.cooling_temperature, _, _ = self._select_temp_sensor(cooling_module_name)

        else:
            self.esr_temperature = self.esr_gasflow = self.esr_heater = None
            self.cooling_temperature = None

        # =====================================================================
        # define / load certain settings for customxepr functions
        # =====================================================================

        # settling time for cryostat temperature (in sec)
        self._temp_wait_time = CONF.get('CustomXepr', 'temp_wait_time')
        # ESR temperature stability tolerance (in K)
        self._temperature_tolerance = CONF.get('CustomXepr', 'esr_temperature_tolerance')
        # cooling temperature stability tolerance (in K)
        self._max_cooling_temperature = CONF.get('CustomXepr', 'max_cooling_temperature')

        self._wait = 0.2  # waiting time for Xepr to process commands (in sec)
        self._tuning_timeout = 60  # timeout for phase tuning (in sec)

        self._last_qvalue = None  # last measured Q-value
        self._last_qvalue_err = None  # last measured Q-value error

        # =====================================================================
        # interaction with manager
        # =====================================================================
        self.abort = self.manager.abort

        if keithley is not None:
            self.manager.abort_events = [self.keithley.abort_event]

        # =====================================================================
        # create synchronous versions of CustomXepr methods
        # =====================================================================

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, '__wrapped__'):
                setattr(self, attr_name + '_sync', types.MethodType(attr.__wrapped__, self))

# ========================================================================================
# define basic functions for email notifications, pausing, etc.
# ========================================================================================

    @property
    def notify_address(self):
        """List with email addresses for status notifications."""
        return self.manager.notify_address

    @notify_address.setter
    def notify_address(self, address_list):
        """Setter: List with email addresses for notifications."""
        self.manager.notify_address = address_list

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

    @manager.queued_exec
    def sendEmail(self, body):
        """
        Sends an email to the list of addresses given by :attr:`notify_address`.
        The email server and sender address can be configured in the config file.

        :param str body: Text to send.
        """
        self.emailSender.sendmail(self.notify_address, 'CustomXepr Notification', body)

    @manager.queued_exec
    def sleep(self, seconds):
        """
        Pauses for the specified amount of seconds. Sleeping can be aborted
        by the user.

        :param int seconds: Number of seconds to pause.
        """
        eta = time.time() + seconds
        eta_string = time.strftime('%H:%M', time.localtime(eta))
        message = 'Waiting for {:.0f} seconds, ETA: {}.'.format(seconds, eta_string)
        logger.info(message)

        # brake up into 1 sec sleep intervals, give option to abort
        if seconds > 1:
            for i in range(0, seconds):
                time.sleep(1)
                logger.status('Waiting {:.0f}/{:.0f}.'.format(i+1, seconds))
                # check for abort event
                if self.abort.is_set():
                    logger.info('Aborted by user.')
                    return
        # use a single sleep command for less than one second pause
        else:
            time.sleep(seconds)

# ========================================================================================
# set up Xepr functions
# ========================================================================================

    @manager.queued_exec
    def tune(self):
        """
        Runs Xepr's built-in tuning routine.
        """

        self._check_for_xepr()

        idle_state = self.hidden['TuneState'].value
        time.sleep(self._wait)

        self.hidden['OpMode'].value = 'Tune'
        time.sleep(self._wait)
        self.hidden['Tune'].value = 'Up'
        time.sleep(self._wait)

        while self.hidden['TuneState'].value == idle_state:
            if self.abort.is_set():
                self.hidden['Tune'].value = 'Stop'
                time.sleep(self._wait)
                logger.info('Tuning aborted by user.')
                return
            else:
                time.sleep(1)

        while self.hidden['TuneState'].value != idle_state:
            if self.abort.is_set():
                self.hidden['Tune'].value = 'Stop'
                time.sleep(self._wait)
                logger.info('Tuning aborted by user.')
                return
            else:
                time.sleep(1)

    @manager.queued_exec
    def finetune(self):
        """
        Runs Xepr's built-in finetuning routine.
        """

        self._check_for_xepr()
        idle_state = self.hidden['TuneState'].value

        self.hidden['Tune'].value = 'Fine'
        time.sleep(self._wait)

        while self.hidden['TuneState'].value == idle_state:
            if self.abort.is_set():
                self.hidden['Tune'].value = 'Stop'
                time.sleep(self._wait)
                logger.info('Tuning aborted by user.')
                return
            else:
                time.sleep(1)

        while self.hidden['TuneState'].value != idle_state:
            if self.abort.is_set():
                self.hidden['Tune'].value = 'Stop'
                time.sleep(self._wait)
                logger.info('Tuning aborted by user.')
                return
            else:
                time.sleep(1)

    @manager.queued_exec
    def customtune(self, low_q=False):
        """
        Custom tuning routine with higher accuracy. It takes longer than :meth:`tune`
        and requires the spectrometer to be already close to tuned. In case of lossy
        samples, you can set ``lowQ`` to ``True`` so that the tuning routine will cycle
        through a smaller range of microwave powers. For lossy samples where the Q-value
        will be lower than 3000, it is recommended to manually tune the cavity.

        :param bool low_q: If ``True``, the tuning routine will be adjusted for lossy samples.
        """

        self._check_for_xepr()

        iris_tolerance = 3 if low_q else 1
        bias_tolerance = 3 if low_q else 1
        freq_tolerance = 5 if low_q else 2

        logger.info('Tuning.')

        # save current operation mode and attenuation
        mode = self.hidden['OpMode'].value
        time.sleep(self._wait)
        atten_start = self.hidden['PowerAtten'].value
        time.sleep(self._wait)

        # switch mode to 'Operate'
        if not mode == 'Operate':
            self.hidden['OpMode'].value = 'Operate'
            time.sleep(self._wait)

        dB_min = 10 if not low_q else 20
        dB_max = 50 if not low_q else 45

        # tune frequency and phase at 30 dB
        self.hidden['PowerAtten'].value = 30
        time.sleep(self._wait)
        self.tuneFreq(freq_tolerance)
        time.sleep(self._wait)
        self.tunePhase()
        time.sleep(self._wait)

        # tune bias of reference arm at dB_max
        # (where diode current is determined by reference arm)
        self.hidden['PowerAtten'].value = dB_max
        time.sleep(self._wait)
        self.tuneBias(bias_tolerance)
        time.sleep(self._wait)

        # tune iris at 40 dB and 30 dB
        for atten in [40, 30]:
            # check for abort event
            if self.abort.is_set():
                self.hidden['PowerAtten'].value = atten_start
                time.sleep(self._wait)
                logger.info('Aborted by user.')
                return

            self.hidden['PowerAtten'].value = atten
            time.sleep(self._wait)

            self.tuneIris(iris_tolerance)
            time.sleep(self._wait)

        # tune iris and phase and frequency at 20 dB and dB_min
        for atten in [20, dB_min]:
            # check for abort event, clear event
            if self.abort.is_set():
                self.hidden['PowerAtten'].value = atten_start
                time.sleep(self._wait)
                logger.info('Aborted by user.')
                return

            self.hidden['PowerAtten'].value = atten
            time.sleep(self._wait)
            self.tunePhase()
            time.sleep(self._wait)
            self.tuneIris(iris_tolerance)
            time.sleep(self._wait)
            self.tuneFreq(freq_tolerance)
            time.sleep(self._wait)

        # tune bias at dB_max
        self.hidden['PowerAtten'].value = dB_max
        time.sleep(self._wait)
        self.tuneBias(bias_tolerance)
        time.sleep(self._wait)

        # tune iris at 15 dB
        self.hidden['PowerAtten'].value = 20
        time.sleep(self._wait)
        self.tuneIris(iris_tolerance)
        time.sleep(self._wait)

        # tune bias at dB_max
        self.hidden['PowerAtten'].value = dB_max
        time.sleep(self._wait)
        self.tuneBias(bias_tolerance)
        time.sleep(self._wait)

        # tune iris at dB_min
        self.hidden['PowerAtten'].value = dB_min
        time.sleep(self._wait)
        self.tuneIris(iris_tolerance)
        time.sleep(self._wait)

        # reset attenuation to original value, tune frequency again
        self.hidden['PowerAtten'].value = atten_start
        time.sleep(self._wait)
        self.tuneFreq(freq_tolerance)
        time.sleep(self._wait)

        logger.status('Tuning done.')

    @manager.queued_exec
    def tuneBias(self, tolerance=1):
        """
        Tunes the diode bias only. A perfectly tuned bias results in a diode current of
        200 mA for all microwave powers.

        :param int tolerance: Minimum diode current offset that must be achieved before
            :meth:`tuneBias` returns.
        """
        self._check_for_xepr()

        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Bias).')
        time.sleep(self._wait)

        # get offset from 200 mA
        diff = self.hidden['DiodeCurrent'].value - 200
        time.sleep(self._wait)
        tolerance1 = 10  # tolerance for fast tuning
        tolerance2 = tolerance  # tolerance for second fine tuning

        # rapid tuning with high tolerance and large steps
        while abs(diff) > tolerance1:
            # check for abort event
            if self.abort.is_set():
                return

            step = 1*cmp(0, diff)  # coarse step of 1
            self.XeprCmds.aqParStep('AcqHidden', '*cwBridge.SignalBias',
                                    'Coarse {}'.format(step))  # TODO: migrate from XeprCmds
            time.sleep(0.5)
            diff = self.hidden['DiodeCurrent'].value - 200
            time.sleep(self._wait)

        # fine tuning with low tolerance and small steps
        while abs(diff) > tolerance2:
            # check for abort event
            if self.abort.is_set():
                return

            step = 5*cmp(0, diff)  # fine step of 5
            self.XeprCmds.aqParStep('AcqHidden', '*cwBridge.SignalBias',
                                    'Fine {}'.format(step))  # TODO: migrate from XeprCmds
            time.sleep(0.5)
            diff = self.hidden['DiodeCurrent'].value - 200
            time.sleep(self._wait)

    @manager.queued_exec
    def tuneIris(self, tolerance=1):
        """
        Tunes the cavity's iris only. A perfectly tuned iris results in a diode current of
        200 mA for all microwave powers.

        :param int tolerance: Minimum diode current offset that must be achieved before
            :meth:`tuneIris` returns.
        """
        self._check_for_xepr()

        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Iris).')
        time.sleep(self._wait)

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
            time.sleep(self._wait)
            # set value to 0.1 if step is smaller
            # (usually only happens below 10dB)
            step = max(step, 0.1)
            # increase waiting time between steps when close to tuned
            # with a maximum waiting of 1 sec
            wait = min(5/(abs(diff) + 0.1), 1)
            self.XeprCmds.aqParSet('AcqHidden', cmd, 'True')  # TODO: migrate from XeprCmds
            time.sleep(step)
            self.XeprCmds.aqParSet('AcqHidden', cmd, 'False')  # TODO: migrate from XeprCmds
            time.sleep(wait)

            diff = self.hidden['DiodeCurrent'].value - 200
            time.sleep(self._wait)

    @manager.queued_exec
    def tuneFreq(self, tolerance=2):
        """
        Tunes the microwave frequency only, to a lock offset close to zero.

        :param int tolerance: Minimum lock offset that must be achieved before
            :meth:`tuneFreq` returns.
        """
        self._check_for_xepr()

        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Freq).')
        time.sleep(self._wait)

        fq_offset = self.hidden['LockOffset'].value
        time.sleep(self._wait)

        while abs(fq_offset) > tolerance:
            # check for abort event
            if self.abort.is_set():
                return

            step = 1 * cmp(0, fq_offset) * max(abs(int(fq_offset/10)), 1)
            self.XeprCmds.aqParStep('AcqHidden', '*cwBridge.Frequency',
                                    'Fine {}'.format(step))
            time.sleep(1)
            fq_offset = self.hidden['LockOffset'].value
            time.sleep(self._wait)

    @manager.queued_exec
    def tunePhase(self):
        """
        Tunes the phase of the MW reference arm only such that the diode current is
        maximized.
        """
        self._check_for_xepr()
        # check for abort event
        if self.abort.is_set():
            return

        logger.status('Tuning (Phase).')
        time.sleep(self._wait)

        t0 = time.time()

        # get current phase and range
        phase0 = self.hidden['SignalPhase'].value
        time.sleep(self._wait)
        phase_min = self.hidden['SignalPhase'].aqGetParMinValue()
        time.sleep(self._wait)
        phase_max = self.hidden['SignalPhase'].aqGetParMaxValue()
        time.sleep(self._wait)
        phase_step = self.hidden['SignalPhase'].aqGetParCoarseSteps()
        time.sleep(self._wait)

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
            time.sleep(self._wait)
            diode_curr_array = np.append(diode_curr_array, diode_curr)
            if time.time() - t0 > self._tuning_timeout:
                logger.info('Phase tuning timeout.')
                break

        upper = np.mean(diode_curr_array[phase_array > phase0])
        lower = np.mean(diode_curr_array[phase_array < phase0])
        direction = cmp(upper, lower)

        # determine position of maximum phase by stepping until phase deceases again
        self.hidden['SignalPhase'].value = phase0
        time.sleep(1)
        diode_curr_new = self.hidden['DiodeCurrent'].value
        time.sleep(self._wait)

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
                self.tuneIris(tolerance=10)
                return

            # abort if phase at limit
            if self._phase_at_limit(new_phase, phase_min, phase_max):
                return

            # get new reading
            self.hidden['SignalPhase'].value = new_phase
            time.sleep(1)
            diode_curr_new = self.hidden['DiodeCurrent'].value
            time.sleep(self._wait)

            diode_curr_array = np.append(diode_curr_array, diode_curr_new)
            phase_array = np.append(phase_array, new_phase)

            # timeout if Xepr is not responsive
            if time.time() - t0 > self._tuning_timeout:
                logger.info('Phase tuning timeout.')
                break

        # set phase to the best value
        best_phase = phase_array[np.argmax(diode_curr_array)]
        self.hidden['SignalPhase'].value = best_phase
        time.sleep(self._wait)

    @manager.queued_exec
    def getQValueFromXepr(self, path=None, temperature=298):
        """
        Gets the Q-Value as determined by Xepr, averaged over 20 readouts, and saves it
        in the specified file.

        :param str path: Directory where Q-Value reading is saved with corresponding
            temperature and time-stamp.
        :param float temperature: Temperature in Kelvin during Q-Value measurement.

        :returns: Measured Q-Value.
        :rtype: float
        """

        self._check_for_xepr()

        wait_old = self._wait
        self._wait = 1

        logger.info('Reading Q-value.')

        att = self.hidden['PowerAtten'].value  # remember current attenuation
        time.sleep(self._wait)
        self.hidden['OpMode'].value = 'Tune'
        time.sleep(self._wait)
        self.hidden['RefArm'].value = 'On'
        time.sleep(self._wait)
        self.hidden['PowerAtten'].value = 33
        time.sleep(self._wait)
        self.hidden['ModeZoom'].value = 2
        time.sleep(self._wait)

        q_values = np.array([])

        time.sleep(1)

        for iteration in range(0, 40):
            # check for abort event
            if self.abort.is_set():
                logger.info('Aborted by user.')
                return
            q_values = np.append(q_values, self.hidden['QValue'].value)
            time.sleep(1)

        self.hidden['PowerAtten'].value = 32
        time.sleep(self._wait)
        self.hidden['ModeZoom'].value = 1
        time.sleep(self._wait)
        self.hidden['RefArm'].value = 'On'
        time.sleep(self._wait)
        self.hidden['OpMode'].value = 'Operate'

        time.sleep(3)

        self.tuneFreq()
        self.tuneFreq()
        self.tuneBias()
        self.tuneFreq()

        self.hidden['PowerAtten'].value = att
        time.sleep(self._wait)
        q_mean = q_values.mean()
        q_stderr = q_values.std()

        if path is not None:
            path = os.path.join(path, 'QValues.txt')
            self._saveQValue2File(temperature, q_mean, q_stderr, path)

        if q_mean > 3000:
            logger.info('Q = {:.0f}+/-{:.0f}.'.format(q_mean, q_stderr))
        elif q_mean <= 3000:
            logger.warning('Q = {:.0f}+/-{:.0f} is very small. Please check on '
                           'experiment.'.format(q_mean, q_stderr))

        self._wait = wait_old

        return q_mean

    @manager.queued_exec
    def getQValueCalc(self, path=None, temperature=298):
        """
        Calculates the Q-value by fitting the cavity mode picture to a Lorentzian
        resonance with a polynomial baseline. It uses all available zoom factors to
        resolve both sharp and broad resonances (high and low Q-values, respectively) and
        is therefore more accurate than :meth:`getQValueFromXepr`.

        :param str path: Directory where Q-Value reading is saved with corresponding
            temperature and time-stamp.
        :param float temperature: Temperature in Kelvin during a Q-value measurement.
            Defaults to room temperature.

        :returns: Mode picture instance.
        :rtype: :class:`experiment.ModePicture`
        """

        self._check_for_xepr()

        wait_old = self._wait
        self._wait = 1

        logger.info('Reading Q-value.')
        att = self.hidden['PowerAtten'].value  # remember current attenuation
        time.sleep(self._wait)
        freq = self.hidden['FrequencyMon'].value  # get current frequency
        time.sleep(self._wait)

        self.hidden['OpMode'].value = 'Tune'
        time.sleep(self._wait)
        self.hidden['RefArm'].value = 'Off'
        time.sleep(self._wait)
        self.hidden['LogScaleEnab'].value = False  # ensure linear scale mode picture
        time.sleep(self._wait)
        self.hidden['PowerAtten'].value = 33
        time.sleep(1)

        self.hidden['PowerAtten'].value = 20
        time.sleep(2)

        # collect mode pictures for different zoom levels
        mode_pic_data = {}

        for mode_zoom in [1, 2, 4, 8]:

            # check for abort event
            if self.abort.is_set():
                logger.info('Aborted by user.')
                return

            y_data = np.array([])

            self.hidden['ModeZoom'].value = mode_zoom
            time.sleep(2)

            n_points = int(self.hidden['DataRange'][1])
            time.sleep(self._wait)

            for i in range(0, n_points):
                y_data = np.append(y_data, self.hidden['Data'][i])

            mode_pic_data[mode_zoom] = y_data

        mp = ModePicture(mode_pic_data, freq)
        self._last_qvalue = mp.qvalue
        self._last_qvalue_err = mp.qvalue_stderr

        self.hidden['PowerAtten'].value = 30
        time.sleep(self._wait)
        self.hidden['ModeZoom'].value = 1
        time.sleep(self._wait)
        self.hidden['RefArm'].value = 'On'
        time.sleep(self._wait)
        self.hidden['OpMode'].value = 'Operate'

        time.sleep(2)

        self.tuneFreq()
        self.tuneFreq()
        self.tuneBias()
        self.tuneFreq()

        self.hidden['PowerAtten'].value = att
        time.sleep(self._wait)

        if mp.qvalue > 3000:
            logger.info('Q = {:.0f}+/-{:.0f}.'.format(mp.qvalue, mp.qvalue_stderr))
        elif mp.qvalue <= 3000:
            logger.warning('Q = {:.0f}+/-{:.0f} is very small. Please check on '
                           'experiment.'.format(mp.qvalue, mp.qvalue_stderr))

        if path is not None:
            path = os.path.expanduser(path)
            if not os.path.isdir(path):
                raise IOError('"{}" is not a valid directory.'.format(path))

            path1 = os.path.join(path, 'QValues.txt')
            path2 = os.path.join(path, 'ModePicture{0:03d}K.txt'.format(int(temperature)))

            self._saveQValue2File(temperature, mp.qvalue, mp.qvalue_stderr, path1)
            mp.save(path2)

        self._wait = wait_old

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

    @staticmethod
    def getExpDuration(exp):
        """
        Estimates the time required to run the given experiment. The returned value is
        given in seconds and is a lower limit, the actual run time may be longer due to
        fine-tuning between scans, waiting times for stabilization and flybacks.

        :param exp: Xepr experiment object to run.

        :returns: Estimated experiment duration in seconds.
        :rtype: float
        """

        sweep_time_par = exp['signalChannel.SweepTime']
        sweep_time = Q_(sweep_time_par.value, sweep_time_par.aqGetParUnits())

        field_delay_par = exp['fieldCtrl.Delay']  # given in s
        field_delay = Q_(field_delay_par.value, field_delay_par.aqGetParUnits())

        nb_scans = exp['NbScansToDo'].value

        ramp_step_time = (sweep_time + field_delay) * nb_scans  # total time for one step

        # check if we have a seconday axis
        if 'ramp2.*' in exp:
            if 'User defined' in exp['ramp2.sweepType'].value:
                nb_ramp = len(exp['ramp2.SweepData'].value.split())  # returns a space delimited str
            else:
                nb_ramp = exp['ramp2.NbPoints'].value
        else:
            nb_ramp = 1

        if 'delay2.*' in exp:
            ramp_delay_par = exp['delay2.Delay']
            ramp_delay = Q_(ramp_delay_par.value, ramp_delay_par.aqGetParUnits())
        else:
            ramp_delay = 0

        total = (ramp_step_time + ramp_delay) * nb_ramp

        return float(total / Q_('1 sec'))

    @manager.queued_exec
    def runXeprExperiment(self, exp, retune=True, path=None, **kwargs):
        """
        Runs the Xepr experiment ``exp``. Keyword arguments ``kwargs`` allow the user to
        pass experiment settings to Xepr (e.g., 'ModAmp' for modulation amplitude).
        Allowed parameters will depend on the type of experiment and its functional
        units, e.g., 'mwBridge', 'fieldCtrl' etc. You can get a list of all units and
        their parameters for a given experiment ``exp`` as follows:

        >>> print(exp.getFuList())
            ['acqStart',
             'fieldCtrl',
             'fieldSweep',
             'freqCounter',
             'mwBridge',
             'recorder',
             'scanEnd',
             'signalChannel']
        >>> print(exp.getFuParList('mwBridge'))
            ['AcqFineTuning',
             'AcqScanFTuning',
             'AcqSliceFTuning',
             'BrConnStatus',
             'BridgeCalib',
             'EMBType',
             'EWSMBC',
             'EmbBridge',
             'Power',
             'PowerAt0DB',
             'PowerAtten',
             'PowerAttenMon',
             'QValue',
             'TuneStateExpMon']

        If a temperature controller is connected, CustomXepr monitors the temperature
        during the measurement and emits warnings when fluctuations repeatedly exceed the
        given temperature stability requirement.

        If the ``path`` argument is given, the resulting data set is saved to the drive.
        Otherwise, a temporary file will be created (those are deleted periodically by the
        operating system). The temperature and its stability as well as the
        last-measurement Q-value (if available) are written to the Bruker '.DSC' file.

        :param exp: Xepr experiment object to run.
        :param bool retune: Retune iris and freq between scans (default: True).
        :param str path: Path to file. If given, the data set will be saved to this path,
            otherwise, a temporary file will be created. No Xepr file name restrictions
            apply.
        :param kwargs: Keyword arguments corresponding to Xepr experiment parameters.
            Allowed parameters will depend on the type of experiment.

        :returns: Xepr dataset.
        :rtype: :class:`experiment.XeprData`
        """

        self._check_for_xepr()

        # -----------set experiment parameters if given in kwargs--------------
        for key in kwargs:
            exp[key].value = kwargs[key]
            time.sleep(self._wait)

        d = timedelta(seconds=self.getExpDuration(exp))
        eta = datetime.now() + d

        logger.info(
            'Measurement "{0}" is running. Estimated duration: {1} min (ETA {2}).'.format(
                exp.aqGetExpName(),
                int(d.total_seconds()/60),
                eta.strftime('%H:%M')
            )
        )
        # -------------------start experiment----------------------------------

        has_mercury = self._check_for_mercury(raise_error=False)

        if has_mercury:
            temperature_fluct_history = np.array([])
            temperature_setpoint = self.esr_temperature.loop_tset
            n_temperature_volatile = 0
        else:
            temperature_fluct_history = None
            temperature_setpoint = None
            n_temperature_volatile = None

        if has_mercury and not self._cooling_temperature_ok():
            return

        exp.select()
        time.sleep(self._wait)
        exp.aqExpRun()
        time.sleep(self._wait)

        # wait for experiment to start
        while not exp.isRunning:
            time.sleep(self._wait)

        if retune:  # schedule pause after scan to retune
            time.sleep(1)
            exp.aqExpPause()
            time.sleep(self._wait)

        def is_running_or_paused():
            running = exp.isRunning
            time.sleep(self._wait)
            paused = exp.isPaused
            time.sleep(self._wait)
            return running or paused

        while is_running_or_paused():

            # check for abort event
            if self.abort.is_set():
                exp.aqExpPause()
                exp.aqExpAbort()
                time.sleep(self._wait)
                logger.info('Aborted by user.')
                return

            nb_scans_done = exp['NbScansDone'].value
            time.sleep(self._wait)
            nb_scans_to_do = exp['NbScansToDo'].value
            time.sleep(self._wait)
            logger.status('Recording scan {:.0f}/{.0f}.'.format(nb_scans_done + 1, nb_scans_to_do))

            if retune:
                # tune frequency and iris when a new slice scan starts
                if exp.isPaused and not nb_scans_done == nb_scans_to_do:
                    logger.status('Checking tuned.')
                    self.tuneFreq(tolerance=3)
                    self.tuneFreq(tolerance=3)
                    self.tuneIris(tolerance=7)

                    # start next scan
                    exp.aqExpRun()
                    time.sleep(self._wait)

                    # wait for scan to start and schedule next pause
                    while not exp.isRunning:
                        time.sleep(1)
                    exp.aqExpPause()
                    time.sleep(self._wait)

            # check cryostat and cooling water temperatures
            if has_mercury:

                if not self._cooling_temperature_ok():
                    return

                diff = abs(self.esr_temperature.temp[0] - temperature_setpoint)
                temperature_fluct_history = np.append(temperature_fluct_history, diff)
                # increment the number of violations n_out if temperature is unstable
                n_temperature_volatile += (diff > 4*self._temperature_tolerance)
                # warn once for every 120 temperature violations
                if np.mod(n_temperature_volatile, 120) == 1:
                    max_diff = np.max(temperature_fluct_history)
                    logger.warning('Temperature fluctuations of +/-{:.2f}K.'.format(max_diff))
                    n_temperature_volatile += 1  # prevent from warning again the next second

                # Pause measurement and raise error after 15 min of instability
                if n_temperature_volatile > 60 * 15:
                    exp.aqExpPause()
                    raise RuntimeError('Temperature could not be kept stable for ' +
                                       '15 min. Aborting current measurement and ' +
                                       'pausing all pending jobs.')

            time.sleep(1)

        # get temperature stability during scan if mercury was connected
        if has_mercury:
            max_diff = np.max(temperature_fluct_history)
            logger.info('Temperature stable at ({:.2f}+/-{:.2f})K during '
                        'scans.'.format(temperature_setpoint, max_diff))

        logger.info('All scans complete.')

        # -----------------show and save data----------
        # switch viewpoint to experiment which just finished running
        time.sleep(self._wait)
        exp_title = exp.aqGetExpName()
        time.sleep(self._wait)
        self.XeprCmds.aqExpSelect(1, exp_title)
        time.sleep(self._wait)

        # save the data to tmp file, this insures that we always save to a file path
        # that Xepr can handle

        with tempfile.NamedTemporaryFile(prefix='autosave_', delete=False) as f:
            tmp_path = f.name

        title = os.path.splitext(os.path.basename(path or tmp_path))[0]
        self._saveData(tmp_path, exp=exp, title=title)
        time.sleep(self._wait)

        # add temperature data and Q-value if available
        basename = tmp_path.split('.')[0]
        dsc_path = basename + '.DSC'

        dset = XeprData(dsc_path)

        if self._last_qvalue is not None:
            dsl_mwbridge = dset.dsl.groups['mwBridge']
            dsl_mwbridge.pars['QValue'] = XeprParam(self._last_qvalue)
            dsl_mwbridge.pars['QValueErr'] = XeprParam(self._last_qvalue_err)

        if has_mercury:
            dsl_temp = ParamGroupDSL(name='tempCtrl')
            dsl_temp.pars['Temperature'] = XeprParam(temperature_setpoint, 'K')
            dsl_temp.pars['Stability'] = XeprParam(round(max_diff, 4), 'K')
            dsl_temp.pars['AcqWaitTime'] = XeprParam(self._temp_wait_time, 's')
            dsl_temp.pars['Tolerance'] = XeprParam(self._temperature_tolerance, 'K')

            dset.dsl.groups['tempCtrl'] = dsl_temp

        if retune:
            dset.pars['AcqFineTuning'] = 'Slice'  # TODO: confirm correct value
            dset.pars['AcqSliceFTuning'] = 'On'

        new_path = path or tmp_path

        dset.save(new_path)
        logger.info('Data saved to "{}".'.format(new_path))

        return dset

    def _cooling_temperature_ok(self):

        if (self.cooling_temperature
                and self.cooling_temperature.temp[0] > self._max_cooling_temperature):
            logger.error('Cooling temperature above {} Celsius. Aborting '
                         'measurement.'.format(self._max_cooling_temperature))
            self.setStandby()
            self.manager.pause_worker()
            return False
        else:
            return True

    @manager.queued_exec
    def saveCurrentData(self, path, exp=None):
        """
        Saves the data from a given experiment in Xepr to the specified path. If ``exp``
        is `None` the currently displayed data set is saved.

        Xepr only allows file paths shorter than 128 characters.

        .. note::
           To save a just completed measurement, please use the ``path`` argument of
           :func:`runXeprExperiment`. This will automatically add temperature stability
           and Q-value information to your data files.

        :param str path: Absolute path to save data file. The path must be compatible with
            Xepr, i.e., it must be shorter than 128 characters.
        :param exp: Xepr experiment instance associated with data set. Defaults to
            currently selected experiment if not given.
        """

        print('To save a just completed measurement, please use the "path" argument ' +
              'of "runXeprExperiment". This will automatically add temperature ' +
              'stability and Q-value information to your data files.')

        self._saveData(path, exp)

        logger.info('Data saved to "{}".'.format(path))

    @manager.queued_exec
    def setStandby(self):
        """
        Sets the magnetic field to zero and the MW bridge to standby.
        """

        self._check_for_xepr()

        # check if WindDown experiment already exists, otherwise create
        try:
            wd = self.xepr.XeprExperiment('WindDown')
            time.sleep(self._wait)
        except ExperimentError:
            wd = self.xepr.XeprExperiment('WindDown', exptype='C.W.',
                                          axs1='Field', ordaxs='Signal channel')
        time.sleep(self._wait)

        wd.aqExpActivate()
        time.sleep(self._wait)
        wd['CenterField'].value = 0
        time.sleep(self._wait)
        wd['AtCenter'].value = True
        time.sleep(self._wait)

        self.hidden['OpMode'].value = 'Tune'
        time.sleep(3)
        self.hidden['OpMode'].value = 'Stand By'
        time.sleep(self._wait)

        logger.info('EPR set to standby.')

    def _saveData(self, path, exp=None, title=None):
        """
        Saves the data from a given experiment in Xepr to the specified path. If ``exp``
        is `None` the currently displayed data set is saved.

        Xepr only allows file paths shorter than 128 characters.

        :param str path: Absolute path to save data file. Must be shorter than 128
            characters and must comply with possibly other Xepr file name restrictions.
        :param exp: Xepr experiment instance associated with data set. Defaults to
            currently selected experiment if not given.
        :param str title: Name of the data set. Will be saved as a parameter in the DSC
            file. If not given, the basename of the path will be used.
        """

        self._check_for_xepr()

        path = os.path.expanduser(path)

        if len(path) > 128:
            raise ValueError('Only paths with with 128 characters or less are ' +
                             'allowed by Xepr.')

        directory, basename = os.path.split(path)

        if not title:
            title = os.path.splitext(basename)[0]

        # check if directory exists, create otherwise
        if not os.path.exists(directory):
            os.makedirs(directory)

        # switch viewpoint to experiment if given
        if exp is not None:
            exp_title = exp.aqGetExpName()
            time.sleep(self._wait)
            self.XeprCmds.aqExpSelect(1, exp_title)
            time.sleep(self._wait)

        # tell Xepr to save data
        self.XeprCmds.ddPath(path)
        time.sleep(self._wait)
        self.XeprCmds.vpSave('Current Primary', title,  path)
        time.sleep(self._wait)

    def _phase_at_limit(self, phase, phase_min, phase_max):

        assert phase_max > phase_min

        deg_step = 6.5  # approximate step of 1 deg

        if phase_min < phase < phase_max:
            return False
        else:
            # shift by 360° if maximum or minimum is encountered
            direction = int(phase <= phase_min) - int(phase >= phase_max)
            self.hidden['SignalPhase'].value = phase + direction*360*deg_step
            logger.info('Phase at limit, cycling by 360 deg.')
            time.sleep(4)
            return True

# ========================================================================================
# set up cryostat functions
# ========================================================================================

    @manager.queued_exec
    def setTemperature(self, target, wait_stable=True):
        """
        Sets the target temperature for the ESR900 cryostat and waits for it to stabilize
        within :attr:`temp_wait_time` with fluctuations below
        :attr:`temperature_tolerance`. Warns the user if this takes too long.

        :param float target: Target temperature in Kelvin.
        :param bool wait_stable: If ``True``, this function will wait until the
            temperature is stable before it returns. See :func:`waitTemperatureStable`
        """

        self._check_for_mercury()

        logger.info('Setting target temperature to {}K.'.format(target))

        # set temperature and wait to stabilize
        self.esr_temperature.loop_tset = target
        if wait_stable:
            self.waitTemperatureStable(target)

            # check if gas flow is too high for temperature set point
            # if yes, reduce minimum value until target is reached
            ht = self._heater_target(target)
            fmin = self.esr_gasflow.gmin

            above_heater_target = (self.esr_heater.volt[0] > 1.2*ht)
            flow_at_min = (self.esr_gasflow.perc[0] == fmin)

            if above_heater_target and flow_at_min:

                logger.warning('Gas flow is too high, trying to reduce.')
                self.esr_temperature.loop_faut = 'ON'
                self.esr_gasflow.gmin = max(fmin - 1, 1)

    @manager.queued_exec
    def setTemperatureRamp(self, ramp):
        """
        Sets the temperature ramp speed for the cryostat in K/min.

        :param float ramp: Ramp in Kelvin per minute.
        """

        self._check_for_mercury()

        # set temperature and wait to stabilize
        self.esr_temperature.loop_rset = ramp
        logger.info('Temperature ramp set to {} K/min.'.format(ramp))

    @manager.queued_exec
    def waitTemperatureStable(self, target):
        """
        Waits for the cryostat temperature to stabilize within the specified tolerance
        :attr:`temperature_tolerance`. Releases after it has been stable for
        :attr:`temp_wait_time` seconds (default of 120 sec).

        :param float target: Target temperature in Kelvin.
        """

        # time in sec after which a timeout warning is issued
        temperature_timeout = self._ramp_time(target) + 30*60  # in sec
        # counter for elapsed seconds since temperature has been stable
        stable_counter = 0
        # counter for temperature warnings
        temperature_warning_counter = 0
        # starting time
        t0 = time.time()

        logger.info('Waiting for temperature to stabilize.')

        while stable_counter < self._temp_wait_time:
            # check for abort command
            if self.abort.is_set():
                logger.info('Aborted by user.')
                return

            # check temperature deviation
            self.T_diff = abs(target - self.esr_temperature.temp[0])
            if self.T_diff > self._temperature_tolerance:
                stable_counter = 0
                time.sleep(1)
                logger.status('Waiting for temperature to stabilize.')
            else:
                stable_counter += 1
                logger.status('Stable for {}/{} sec.'.format(stable_counter,
                                                             self._temp_wait_time))
                time.sleep(1)

            # warn if stabilization is taking longer than expected
            if time.time() - t0 > temperature_timeout and temperature_warning_counter == 0:
                logger.warning('Temperature is taking a long time to stabilize.')
                t0 = time.time()
                temperature_timeout = self._ramp_time(target) + 30*60
                temperature_warning_counter += 1

        message = 'Mercury iTC: Temperature is stable at {}K.'.format(target)
        logger.info(message)

    @manager.queued_exec
    def getTemperature(self):
        """Returns the current temperature in Kelvin."""
        self._check_for_mercury()
        return self.esr_temperature.temp[0]

    @manager.queued_exec
    def getTemperatureSetpoint(self):
        """Returns the temperature setpoint in Kelvin."""
        self._check_for_mercury()
        return self.esr_temperature.loop_tset

    @staticmethod
    def _heater_target(temperature, htt_file=None):
        """
        Returns the ideal heater voltage for a given temperature. This function can be
        used to check the current gas flow: If the heater voltage exceeds its target
        value, the gas flow likely is too high (and vice versa).

        :func:`heater_target` accepts a file path ``htt_file`` to a custom heater target
        table file, used instead of the default values for the ESR900 cryostat. The file
        must contain comma-delimited pairs of temperature (in Kelvin) and heater target
        voltage (in Volts) with a new line for each pair.

        :param float temperature: Temperature in Kelvin.
        :param str htt_file: Path to file with custom heater target table.
        """
        if htt_file is None:
            htt_file = os.path.join(_root, 'experiment', 'mercury_htt.txt')

        htt = np.loadtxt(htt_file, delimiter=',')
        return np.interp(temperature, htt[:, 0], htt[:, 1])

    def _ramp_time(self, target):
        """
        Calculates the expected time in sec to reach the target temperature.
        Assumes a ramp speed of 5 K/min if 'ramp' is turned off.

        :param float target: Target temperature in Kelvin.
        """
        if self.esr_temperature.loop_rena == 'ON':
            expected_time = (abs(target - self.esr_temperature.temp[0]) /
                             self.esr_temperature.loop_rset)  # in min
        else:  # assume ramp of 5 K/min
            expected_time = abs(target - self.esr_temperature.temp[0]) / 5
        return expected_time * 60  # return value in sec

# ========================================================================================
# set up Keithley functions
# ========================================================================================

    @manager.queued_exec
    def transferMeasurement(self, smu_gate=KCONF.get('Sweep', 'gate'),
                            smu_drain=KCONF.get('Sweep', 'drain'),
                            vg_start=KCONF.get('Sweep', 'VgStart'),
                            vg_stop=KCONF.get('Sweep', 'VgStop'),
                            vg_step=KCONF.get('Sweep', 'VgStep'),
                            vd_list=KCONF.get('Sweep', 'VdList'),
                            t_int=KCONF.get('Sweep', 'tInt'),
                            delay=KCONF.get('Sweep', 'delay'),
                            pulsed=KCONF.get('Sweep', 'pulsed'),
                            path=None):
        """
        Records a transfer curve and returns the resulting data. If a valid path is path
        given, the data is also saved as a .txt file.

        :param smu_gate: Name of SMU attached to the gate electrode of an FET.
        :param smu_drain: Name of SMU attached to the drain electrode of an FET.
        :param float vg_start: Start voltage of transfer sweep in Volts.
        :param float vg_stop: End voltage of transfer sweep in Volts.
        :param float vg_step: Voltage step size for transfer sweep in Volts.
        :param list vd_list: List of drain voltage steps in Volts.
        :param float t_int: Integration time in sec for every data point.
        :param float delay: Settling time in sec before every measurement. Set to -1 for
            automatic delay.
        :param bool pulsed: True or False for pulsed or continuous measurements.
        :param str path: File path to save transfer curve data as .txt file.

        :returns: Transfer curve data.
        :rtype: :class:`keithley2600.TransistorSweepData`
        """

        self._check_for_keithley()

        smu_gate = getattr(self.keithley, smu_gate)
        smu_drain = getattr(self.keithley, smu_drain)

        sd = self.keithley.transferMeasurement(
            smu_gate, smu_drain, vg_start, vg_stop, vg_step, vd_list,
            t_int, delay, pulsed
        )

        if path is not None:
            sd.save(path)

        return sd

    @manager.queued_exec
    def outputMeasurement(self, smu_gate=KCONF.get('Sweep', 'gate'),
                          smu_drain=KCONF.get('Sweep', 'drain'),
                          vd_start=KCONF.get('Sweep', 'VdStart'),
                          vd_stop=KCONF.get('Sweep', 'VdStop'),
                          vd_step=KCONF.get('Sweep', 'VdStep'),
                          vg_list=KCONF.get('Sweep', 'VgList'),
                          t_int=KCONF.get('Sweep', 'tInt'),
                          delay=KCONF.get('Sweep', 'delay'),
                          pulsed=KCONF.get('Sweep', 'pulsed'),
                          path=None):
        """
        Records an output curve and returns the resulting data. If a valid path is given,
        the data is also saved as a .txt file.

        :param smu_gate: Name of SMU attached to the gate electrode of an FET.
        :param smu_drain: Name of SMU attached to the drain electrode of an FET.
        :param float vd_start: Start voltage of output sweep in Volts .
        :param float vd_stop: End voltage of output sweep in Volts.
        :param float vd_step: Voltage step size for output sweep in Volts.
        :param list vg_list: List of gate voltage steps in Volts.
        :param float t_int: Integration time in sec for every data point.
        :param float delay: Settling time in sec before every measurement. Set to -1 for
            automatic delay.
        :param bool pulsed: True or False for pulsed or continuous measurements.
        :param str path: File path to save output curve data as .txt file.

        :returns: Output curve data.
        :rtype: :class:`keithley2600.TransistorSweepData`
        """

        self._check_for_keithley()

        smu_gate = getattr(self.keithley, smu_gate)
        smu_drain = getattr(self.keithley, smu_drain)

        sd = self.keithley.outputMeasurement(
            smu_gate, smu_drain, vd_start, vd_stop,vd_step, vg_list,
            t_int, delay, pulsed
        )

        if path is not None:
            sd.save(path)

        return sd

    @manager.queued_exec
    def setVoltage(self, v, smu=KCONF.get('Sweep', 'gate')):
        """
        Sets the bias of the given Keithley SMU.

        :param float v: Gate voltage in Volts.
        :param str smu: Name of SMU. Defaults to the SMU saved as gate.
        """

        self._check_for_keithley()

        smu = getattr(self.keithley, smu)

        self.keithley.applyVoltage(smu, v)
        self.keithley.beeper.beep(0.3, 2400)

    @manager.queued_exec
    def setCurrent(self, i, smu=KCONF.get('Sweep', 'drain')):
        """
        Applies a specified current to the selected Keithley SMU.

        :param float i: Current in Ampere.
        :param str smu: Name of SMU. Defaults to the SMU saved as drain.
        """

        self._check_for_keithley()

        smu = getattr(self.keithley, smu)

        self.keithley.applyCurrent(smu, i)
        self.keithley.beeper.beep(0.3, 2400)

# ========================================================================================
# Helper methods
# ========================================================================================

    def _check_for_mercury(self, raise_error=True):
        """
        Checks if a MercuryITC is connect and correctly configured.
        """

        if not self.mercury:
            error_info = ('No Mercury instance supplied. Functions that ' +
                          'require a connected cryostat will not work.')
        elif not self.mercury.connected:
            error_info = ('MercuryiTC is not connected. Functions that ' +
                          'require a connected cryostat will not work.')
        else:
            temperature_module_name = CONF.get('CustomXepr', 'esr_temperature_nick')
            temp, gasflow, heater = self._select_temp_sensor(temperature_module_name)

            if not temp:
                error_info = ('MercuryiTC error: temperature sensor "{}" not '
                              'found.').format(temperature_module_name)
            elif not heater:
                error_info = ('MercuryiTC error: No heater module configured for "{}". '
                              'Functions that require a connected cryostat will not '
                              'work.').format(temperature_module_name)
            elif not gasflow:
                error_info = ('MercuryiTC error: No gas flow module configured for "{}". '
                              'Functions that require a connected cryostat will not '
                              'work.').format(temperature_module_name)
            else:
                error_info = False

        if error_info:
            if raise_error:
                raise RuntimeError(error_info)
            logger.info(error_info)
            return False
        else:
            return True

    def _check_for_keithley(self, raise_error=True):
        """
        Checks if a keithley instance has been passed and is connected to an an actual
        instrument.
        """

        if not self.keithley:
            error_info = ('No Keithley instance supplied. Functions that ' +
                          'require a connected Keithley SMU will not work.')
        elif not self.keithley.connected:
            error_info = ('Keithley is not connected. Functions that ' +
                          'require a connected Keithley will not work.')
        else:
            error_info = False

        if error_info:
            if raise_error:
                raise RuntimeError(error_info)
            logger.info(error_info)
            return False
        else:
            return True

    def _check_for_xepr(self, raise_error=True):
        if not self.xepr:
            error_info = ('No Xepr instance supplied. Functions that ' +
                          'require Xepr will not work.')
        elif not self.xepr.XeprActive():
            error_info = ('Xepr API not active. Please activate Xepr API by ' +
                          'pressing "Processing > XeprAPI > Enable Xepr API"')
        else:
            error_info = False
            self.XeprCmds = self.xepr.XeprCmds
            if not self.hidden:
                try:
                    self.hidden = self.xepr.XeprExperiment('AcqHidden')
                except Exception:
                    error_info = ('Xepr is not connected to the spectrometer. ' +
                                  'Please connect by pressing "Acquisition > ' +
                                  'Connect To Spectrometer..."')

        if error_info:
            if raise_error:
                raise RuntimeError(error_info)
            logger.info(error_info)
            return False
        else:
            return True

    def _select_temp_sensor(self, nick):

        # find all temperature modules
        temp_mods = [m for m in self.mercury.modules if type(m) == MercuryITC_TEMP]
        if len(temp_mods) == 0:
            raise IOError('MercuryITC does not have any connected temperature modules')

        # find the temperature module with given name
        temperature = next((m for m in temp_mods if m.nick == nick), None)

        if temperature:
            htr_nick = temperature.loop_htr
            aux_nick = temperature.loop_aux

            heater = next((m for m in self.mercury.modules if m.nick == htr_nick), None)
            gasflow = next((m for m in self.mercury.modules if m.nick == aux_nick), None)
        else:
            gasflow = None
            heater = None

        return temperature, gasflow, heater
