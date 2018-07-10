# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 11:48:07 2014

@author: florian

A driver to read and set the Oxford MercuryITC with its modules. Only the USB
connection is supported. Note that this connection is technically just a
serial connection, so the appropriate interface is the serial interface.

This driver supports the aux, heater and temperature modules. Look
at the class docstrings to see all the implemented features (which is almost
all).

The core of this module is the class MercuryITC. To initialize a driver object,
just create an instance of this class with the device's address, e. g.

>> m = MercuryITC('/dev/ttyACM0')

All the instrument attributes can be accessed through instance attributes, e.g.

>> print m.serl

All MercuryITC modules are automatically recognized and added to the modules
attribute:

>> print(m.modules)

Values can be read from and written to the instrument in the same way as for
main models.

>> htr = m.modules[0]
>> print(htr.nick)
>> htr.nick = 'Main heater'
>> print(htr.nick)

There exists a special kind of attributes called *signals* in the MercuryITC
manual. These contain a numeric value as well as a unit. Signals are read
and set as tuples, e.g.

>> print(htr.volt)
>> htr.volt = (2.5, 'V')
>> print(htr.volt)

Note that all attributes which are not *signals* are cached and retrieved only
once from the device. They are stored in memory and only read from memory
afterwards. To remove these variables from memory for whatever reason, simply
call the destructor:

>> del m.serl

It's also possible to empty the entire cache of an object by calling the
clear_cache method:

>> m.clear_cache()

-----

To fix:

MercuryITC: USER and PASS property not implemented
MercuryITC_HTR: POWR not implemented correctly

----

Modified by Sam Schott, 08/08/2016

