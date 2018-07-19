# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 20:19:05 2016

@author: Sam Schott (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""

# system imports
import visa
import logging
import threading


logger = logging.getLogger(__name__)


CONSTANTS = [
            'CAPACITY',
            'ARMED_EVENT_ID',
            'MEASURE_COMPLETE_EVENT_ID',
            'PULSE_COMPLETE_EVENT_ID',
            'SOURCE_COMPLETE_EVENT_ID',
            'SWEEP_COMPLETE_EVENT_ID',
            'SWEEPING_EVENT_ID',
            'IDLE_EVENT_ID',
            'EVENT_ID',
            ]

FUNCTIONS = [
            'beep',
            'bitand',
            'bitor',
            'bitxor',
            'clear',
            'get',
            'getfield',
            'set',
            'setfield',
            'test',
            'toggle',
            'clear',
            'clearcache',
            'add',
            'clear',
            'next',
            'delay',
            'readbit',
            'readport',
            'assert',
            'clear',
            'release',
            'reset',
            'wait',
            'writebit',
            'writeport',
            'clear',
            'getannunciators',
            'getcursor',
            'getlastkey',
            'gettext',
            'inputvalue',
            'add',
            'catalog',
            'delete',
            'menu',
            'prompt',
            'sendkey',
            'setcursor',
            'settext',
            'clear',
            'wait',
            'waitkey',
            'clear',
            'next',
            'all',
            'clear',
            'next',
            'exit',
            'chdir',
            'cwd',
            'is_dir',
            'is_file',
            'mkdir',
            'readdir',
            'rmdir',
            'gettimezone',
            'gm_isweep',
            'gm_vsweep',
            'i_leakage_measure',
            'i_leakage_threshold',
            'InitiatePulseTest',
            'InitiatePulseTestDual',
            'close',
            'flush',
            'input',
            'open',
            'output',
            'read',
            'type',
            'write',
            'applysettings',
            'reset',
            'restoredefaults',
            'assert',
            'clear',
            'connect',
            'disconnect',
            'wait',
            'reset',
            'makegetter',
            'makesetter',
            'meminfo',
            'execute',
            'getglobal',
            'setglobal',
            'opc',
            'remove',
            'rename',
            'print',
            'printbuffer',
            'printnumber',
            'QueryPulseConfig',
            'reset',
            'savebuffer',
            'delete',
            'catalog',
            'load',
            'new',
            'newautorun',
            'restore',
            'run',
            'catalog',
            'list',
            'run',
            'save',
            'read',
            'write',
            'settime',
            'settimezone',
            'recall',
            'save',
            'abort',
            'getstats',
            'recalculatestats',
            'lock',
            'restore',
            'save',
            'unlock',
            'calibratehi',
            'calibratelo',
            'check',
            'r',
            'makebuffer',
            'calibrateY',
            'overlappedY',
            'Y',
            'measureYandstep',
            'reset',
            'savebuffer',
            'calibrateY',
            'set',
            'set',
            'initiate',
            'set',
            'Y',
            'linearY',
            'listY',
            'logY',
            'set',
            'reset',
            'SweepILinMeasureV',
            'SweepIListMeasureV',
            'SweepILogMeasureV',
            'SweepVLinMeasureI',
            'SweepVListMeasureI',
            'SweepVLogMeasureI',
            't',
            'reset',
            'clear',
            'reset',
            'wait',
            'clear',
            'clear',
            'reset',
            'wait',
            'wait',
            'readbit',
            'readport',
            'reset',
            'assert',
            'clear',
            'release',
            'reset',
            'wait',
            'writebit',
            'writeport',
            'clear',
            'connect',
            'disconnect',
            'execute',
            'idn',
            'read',
            'readavailable',
            'reset',
            'termination',
            'abort',
            'rbtablecopy',
            'runscript',
            'write',
            'add',
            'catalog',
            'delete',
            'get',
            'waitcomplete',
            'delete',
            'get',
            'waitcomplete',
            'v',
            'iv',
            'r',
            'p',
            ]

PROPERTIES = [
            'enable',
            'appendmode',
            'basetimestamp',
            'cachemode',
            'capacity',
            'collectsourcevalues',
            'collecttimestamps',
            'fillcount',
            'fillmode',
            'measurefunctions',
            'measureranges',
            'n',
            'readings',
            'sourcefunctions',
            'sourceoutputstates',
            'sourceranges',
            'sourcevalues',
            'statuses',
            'timestampresolution',
            'timestamps',
            'count',
            'mode',
            'overrun',
            'pulsewidth',
            'stimulus',
            'writeprotect',
            'locallockout',
            'numpad',
            'screen',
            'digits',
            'func',
            'func',
            'overrun',
            'count',
            'count',
            'enable',
            'overwritemethod',
            'asciiprecision',
            'byteorder',
            'data',
            'address',
            'autoconnect',
            'address[N]',
            'domain',
            'dynamic',
            'hostname',
            'verify',
            'duplex',
            'gateway',
            'ipaddress',
            'method',
            'speed',
            'subnetmask',
            'linktimeout',
            'lxidomain',
            'nagle',
            'address[N]',
            'name',
            'duplex',
            'gateway',
            'ipaddress',
            'macaddress',
            'dst',
            'rawsocket',
            'telnet',
            'vxi11',
            'speed',
            'subnetmask',
            'timedwait',
            'connected',
            'ipaddress',
            'mode',
            'overrun',
            'protocol',
            'pseudostate',
            'stimulus',
            'autolinefreq',
            'description',
            'linefreq',
            'model',
            'password',
            'passwordmode',
            'prompts',
            'prompts4882',
            'revision',
            'serialno',
            'showerrors',
            'anonymous',
            'autorun',
            'name',
            'source',
            'baud',
            'databits',
            'flowcontrol',
            'parity',
            'poweron',
            'adjustdate',
            'date',
            'due',
            'password',
            'polarity',
            'state',
            'speed',
            'threshold',
            'analogfilter',
            'autorangeY',
            'autozero',
            'count',
            'delay',
            'delayfactor',
            'count',
            'enable',
            'type',
            'highcrangedelayfactor',
            'interval',
            'lowrangeY',
            'nplc',
            'rangeY',
            'enableY',
            'levelY',
            'nvbufferY',
            'sense',
            'autorangeY',
            'compliance',
            'delay',
            'func',
            'highc',
            'levelY',
            'limitY',
            'lowrangeY',
            'offfunc',
            'offlimitY',
            'offmode',
            'output',
            'outputenableaction',
            'rangeY',
            'settling',
            'sink',
            'count',
            'stimulus',
            'autoclear',
            'count',
            'action',
            'stimulus',
            'action',
            'action',
            'stimulus',
            'action',
            'limitY',
            'stimulus',
            'condition',
            'node_enable',
            'node_event',
            'request_enable',
            'request_event',
            'orenable',
            'overrun',
            'stimulus[M]',
            'count',
            'delay',
            'delaylist',
            'overrun',
            'passthrough',
            'stimulus',
            'group',
            'master',
            'node',
            'state',
            'mode',
            'overrun',
            'pulsewidth',
            'stimulus',
            'writeprotect',
            'timeout',
            'abortonconnect',
            'condition',
            'enable',
            'event',
            'ntr',
            'ptr',
            ]


class MagicConstant(object):

    def __init__(self, name, parent):
        if type(name) is not str:
            raise ValueError('First argument must be of type str.')
        self._name = name
        self._parent = parent

    def __get__(self, instance, owner=None):
        return self._parent._query(self._name)

    def __set__(self, instance, value):
        print('%s is read only' % self._name)
        return None

    def __delete__(self):
        del self


class MagicProperty(object):

    def __init__(self, name, parent=None):
        if type(name) is not str:
            raise ValueError('First argument must be of type str.')
        self._name = name
        self._parent = parent
        self.value = None

    def __getattr__(self, attr):
        try:
            # check if attr already exists
            return self.__dict__[attr]
        except (AttributeError, KeyError):
            # handle if not
            return self.__get_global_handler(attr)

    def __get_global_handler(self, name):
        self._parent._query(self._name)

    def __set__(self, instance, value):
        if isinstance(value, str):
            instance._write('%s = "%s"' % (self._name, value))
        else:
            instance._write('%s = %s' % (self._name, value))

    def __delete__(self):
        del self


class MagicFunction(object):

    def __init__(self, name, parent):
        if type(name) is not str:
            raise ValueError('First argument must be of type str.')
        self._name = name
        self._parent = parent

    def __call__(self, *args, **kwargs):
        # Pass on to calls to self._write, store result in variable.
        # Querying results from function calls directly may result in
        # a VisaIOError timeout if the function does not return anything.
        args_string = str(args).strip("()").strip(",").strip("'")
        self._parent._write('result = %s(%s)' % (self._name, args_string))
        # query for result in second call
        return self._parent._query('result')


class MagicClass(object):

    _name = ''
    _parent = None
    __dict__ = {'_name': _name}

    def __init__(self, name, parent=None):
        if type(name) is not str:
            raise ValueError('First argument must be of type str.')
        self._name = name
        self._parent = parent

    def __getattr__(self, attr):
        try:
            # check if attr already exists
            return self.__dict__[attr]
        except (AttributeError, KeyError):
            # handle if not
            return self.__get_global_handler(attr)

    def __get_global_handler(self, name):
        # create callable sub-class for new attr
        new_name = '%s.%s' % (self._name, name)
        if name in CONSTANTS:
            handler = MagicConstant(new_name, parent=self)
            self.__dict__[name] = handler

        elif name in FUNCTIONS:
            handler = MagicFunction(new_name, parent=self)
            self.__dict__[name] = handler

        elif name in PROPERTIES:
            handler = self._parent._query(new_name)
        else:
            handler = MagicClass(new_name, parent=self)
            self.__dict__[name] = handler

        return handler

    def __setattr__(self, attr, value):
        if attr in PROPERTIES and isinstance(value, str):
            self._parent._write('%s.%s = "%s"' % (self._name, attr, value))
        elif attr in PROPERTIES:
            self._parent._write('%s.%s = %s' % (self._name, attr, value))
        else:
            object.__setattr__(self, attr, value)

    def _write(self, value):
        try:
            self._parent._write(value)
        except AttributeError:
            print(value)

    def _query(self, value):
        try:
            return self._parent._query(value)
        except AttributeError:
            print('print(%s)' % value)
            return None

    def __getitem__(self, i):
        new_name = '%s[%s]' % (self._name, i)
        new_class = MagicClass(new_name, parent=self)
        return new_class

    def __iter__(self):
        return self

    def getdoc():
        pass


class Keithley2600(MagicClass):
    """

    Keithley driver to perform base functions. It copies the functionality and
    syntax from the Keithley TSP functions, which have a syntax similar to
    python.

    WARNING:
        There are currntly no checks of allowed values implemented. This driver
        will only now if an accessed attribute is a keithley property, function
        or constant. It will NOT check the validity of input arguments.
        Invalid commands will typically raise a VisaIOError timeout error.

    USAGE:
        keithley = Keithley2600()
        keithley.beeper.beep(1, 2400)  # beeps for 1 sec @ 2400 Hz
        keithley.smua.trigger.source.limiti = 0.1  # sets limit to 0.1 A

    DOCUMENTATION:
        See the Keithley 2600 reference manual for all available commands and
        arguments. All remotely accessible commands can be used with this
        driver.

    """

    _lock = threading.RLock()

    OUTPUT_OFF = 0
    OUTPUT_ON = 1
    OUTPUT_HIGH_Z = 2

    MEASURE_DCAMPS = 0
    MEASURE_DCVOLTS = 1
    MEASURE_OHMS = 2
    MEASURE_WATTS = 3

    DISABLE = 0
    ENABLE = 1

    SENSE_LOCAL = 0
    SENSE_REMOTE = 1
    SENSE_CALA = 3

    SMUA_BUFFER1 = 'smua.nvbuffer1'
    SMUA_BUFFER2 = 'smua.nvbuffer2'
    SMUB_BUFFER1 = 'smub.nvbuffer1'
    SMUB_BUFFER2 = 'smub.nvbuffer2'

    SOURCE_IDLE = 0
    SOURCE_HOLD = 1

    AUTORANGE_OFF = 0
    AUTORANGE_ON = 1
    AUTORANGE_FOLLOW_LIMIT = 2

# =============================================================================
# Connect to keithley
# =============================================================================

    def __init__(self, address):
        super(self.__class__, self).__init__()
        # open Keithley Visa resource
        self.address = address
        self.rm = visa.ResourceManager()
        self.connect()

        self._parent = self
        self._name = 'keithley'

    def connect(self, read_term='\n', bdrate=57600):
        """
        Connects to Keithley and opens pyvisa API.
        """
        try:
            visaAddress = 'TCPIP0::%s::INSTR' % self.address
            self.connection = self.rm.open_resource(visaAddress)
            self.connection.read_termination = read_term
            self.connection.baud_rate = bdrate
        except OSError:
            logger.warning('NI Visa is not installed.')
            self.connection = None
            return

    def disconnect(self):
        """ Disconnect from Keithley """
        try:
            self.connection.close()
            del self.connection
        except AttributeError:
            pass

# =============================================================================
# Define I/O
# =============================================================================

    def _write(self, text):
        """
        Writes text to Keithley.
        """
        self.connection.write(text)

    def _query(self, text):
        """
        Queries and expects response from Keithley.
        """
        with self._lock:
            r = self.connection.query('print(%s)' % text)
            self.connection.clear()

        return self.parse_response(r)

    def parse_response(self, string):
        try:
            r = float(string)
        except ValueError:
            pass

        if string == 'nil':
            r = None
        elif string == 'True':
            r = True
        elif string == 'False':
            r = False

        return r