"""

import visa
import threading


def convert_scaled_values(s, convert=float):
    """Split the value from any other part of a string, i. e. the units, and
    return the a tuple of the value and the extracted unit. Also converts the
    value by the given function."""
    f = filter(lambda x: x in '0123456789.', s)
    try:
        unit = s.split(f)[-1]
    except ValueError:
        unit = 'a.u.'
    return convert(f), unit


class CachedPropertyContainer(object):
    def __init__(self):
        self.clear_cache()

    def _read_property(self, name, convert, ignored_delimiters=0):
        """Read a property from the device.
        name (str): property's name
        convert (factory func): function to convert the str received from the
            instrument; usually float, int or str
        ignored_delimiters (int): Amount of : which belongs to the property's
            value. Only makes sense for str values.
        """
        q = 'READ:%s:%s' % (self.address, name)
        resp = self.query(q)
        delimiters = resp.count(':')
        value = resp.split(':', delimiters-ignored_delimiters)[-1]
        prop = convert(value)
        return prop

    def _write_property(self, name, value, convert):
        if convert == float:
            value_str = '%f' % value
        elif convert == int:
            value_str = '%i' % value
        else:
            value_str = value

        q = 'SET:%s:%s:%s' % (self.address, name, value_str)
        resp = self.query(q).split(':')
        if resp[-1] != 'VALID':
            print(resp)
            raise ValueError(q)
        else:
            return convert(resp[-2])

    def _read_cached_property(self, name, convert, ignored_delimiters=0):
        """Read a cached property from the device.
        name (str): property's name
        convert (factory func): function to convert the str received from the
            instrument; usually float, int or str
        ignored_delimiters (int): Amount of *:* which belongs to the property's
            value. Only makes sense for str values.
        """
        try:
            return self._cache[name]
        except KeyError:
            prop = self._read_property(name, convert, ignored_delimiters)
            self._cache[name] = prop
            return prop

    def _write_cached_property(self, name, value, convert):
        if self._cache[name] is not value:
            cache_value = self._write_property(name, value, convert)
            self._cache[name] = cache_value

    def _delete_cached_property(self, name):
        try:
            self._cache.pop(name)
        except KeyError:
            pass

    def clear_cache(self):
        self._cache = {}

    def query(self):
        pass


class MercuryCommon(CachedPropertyContainer):
    """Contains properties which are common for all MercuryITC devices."""
    @property
    def hver(self):
        """Hardware version - Read only - version number"""
        return self._read_cached_property('MAN:HVER', str)

    @hver.deleter
    def hver(self):
        self._delete_cached_property('MAN:HVER')

    @property
    def fver(self):
        """Firmware version - Read only - version number"""
        return self._read_cached_property('MAN:FVER', str)

    @fver.deleter
    def fver(self):
        self._delete_cached_property('MAN:FVER')

    @property
    def serl(self):
        """Serial number - Read only - alphanumeric"""
        return self._read_cached_property('MAN:SERL', str)

    @serl.deleter
    def serl(self):
        self._delete_cached_property('MAN:SERL')


class MercuryModule(MercuryCommon):
    """Base class for a MercuryITC module."""
    def __init__(self, address, parent):
        super(MercuryModule, self).__init__()
        self.address = address
        self.parent = parent
        self._cache = {}

    def __repr__(self):
        return '%s(%s, %s)' % (type(self).__name__, self.nick, self.parent)

    def read(self):
        return self.parent.read()

    def write(self, q):
        self.parent.write(q)

    def query(self, q):
        return self.parent.query(q)

    @property
    def nick(self):
        """Nickname - Read/set - alphanumeric"""
        return self._read_cached_property('NICK', str)

    @nick.setter
    def nick(self, val):
        self._write_cached_property('NICK', val, str)

    @nick.deleter
    def nick(self):
        self._delete_cached_property('NICK')


class MercuryITC_HTR(MercuryModule):
    def __init__(self, address, parent):
        super(MercuryITC_HTR, self).__init__(address, parent)

    @property
    def pmax(self):
        """Maximum power supported - Read only - Float value"""
        return self._read_cached_property('PMAX', float)

    @pmax.deleter
    def pmax(self):
        self._delete_cached_property('PMAX')

    @property
    def res(self):
        """Nominal resistance - Read/set Float value - [20.00 to 100.00]"""
        return self._read_cached_property('RES', float)

    @res.setter
    def res(self, val):
        if val > 100 or val < 20:
            raise ValueError('Only values between 20.0 and 100.0 allowed')
        else:
            self._write_cached_property('RES', val, float)

    @res.deleter
    def res(self):
        self._delete_cached_property('RES')

    @property
    def vlim(self):
        """Voltage limit - Read/set - Float value [0.0 to 40.00]"""
        return self._read_cached_property('VLIM', float)

    @vlim.setter
    def vlim(self, val):
        if val > 40 or val < 0:
            raise ValueError('Only values between 0.0 and 40.0 allowed')
        else:
            self._write_cached_property('VLIM', val, float)

    @vlim.deleter
    def vlim(self):
        self._delete_cached_property('VLIM')

    @property
    def volt(self):
        """Most recent voltage reading/voltage to set - Read/set Float value
        [0.0 to VLIM]"""
        return convert_scaled_values(self._read_property('SIG:VOLT', str))

    @volt.setter
    def volt(self, val):
        if val[0] > self.vlim or val[0] < 0:
            raise ValueError('Only values from 0 to %s allowed.' % self.vlim)
        else:
            val = [str(v) for v in val]
            self._write_property('SIG:VOLT', ''.join(val), str)

    @property
    def curr(self):
        """Most recent current reading - Read only - Float value"""
        return convert_scaled_values(self._read_property('SIG:CURR', str))

    # TODO: Check this in action and provide a proper fix
    # In a dry environment, powr is 'N/A'.
    @property
    def powr(self):
        """Most recent power reading/ power to set - Read/set - Float value
        [0.0 to Max Power]"""
        return self._read_property('SIG:PWR', str)

    @powr.setter
    def powr(self, val):
        if val > self.pmax or val < 0:
            raise ValueError('Only values from 0 to %s allowed' % self.pmax)
        else:
            self._write_property('SIG:PWR', val, str)


class MercuryITC_TEMP(MercuryModule):
    """Class for an MercuryITC temperature sensor module without the
        temperature control loop settings."""
    TYPES = ['PTC', 'NTC', 'DDE', 'TCE']
    EXCT_TYPES = ['UNIP', 'BIP', 'SOFT']
    CAL_INT = ['LIN', 'SPL', 'LAGR']

    @property
    def type(self):
        """[PTC | NTC | DDE | TCE] - Read/set - Enumerated set"""
        return self._read_cached_property('TYPE', str)

    @type.setter
    def type(self, val):
        if val not in self.TYPES:
            raise ValueError('Only values from %s allowed' % self.TYPES)
        else:
            self._write_cached_property('TYPE', val, str)

    @type.deleter
    def type(self):
        self._delete_cached_property('TYPE')

    @property
    def exct_type(self):
        """Excitation type [UNIP | BIP | SOFT] - Read/set - Enumerated set"""
        return self._read_cached_property('EXCT:TYPE', str)

    @exct_type.setter
    def exct_type(self, val):
        if val not in self.TYPES:
            raise ValueError('Only values from %s allowed' % self.EXCT_TYPES)
        else:
            self._write_cached_property('EXCT:TYPE', val, str)

    @exct_type.deleter
    def exct_type(self):
        self._delete_cached_property('EXCT:TYPE')

    @property
    def exct_mag(self):
        """Excitation magnitude - Read/set - Float value followed by a scale"""
        return self._read_cached_property('EXCT:MAG', str)

    @exct_mag.setter
    def exct_mag(self, val):
        # TODO: Add proper value checking
        if False:
            raise ValueError()
        else:
            self._write_cached_property('EXCT:MAG', val, str)

    @exct_mag.deleter
    def exct_mag(self):
        self._delete_cached_property('EXCT:MAG')

    @property
    def cal_file(self):
        """Calibration file name - Read/set - Filename"""
        return self._read_cached_property('CAL:FILE', str)

    @cal_file.setter
    def cal_file(self, val):
        # TODO: Add proper value checking
        if False:
            raise ValueError()
        else:
            self._write_cached_property('CAL:FILE', val, str)

    @cal_file.deleter
    def cal_file(self):
        self._delete_cached_property('CAL:FILE')

    @property
    def cal_int(self):
        """Interpolation type [LIN | SPL | LAGR] - Read/set - Enumerated set"""
        return self._read_cached_property('CAL:INT', str)

    @cal_int.setter
    def cal_int(self, val):
        if val not in self.CAL_INT:
            raise ValueError('Only values from %s allowed' % self.CAL_INT)
        else:
            self._write_cached_property('CAL:INT', val, str)

    @cal_int.deleter
    def cal_int(self):
        self._delete_cached_property('CAL:INT')

    @property
    def cal_scal(self):
        """Scaling factor - Read/set - Float value [0.5 to 1.5]"""
        return self._read_cached_property('CAL:SCAL', float)

    @cal_scal.setter
    def cal_scal(self, val):
        if val > 1.5 or val < 0.5:
            raise ValueError('Only values between 0.5 and 1.5 allowed')
        else:
            self._write_cached_property('CAL:SCAL', val, float)

    @cal_scal.deleter
    def cal_scal(self):
        self._delete_cached_property('CAL:SCAL')

    @property
    def cal_offs(self):
        """Offset value - Read/set - Float value [-100.0 to 100.0]"""
        return self._read_cached_property('CAL:OFFS', float)

    @cal_offs.setter
    def cal_offs(self, val):
        if val > 100 or val < -100:
            raise ValueError('Only values between -100.0 and 100.0 allowed')
        else:
            self._write_cached_property('CAL:OFFS', val, float)

    @cal_offs.deleter
    def cal_offs(self):
        self._delete_cached_property('CAL:OFFS')

    @property
    def cal_hotl(self):
        """Hot limit - Read only - Float value"""
        return self._read_cached_property('CAL:HOTL', str)

    @cal_hotl.deleter
    def cal_hotl(self):
        self._delete_cached_property('CAL:HOTL')

    @property
    def cal_coldl(self):
        """Cold limit - Read only - Float value"""
        return self._read_cached_property('CAL:COLDL', str)

    @cal_coldl.deleter
    def cal_coldl(self):
        self._delete_cached_property('CAL:COLDL')

    @property
    def volt(self):
        """Most recent voltage reading - Read only - Float value"""
        return convert_scaled_values(self._read_property('SIG:VOLT', str))

    @property
    def res(self):
        """Most recent resistance reading - Read only - Float value"""
        return convert_scaled_values(self._read_property('SIG:RES', str))

    @property
    def temp(self):
        """Most recent temperature reading - Read only - Float value"""
        return convert_scaled_values(self._read_property('SIG:TEMP', str))

    @property
    def slop(self):
        """Temperature sensitivity - Read only - Float value"""
        return convert_scaled_values(self._read_property('SIG:SLOP', str))


class MercuryITC_LOOP(MercuryModule):
    """Class for an MercuryITC temperature sensor module containing only the
        temperature control loop settings."""
    nick = 'LOOP'

    @property
    def pid_p(self):
        """Proportional gain - Read/set - Float value"""
        return self._read_cached_property('P', float)

    @pid_p.setter
    def pid_p(self, val):
        self._write_cached_property('P', val, float)

    @pid_p.deleter
    def pid_p(self):
        self._delete_cached_property('P')

    @property
    def pid_i(self):
        """Integral gain - Read/set - Float value"""
        return self._read_cached_property('I', float)

    @pid_i.setter
    def pid_i(self, val):
        self._write_cached_property('I', val, float)

    @pid_i.deleter
    def pid_i(self):
        self._delete_cached_property('I')

    @property
    def pid_d(self):
        """Differential gain - Read/set - Float value"""
        return self._read_cached_property('D', float)

    @pid_d.setter
    def pid_d(self, val):
        self._write_cached_property('D', val, float)

    @pid_d.deleter
    def pid_d(self):
        self._delete_cached_property('D')

    @property
    def pid_table(self):
        """Automatic PID values from table - Read/set - String value"""
        return self._read_cached_property('PIDT', str)

    @pid_table.setter
    def pid_table(self, val):
        if val == 'ON' or val == 'OFF':
            self._write_cached_property('PIDT', val, str)
        else:
            raise ValueError('Only values "ON" or "OFF" allowed')

    @pid_table.deleter
    def pid_table(self):
        self._delete_cached_property('PIDT')

    @property
    def heater_auto(self):
        """
        Enables or disables PID control of heater - Read/set - Float value
        """
        return self._read_cached_property('ENAB', str)

    @heater_auto.setter
    def heater_auto(self, val):
        if val == 'ON' or val == 'OFF':
            self._write_cached_property('ENAB', val, str)
        else:
            raise ValueError('Only values "ON" or "OFF" allowed')

    @heater_auto.deleter
    def heater_auto(self):
        self._delete_cached_property('ENAB')

    @property
    def flow_auto(self):
        """Enables or disables automatic gas flow - Read/set - String value"""
        return self._read_cached_property('FAUT', str)

    @flow_auto.setter
    def flow_auto(self, val):
        if val == 'ON' or val == 'OFF':
            self._write_cached_property('FAUT', val, str)
        else:
            raise ValueError('Only values "ON" or "OFF" allowed')

    @flow_auto.deleter
    def flow_auto(self):
        self._delete_cached_property('FAUT')

    @property
    def t_setpoint(self):
        """Temperature setpoint for PID loop - Read/set - Float value"""
        resp = convert_scaled_values(self._read_property('TSET', str))
        return resp[0]

    @t_setpoint.setter
    def t_setpoint(self, val):
        if val > 310 or val < 3:
            raise ValueError('Only values between 3K and 310K allowed')
        else:
            self._write_property('TSET', val, float)

    @property
    def flow(self):
        """Gas flow in percent - Read/set - Float value"""
        return self._read_property('FSET', float)

    @flow.setter
    def flow(self, val):
        if val > 100 or val < 0:
            raise ValueError('Only values between 0 and 100 allowed')
        else:
            self._write_property('FSET', val, float)

    @property
    def heater(self):
        """Heater power in percent of total - Read/set - Float value"""
        return self._read_property('HSET', float)

    @heater.setter
    def heater(self, val):
        if val > 100 or val < 0:
            raise ValueError('Only values between 0 and 100 allowed')
        else:
            self._write_property('HSET', val, float)

    @property
    def ramp(self):
        """Temperature ramp speed in K/min - Read/set - String value"""
        resp = self._read_cached_property('RSET', str)
        if resp == 'infK/m':
            return 'inf'
        else:
            tmp = convert_scaled_values(resp)
            return tmp[0]

    @ramp.setter
    def ramp(self, val):
        self._write_cached_property('RSET', val, str)

    @ramp.deleter
    def ramp(self):
        self._delete_cached_property('RSET')

    @property
    def ramp_enable(self):
        """Enables or disables temperature ramp - Read/set - String value"""
        return self._read_cached_property('RENA', str)

    @ramp_enable.setter
    def ramp_enable(self, val):
        if val in ('ON', 'OFF'):
            val = [str(v) for v in val]
            self._write_cached_property('RENA', ''.join(val), str)
        else:
            raise ValueError('Only values "ON" or "OFF" allowed')

    @ramp_enable.deleter
    def ramp_enable(self):
        self._delete_cached_property('RENA')

    @property
    def flow_auto(self):
        """
        Enables or disables automatic gas flow regulation - Read/set -
        String value
        """
        return self._read_cached_property('FAUT', str)

    @flow_auto.setter
    def flow_auto(self, val):
        if val in ('ON', 'OFF'):
            self._write_cached_property('FAUT', val, str)
        else:
            raise ValueError('Only values "ON" or "OFF" allowed')

    @flow_auto.deleter
    def flow_auto(self):
        self._delete_cached_property('FAUT')


class MercuryITC_AUX(MercuryModule):
    """Class for an MercuryITC AUX (gas flow) module."""
    @property
    def gmin(self):
        """Minimum gas flow setting - Read/set - float value > 20"""
        return self._read_cached_property('GMIN', float)

    @gmin.setter
    def gmin(self, val):
        if val < 1:
            raise ValueError('Only values larger than 1% allowed')
        else:
            self._write_cached_property('GMIN', val, float)

    @gmin.deleter
    def gmin(self):
        self._delete_cached_property('GMIN')

    @property
    def gfsf(self):
        """Gas flow scaling factor - Read/set - float value (0.0 to 99.0)"""
        return self._read_cached_property('GFSF', float)

    @gfsf.setter
    def gfsf(self, val):
        if val > 99 or val < 0:
            raise ValueError('Only values between 0.0 and 99.0 allowed')
        else:
            self._write_cached_property('GFSF', val, float)

    @gfsf.deleter
    def gfsf(self):
        self._delete_cached_property('GFSF')

    @property
    def tes(self):
        """Temperature error sensitivity - Read/set -
        float value (0.0 to 20.0)"""
        return self._read_cached_property('TES', float)

    @tes.setter
    def tes(self, val):
        if val > 20 or val < 0:
            raise ValueError('Only values between 0.0 and 20.0 allowed')
        else:
            self._write_cached_property('TES', val, float)

    @tes.deleter
    def tes(self):
        self._delete_cached_property('TES')

    @property
    def tves(self):
        """Temperature voltage error sensitivity - Read/set -
        float value (0.0 to 20.0)"""
        return self._read_cached_property('TVES', float)

    @tves.setter
    def tves(self, val):
        if val > 20 or val < 0:
            raise ValueError('Only values between 0.0 and 20.0 allowed')
        else:
            self._write_cached_property('TVES', val, float)

    @tves.deleter
    def tves(self):
        self._delete_cached_property('TVES')

    @property
    def gear(self):
        """Valve gearing - Read/set - unsigned integer (0 to 7)"""
        return self._read_cached_property('GEAR', int)

    @gear.setter
    def gear(self, val):
        if val > 7 or val < 0:
            raise ValueError('Only values between 0 and 7 allowed')
        else:
            self._write_cached_property('GEAR', val, int)

    @gear.deleter
    def gear(self):
        self._delete_cached_property('GEAR')

    @property
    def spd(self):
        """Stepper speed - Read/set - unsigned integer (0=slow, 1=fast)"""
        return self._read_cached_property('SPD', int)

    @spd.setter
    def spd(self, val):
        if val not in (0, 1):
            raise ValueError('Only 0 (slow) and 1 (fast) allowed')
        else:
            self._write_cached_property('SPD', val, int)

    @spd.deleter
    def spd(self):
        self._delete_cached_property('SPD')

    @property
    def step(self):
        """Present position of the stepper motor - Read only -
        unsigned integer (0.0 to Max Steps)"""
        return convert_scaled_values(self._read_property('SIG:STEP', str))

    @property
    def perc(self):
        """Percentage open - Read only - float value (0.0 to 100.0)"""
        return convert_scaled_values(self._read_property('SIG:PERC', str))

    @property
    def in_(self):
        """Input state - Read only - string"""
        return convert_scaled_values(self._read_property('SIG:IN', str))


class MercuryITC(MercuryCommon):
    """The main driver for the MercuryITC device. It contains all modules in
    the instance variable *modules*.
    Pass the address and port of the device as arguments.
    """
    USERS = ['NORM', 'ENG']
    DIMAS = ['ON', 'OFF']
    _lock = threading.RLock()

    def __init__(self, IP, port='7020'):
        super(MercuryITC, self).__init__()
        self.IP = IP
        self.port = port
        self.rm = visa.ResourceManager()
        self.connect()
        self._init_modules()
        self.address = 'SYS'

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.IP)

    def connect(self):
        self.connection = self.rm.open_resource('TCPIP0::%s::%s::SOCKET'
                                                % (self.IP, self.port))
        self.connection.read_termination = '\n'

    def disconnect(self):
        try:
            self.connection.close()
            del self.connection
        except AttributeError:
            pass

    def _init_modules(self):
        self.modules = []
        modules = self.cat.split(':DEV:')[1:]
        for module in modules:
            cls = module.split(':')[1]
            address = 'DEV:%s' % module
            if cls == 'TEMP':
                self.modules.append(MercuryITC_TEMP(address, self))
                loop_address = address + ':LOOP'
                self.modules.append(MercuryITC_LOOP(loop_address, self))
            elif cls == 'AUX':
                self.modules.append(MercuryITC_AUX(address, self))
            elif cls == 'HTR':
                self.modules.append(MercuryITC_HTR(address, self))

    def write(self, q):
        self.connection.write(q)

    def read(self):
        value = self.connection.read()
        return value

    def query(self, q):
        with self._lock:
            r = self.connection.query('%s' % q)
            self.connection.clear()
        return r

    @property
    def cat(self):
        """catalogue - Read only"""
        return self.query('READ:SYS:CAT')

    @property
    def rst(self):
        """reset the system - Set"""
        return False

    @rst.setter
    def rst(self, val):
        if val:
            q = 'SET:SYS:RST'
            resp = self.query(q).split(':')
        if resp[-1] != 'VALID':
            raise ValueError(q)

    @property
    def flsh(self):
        """amount of free space in flash memory - Read only -
        free space in kByte"""
        return self._read_cached_property('FLSH', float)

    # TODO: Fix code below for engineering mode, needs password
    """
    @property
    def user(self):
        return self._read_cached_property('USER', str)

    @user.setter
    def user(self, val):
        if val not in self.USERS:
            raise ValueError('Only values from %s allowed' % self.USERS)
        else:
            self._write_cached_property('USER', val, str)

    @user.deleter
    def user(self):
        self._delete_cached_property('USER')
    """

    @property
    def dima(self):
        """auto dim on/off - Read/Set - OFF, ON"""
        return self._read_cached_property('DISP:DIMA', str)

    @dima.setter
    def dima(self, val):
        if val not in self.DIMAS:
            raise ValueError('Only values from %s allowed' % self.DIMAS)
        else:
            self._write_cached_property('DISP:DIMA', val, str)

    @dima.deleter
    def dima(self):
        self._delete_cached_property('DISP:DIMA')

    @property
    def dimt(self):
        """auto dim time - Read/Set - seconds"""
        return self._read_cached_property('DISP:DIMT', int)

    @dimt.setter
    def dimt(self, val):
        if val < 0:
            raise ValueError('Only values positive values allowed')
        else:
            self._write_cached_property('DISP:DIMT', val, int)

    @dimt.deleter
    def dimt(self):
        self._delete_cached_property('DISP:DIMT')

    @property
    def brig(self):
        """brightness - Read/Set - 10.0 to 100.0%"""
        return self._read_cached_property('DISP:BRIG', float)

    @brig.setter
    def brig(self, val):
        if val < 0 or val > 100:
            raise ValueError('Only values between 0.0 and 100.0 allowed')
        else:
            self._write_cached_property('DISP:BRIG', val, float)

    @brig.deleter
    def brig(self):
        self._delete_cached_property('DISP:BRIG')

    @property
    def time(self):
        """time in the 24 hour clock - Read/Set - hh:mm:ss"""
        return self._read_property('TIME', str, 2)

    @time.setter
    def time(self, val):
        hh, mm, ss = [int(s) for s in val.split(':')]
        if hh < 0 or hh > 23:
            raise ValueError('Hours must be between 0 and 24')
        else:
            hh = ('%i' % hh).zfill(2)
        if mm < 0 or mm > 59:
            raise ValueError('Minutes must be between 0 and 60')
        else:
            mm = ('%i' % mm).zfill(2)
        if ss < 0 or ss > 59:
            raise ValueError('Seconds must be between 0 and 60')
        else:
            ss = ('%i' % ss).zfill(2)
        val = ':'.join([hh, mm, ss])
        self._write_property('TIME', val, str)

    @property
    def date(self):
        """date - Read/Set - yyyy:mm:dd"""
        return self._read_property('DATE', str, 2)

    @date.setter
    def date(self, val):
        yyyy, mm, dd = [int(s) for s in val.split(':')]
        yyyy = ('%i' % yyyy).zfill(4)
        if mm < 1 or mm > 12:
            raise ValueError('Month must be between 1 and 12')
        else:
            mm = ('%i' % mm).zfill(2)
        if dd < 0 or dd > 31:
            raise ValueError('Days must be between 0 and 31')
        else:
            dd = ('%i' % dd).zfill(2)
        val = ':'.join([yyyy, mm, dd])

        # Note that this might not validate, since the implementation of the
        # Mercury ITC uses a long signed int to store the unix time stamp, so
        # the maximum date is limited, and also invalidates negative values.

        self._write_property('DATE', val, str)

    @property
    def alarms(self):
        """Gets the system alarms log"""
        string = self._read_property('ALRM', str)
        alarm_list = string[:-1].split(';')
        alarms_dict = dict(item.split('\t') for item in alarm_list)
        return alarms_dict
