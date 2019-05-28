# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import, unicode_literals
import os
import re
import numpy as np
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping


def is_metadata(line):
    # metadata lines are either empty or start with a non-alphabetic character
    return len(line) == 0 or not line[0].isalpha()


class XeprParam(object):
    """
    Holds a Bruker measurement parameter in the BES3T file format.

    :ivar value: The parameter value. Should be of type :class:`int`, :class:`float`,
        :class:`bool`, :class:`str`, or :class:`numpy.ndarray`.
    :ivar str unit: String containing the unit. Defaults to an empty string.
    :ivar str comment: Defaults to an empty string. If not empty,
        :attr:`comment` must start with "\*".
    """

    def __init__(self, value=None, unit='', comment=''):

        self._value = value
        self._unit = unit
        self._comment = comment

        self._string = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._string = None

    @property
    def unit(self):
        return self._value

    @unit.setter
    def unit(self, unit):
        self._unit = unit
        self._string = None

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment
        self._string = None

    def to_string(self):
        """
        Prints a parameter as string in the Bruker BES3T format.

        :return: Parsed parameter.
        :rtype: str
        """
        # return original parsed version, if present

        if self._string:
            return self._string
        else:
            return self._to_string()

    def _to_string(self):

        # prepare value string (and potentially header string)
        header_str = ''
        if self._value is None:  # => empty string
            value_str = ''
        elif isinstance(self._value, np.ndarray):  # => flatten and add header
            value_str = ','.join([str(x) for x in self._value.flatten()])
            shape_str = str(self._value.shape).lstrip('(').strip(')').replace(' ', '')
            header_str = '{{{0};{1};{2}}}'.format(self._value.ndim, shape_str, 0)
        else:  # => take default string representation
            value_str = str(self._value)

        # determine order of strings (unit comes before value for arrays!)
        if header_str:  # array
            return_list = [header_str, self._unit, value_str, self._comment]
        else:  # not an array
            return_list = [value_str, self._unit, self._comment]

        # join all non-empty strings
        return_str = ' '.join([r for r in return_list if r != ''])

        return return_str

    def from_string(self, string):
        """
        Parses a parameter from string given in the Bruker BES3T format.

        :param str string: String to parse.
        """

        self._string = string
        self._value = None
        self._unit = ''
        self._comment = ''

        contents = string.split()

        if not contents:
            return

        # remove trailing comments
        if contents[-1].startswith('*'):
            self._comment = contents[-1]
            del contents[-1]

        par_header = None

        if len(contents) == 0:
            # return if string only was a comment
            return
        elif len(contents) == 1:
            # set single field as value
            par_value = contents[0]
        elif len(contents) == 2:
            # check if we have a header-value pair, a value-unit pair, or a single value
            if re.match(r'\{.*\}', contents[0]):  # first block is a header
                par_header = contents[0]
                par_value = contents[1]
            else:
                try:
                    float(contents[0])
                    par_value = contents[0]
                    # if first block is a number, second block must be a unit
                    self._unit = contents[1]
                except ValueError:  # a string with spaces
                    par_value = ' '.join(contents)
        # check if we have a header-unit-value triple
        elif re.match(r'\{.*\}', contents[0]):
            par_header = contents[0]
            self._unit = contents[1]
            par_value = contents[2]
        else:  # otherwise just save as string
            par_value = ' '.join(contents)

        if par_header:  # follow header instructions to parse the value
            array = np.array([float(x) for x in par_value.split(',')])
            shape = [int(x) for x in par_header.split(';')[1].split(',')]
            self._value = array.reshape(shape)
        else:  # try to convert the value to Python types int / float / bool / str
            try:
                if '.' in par_value:
                    self._value = float(par_value)
                else:
                    self._value = int(par_value)
            except ValueError:
                if par_value == 'True':
                    self._value = True
                elif par_value == 'False':
                    self._value = False
                else:
                    self._value = par_value

    def __repr__(self):
        return '<{0}({1})>'.format(self.__class__.__name__, self.to_string())


class ParamGroup(object):
    """
    Class to hold an Xepr experiment parameter group, which is part of a layer.

    :cvar HEADER_FMT: Format of parameter group header.
    :cvar CELL_LENGTH: Length of cell containing the parameter name.
    :cvar DELIM: Delimiter between parameter name and value.

    :ivar str name: The parameter group's name.
    :ivar dict pars: Dictionary containing all :class:`XeprParam` instances belonging
        to the group.
    """
    HEADER_FMT = '* {0}'
    CELL_LENGTH = 19
    DELIM = ''

    def __init__(self, name='', pars=None):
        self.name = name
        if pars is None:
            self.pars = dict()
        else:
            self.pars = dict(pars)

    def to_string(self):
        """
        Prints a parameter group as string.
        """
        if self.HEADER_FMT:
            lines = [self.HEADER_FMT.format(self.name)]
        else:
            lines = []

        for name, param in self.pars.items():
            new_line = '{0}{1}{2}'.format(name.ljust(self.CELL_LENGTH), self.DELIM,
                                          param.to_string())
            lines.append(new_line)

        return '\n'.join(lines)

    def from_string(self, string):
        """
        Parses a parameter group from given string.

        :param str string: Parameter group string from Bruker .DSC file.
        """

        lines = string.split('\n')

        for line in lines:
            if not is_metadata(line):
                contents = line.split()
                par_name = contents[0]
                par_string = ' '.join(contents[1:])

                new_param = XeprParam()
                new_param.from_string(par_string)
                self.pars[par_name] = new_param

    def __repr__(self):
        return '<{0}({1})>'.format(self.__class__.__name__, self.name)


class ParamGroupDESC(ParamGroup):
    """
    Class to hold an Xepr experiment parameter group which forms a section
    of the Descriptor Layer (DESC).
    """
    HEADER_FMT = '*\n*	{0}:\n*'
    CELL_LENGTH = 0
    DELIM = '\t'


class ParamGroupSPL(ParamGroup):
    """
    Class to hold an Xepr experiment parameter group associated with a functional unit,
    part of the Standard Parameter Layer (SPL).
    """

    HEADER_FMT = None
    CELL_LENGTH = 8
    DELIM = ''


class ParamGroupDSL(ParamGroup):
    """
    Class to hold an Xepr experiment parameter group associated with a functional unit,
    part of the Device Specific Layer (DSL).
    """
    VERSION = '1.0'
    HEADER_FMT = '\n.DVC     {0}, %s\n' % VERSION
    CELL_LENGTH = 19
    DELIM = ''


class ParamGroupMHL(ParamGroup):
    """
    Class to hold an Xepr experiment parameter group which forms a section
    of the Manipulation History Layer (MHL).
    """

    HEADER_FMT = '*\n*	{0}:\n*'
    CELL_LENGTH = 8
    DELIM = ''


class ParamLayer(object):
    """
    Parameter layer object. Contains a top level parameter section of a
    Bruker BES3T file. This should be subclassed, depending on the actual
    parameter layer type.

    :cvar TYPE: Parameter layer type. Can be 'DESC' for a Descriptor Layer, 'SPL' for a
        Standard Parameter Layer, 'DSL' for a Device Specific Layer or 'MHL' for a
        Manipulation History Layer.
    :cvar NAME: Parameter layer name.
    :cvar VERSION: Parameter layer version. This identifies the implemented BES3T file
        format specification used when parsing the information.
    :cvar HEADER_FMT: Header format for the parameter layer.
    :cvar END: Characters to indicate the end of layer in '.DSC' file.
    """

    TYPE = 'TEMP'
    NAME = 'TEMPLATE LAYER'
    VERSION = '1.0'
    SUPPORTED_VERSIONS = ('1.0', '1.2', '2.0',)

    HEADER_FMT = '#{0}	{1} * {2}\n*'
    LB = '\n'
    END = '*\n' + '*'*60 + '\n*'

    GROUP_CLASS = ParamGroup

    def __init__(self, groups=None):
        self.groups = dict() if groups is None else groups

    def to_string(self):
        """
        Prints the parameter layer as string.

        :return: Parameter layer string in as found in '.DSC' file.
        :rtype: str
        """
        lines = [self.HEADER_FMT.format(self.TYPE, self.VERSION, self.NAME)]

        for group in self.groups.values():
            lines.append(group.to_string())

        lines.append(self.END)

        return '\n'.join(lines)

    def from_string(self, string):
        """
        Parses parameter layer string to contained parameters

        :param str string: Parameter layer string in as found in '.DSC' file.
        """
        self.groups = dict()

        # use only alphabetic characters in `unique`
        # otherwise `re.escape` may inadvertently escape them in Python < 3.7
        unique = 'UNIQUESTRING'
        fmt = self.GROUP_CLASS.HEADER_FMT
        assert unique not in fmt

        regexp1 = re.escape(fmt.format(unique)).replace(unique, '(.*)')
        regexp2 = re.escape(fmt.format(unique)).replace(unique, '.*')

        group_names = re.findall(regexp1, string)
        group_contents = re.split(regexp2, string)[1:]

        for name, content in zip(group_names, group_contents):
            new_group = self.GROUP_CLASS(name=name)
            new_group.from_string(content)
            self.groups[name] = new_group


class DescriptorLayer(ParamLayer):
    """
    Descriptor Layer class.
    """

    TYPE = 'DESC'
    NAME = 'DESCRIPTOR INFORMATION'
    VERSION = '1.2'
    SUPPORTED_VERSIONS = ('1.2',)

    HEADER_FMT = '#{0}	{1} * {2} ***********************'

    GROUP_CLASS = ParamGroupDESC


class StandardParameterLayer(ParamLayer):
    """
    Standard Parameter Layer class.
    """

    TYPE = 'SPL'
    NAME = 'STANDARD PARAMETER LAYER'
    VERSION = '1.2'
    SUPPORTED_VERSIONS = ('1.2',)

    GROUP_CLASS = ParamGroupSPL

    def from_string(self, string):
        self.groups = dict()

        new_group = self.GROUP_CLASS(name='')
        new_group.from_string(string)
        self.groups[''] = new_group


class DeviceSpecificLayer(ParamLayer):
    """
    Device Specific Parameter Layer class.
    """

    TYPE = 'DSL'
    NAME = 'DEVICE SPECIFIC LAYER'
    VERSION = '1.0'
    SUPPORTED_VERSIONS = ('1.0',)

    END = '\n*\n' + '*' * 60 + '\n*'

    GROUP_CLASS = ParamGroupDSL


class ManipulationHistoryLayer(ParamLayer):
    """
    Manipulation History Parameter Layer class.
    """
    TYPE = 'MHL'
    NAME = 'MANIPULATION HISTORY LAYER by BRUKER'
    VERSION = '1.0'
    SUPPORTED_VERSIONS = ('1.0',)

    GROUP_CLASS = ParamGroupMHL


class ParamDict(MutableMapping):

    def __init__(self, layers):

        for layer in layers.values():
            if not isinstance(layer, ParamLayer):
                raise ValueError('Layers must all be instances of "ParamLayer".')

        self.layers = layers

    def _flatten(self):

        flat_dict = dict()

        for layer in self.layers.values():
            for group in layer.groups.values():
                flat_dict.update(group.pars)

        return flat_dict

    def copy(self):
        """
        Returns the flatted dictionary.

        :rtype: dict
        """
        return self._flatten()

    def __getitem__(self, key):

        flat_dict = self._flatten()

        return flat_dict[key]

    def __setitem__(self, key, value):

        # convert value to XeprParam if necessary
        if not isinstance(value, XeprParam):
            value = XeprParam(value)

        # if the parameter belongs to an existing group, update it with the new value
        for layer in self.layers.values():
            for group in layer.groups.values():
                if key in group.pars.keys():
                    group.pars[key] = value
                    return  # we are done!

        # if the parameter is new, add it as a 'customXepr' parameter
        if 'customXepr' not in self.layers['DSL'].groups:
            self.layers['DSL'].groups['customXepr'] = ParamGroupDSL('customXepr')

        self.layers['DSL'].groups['customXepr'].pars[key] = value

    def __delitem__(self, key):

        is_deleted = False

        for layer in self.layers.values():
            for group in layer.groups.values():
                if key in group.pars.keys():
                    del group.pars[key]
                    is_deleted = True

        if not is_deleted:
            raise KeyError('Parameter "%s" does not exist.' % key)

    def __iter__(self):
        flat_dict = self._flatten()
        return iter(flat_dict)

    def __len__(self):
        flat_dict = self._flatten()
        return len(flat_dict)


# noinspection PyTypeChecker
class XeprData(object):
    """
    Holds a Bruker EPR measurement result, including all measurement parameters.
    Supports importing and exporting to the Bruker BES3T file format ('.DSC',
    '.DTA' and possible associated 'XGF', 'YGF' and 'ZGF' files) in the 1.2
    specification currently used by Xepr. Parameters are stored in the following
    attributes and are grouped after the associated functional unit (e.g., 'mwBridge',
    'fieldCtrl') or type (e.g., 'Documentational Text').

    :ivar desc: :class:`DescriptorLayer` instance holding the parameters from the '.DSC'
        file that describe content and parsing of corresponding data files ('.DTA' etc).
    :ivar spl: :class:`StandardParameterLayer` instance holding all mandatory EPR
        parameters, such as the microwave power.
    :ivar dsl: :class:`DeviceSpecificLayer` instance holding the EPR measurement
        parameters specific to the instrument and type of measurement, i.e., the
        measurement temperature, sample angles, integration time, etc.
    :ivar mhl: :class:`ManipulationHistoryLayer` instance holding all parameters that
        describe manipulations performed on the data set (e.g., baseline correction,
        scaling, ...).

    The actual data is accessible as numpy arrays :attr:`XeprData.x`, :attr:`XeprData.y`,
    :attr:`XeprData.z` and :attr:`XeprData.o`.

    All measurement parameters are also accessible in as a dictionary
    attr:`XeprData.pars`. Setting the value of an existing parameter will automatically
    update it in the appropriate parameter layer. Setting a new parameter value will
    add it to a 'customXepr' device group in the :class:`DeviceSpecificLayer`.

    It is not currently possible to change the contained spectra but only the parameters.

    .. warning::

        Changing the parameters in the Descriptor Layer may result in inconsistencies
        between the parameter file (DSC) and the actual data files (DTA, XGF, YGF, ZGF)
        and therefore may result in corrupted files.

    :Example:

        Read a data file and get some information about the device specific parameters:

        >>> from customxepr import XeprData, XeprParam
        >>> dset = XeprData('/path/to/file.DSC')
        >>> dset.dsl.groups
        {'fieldCtrl': <ParamGroupDSL(fieldCtrl)>,
         'fieldSweep': <ParamGroupDSL(fieldSweep)>,
         'freqCounter': <ParamGroupDSL(freqCounter)>,
         'mwBridge': <ParamGroupDSL(mwBridge)>,
         'recorder': <ParamGroupDSL(recorder)>,
         'signalChannel': <ParamGroupDSL(signalChannel)>}
        >>> dset.dsl.groups['mwBridge'].pars
        {'AcqFineTuning': <XeprParam(Never)>,
         'AcqScanFTuning': <XeprParam(Off)>,
         'AcqSliceFTuning': <XeprParam(Off)>,
         'BridgeCalib': <XeprParam(50.5)>,
         'Power': <XeprParam(0.002 mW)>,
         'PowerAtten': <XeprParam(50.0 dB)>,
         'QValue': <XeprParam(5900)>}

        Change the value of an existing parameter:

        >>> dset.pars['ModAmp'] = XeprParam(value=2, unit='G')

        Add a new parameter without an associated group (it will be added to a
        'customXepr' group in the DSL layer):

        >>> dset.pars['NewParam'] = 1234

        Add a new parameter to the microwave bridge device group:

        >>> dset.dsl.groups['mwBridge'].pars['QValue']  = XeprParam(6789)

        Add a new parameter group for a temperature controller, with two parameters:

        >>> pars = {'Temperature': XeprParam(290, 'K'),
        ...         'AcqWaitTime': XeprParam(120, 's')}
        >>> new_group = ParamGroupDSL('tempCtrl', pars)
        >>> dset.dsl.groups['tempCtrl'] = new_group

        Save the modified data set:

        >>> data_set.save('/path/to/file.DSC')

    """

    IRFMTS_DICT = {'D': 'f8', 'F': 'f4', 'I': 'i4', 'NODATA': '', '0': ''}

    byte_order = '>'  # Bruker data files default to 'big-endian' byte-order

    def __init__(self, path=None):
        """
        :param str path: If given, the data file will be loaded from ``path``.
        """

        self.desc = DescriptorLayer()  # Descriptor Layer (mandatory)
        self.spl = StandardParameterLayer()  # Standard Parameter Layer (optional)
        self.dsl = DeviceSpecificLayer()  # Device Specific Layer (optional)
        self.mhl = ManipulationHistoryLayer()  # Manipulation History Layer (optional)

        self.param_layers = dict(DESC=self.desc, SPL=self.spl, DSL=self.dsl, MHL=self.mhl)

        self.pars = ParamDict(layers=self.param_layers)

        self._dsc = None
        self._dta = np.array([])

        self._x = np.array([])
        self._y = np.array([])
        self._z = np.array([])
        self._o = np.array([])

        if path:
            self.load(path)

    @property
    def x(self):
        return self._x.astype(float)

    @property
    def y(self):
        return self._y.astype(float)

    @property
    def z(self):
        return self._z.astype(float)

    @property
    def o(self):
        """
        Returns a numpy array with ordinate data or a tuple of arrays containing all
        ordinate data sets. If real and imaginary parts are present, they will be
        combined to a complex numpy array.
        """

        ikkf = self.pars['IKKF'].value.split(',')  # get ordinate type: real or complex

        # split self._o into numpy arrays, combine real and imaginary parts
        r_list = []
        for i in range(len(ikkf)):
            # get real part
            r = self._o['o%s real' % i].astype(float)
            if ikkf[i] == 'CPLX':
                # add imaginary part
                r = r + 1j*self._o['o%s imag' % i].astype(float)
            r_list.append(r)

        return r_list[0] if len(r_list) == 1 else tuple(r_list)

    def load(self, path):
        """
        Loads data and parameters from a '.DSC' file and accompanying data files.

        :param str path: Path to '.DSC' file or accompanying data files to load. Any of
            those file paths can be given, the other files belonging to the same data set
            will be found automatically if in the same directory.
        """

        path = os.path.expanduser(path)
        base_path = path.split('.')[0]

        dsc_path = base_path + '.DSC'

        if not os.path.isfile(dsc_path):
            raise ValueError('No such file: %s' % dsc_path)

        self._load_dsc(base_path)
        self._load_dta(base_path)

    def _load_dsc(self, base_path):

        dsc_path = base_path + '.DSC'

        with open(dsc_path, 'r') as f:
            self._dsc = f.read()

        # separate layer sections, delimited by '#'
        layer_strings = self._dsc.split('#')[1:]

        # read layer sections
        for string in layer_strings:
            # separate strings into header and body
            head, sep, tail = string.partition('\n')
            # identify layer type and format version from header
            layer_type, version = head.split()[0:2]

            # check if type and version are supported, raise error or warn otherwise
            if layer_type not in self.param_layers.keys():
                raise IOError('Parameter layer "{0}" not recognized.'.format(layer_type))
            if version not in self.param_layers[layer_type].SUPPORTED_VERSIONS:
                print('Version {0} of {1} format is not '.format(version, layer_type) +
                      'supported. You may encounter parsing errors and data corruption.')

            # parse content to respective parameter layer objects
            self.param_layers[layer_type].from_string(tail)
            self.param_layers[layer_type].VERSION = version

        # determine byte order of data from DSC file
        if self.pars['BSEQ'].value == 'BIG':
            self._byte_order = '>'
        elif self.pars['BSEQ'].value == 'LIT':
            self._byte_order = '<'
        else:
            raise IOError('Byte-order of data file is not supported.')

    def _get_dta_dtype(self):

        # determine if acquired quantities are real or complex
        ikkfs = self.pars['IKKF'].value.split(',')

        # determine type of data: int 32-bit, float 32-bit or float 64-bit
        if 'CPLX' in ikkfs:
            irfmts = self.pars['IRFMT'].value.split(',')
            iifmts = self.pars['IRFMT'].value.split(',')
        else:
            irfmts = self.pars['IRFMT'].value.split(',')
            iifmts = len(irfmts)*['0']

        # convert to numpy data types
        try:
            dtypes_real = [self.IRFMTS_DICT[irfmt] for irfmt in irfmts]
            dtypes_imag = [self.IRFMTS_DICT[iifmt] for iifmt in iifmts]
        except KeyError:
            raise IOError('Data file has a not-supported data-type. Data type must ' +
                          'be double (64-bit), float(32-bit), or int (32-bit).')

        # assert that we have data types for each quantity
        assert len(dtypes_real) == len(ikkfs)
        assert len(dtypes_imag) == len(ikkfs)

        field_names = []
        data_types = []
        for n, dtype_r, dtype_i in zip(range(len(ikkfs)), dtypes_real, dtypes_imag):
            data_types.append(self._byte_order + dtype_r)
            field_names.append('o%s real' % n)
            if not dtype_i == '':
                data_types.append(self._byte_order + dtype_i)
                field_names.append('o%s imag' % n)

        return list((fn, dt) for fn, dt in zip(field_names, data_types))

    def _get_axis_dtype(self, axis='x'):

        # determine type of data: int 32-bit, float 32-bit or float 64-bit
        par_name = axis.capitalize() + 'FMT'
        try:
            dtype = self.IRFMTS_DICT[self.pars[par_name].value]
        except KeyError:
            raise IOError('Axis data file has a not-supported data-type. Data type ' +
                          'must be double (64-bit), float(32-bit), or int (32-bit).')
        return self._byte_order + dtype

    def _load_dta(self, base_path):

        dta_path = base_path + '.DTA'
        fmt = self._get_dta_dtype()

        self._dta = np.fromfile(dta_path, fmt)

        if self.pars['XTYP'].value == 'IDX':  # indexed data
            ax_min = self.pars['XMIN'].value
            ax_max = ax_min + self.pars['XWID'].value
            ax_pts = self.pars['XPTS'].value
            self._x = np.linspace(ax_min, ax_max, ax_pts)
        elif self.pars['XTYP'].value == 'IGD':  # data points saved in file
            fmt = self._get_axis_dtype('X')
            self._x = np.fromfile(base_path + '.XGF', fmt)
        elif self.pars['XTYP'].value == 'NTUP':  # currently not supported
            raise IOError('Tuple data is currently not supported by XeprData.')

        if self.pars['YTYP'].value == 'IDX':  # indexed data
            ax_min = self.pars['YMIN'].value
            ax_max = ax_min + self.pars['YWID'].value
            ax_pts = self.pars['YPTS'].value
            self._y = np.linspace(ax_min, ax_max, ax_pts)
        elif self.pars['YTYP'].value == 'IGD':  # data points saved in file
            fmt = self._get_axis_dtype('Y')
            self._y = np.fromfile(base_path + '.YGF', fmt)
        elif self.pars['YTYP'].value == 'NTUP':  # currently not supported
            raise IOError('Tuple data is currently not supported by XeprData.')

        if self.pars['ZTYP'].value == 'IDX':  # indexed data
            ax_min = self.pars['ZMIN'].value
            ax_max = ax_min + self.pars['ZWID'].value
            ax_pts = self.pars['ZPTS'].value
            self._z = np.linspace(ax_min, ax_max, ax_pts)
        elif self.pars['ZTYP'].value == 'IGD':  # data points saved in file
            fmt = self._get_axis_dtype('Z')
            self._z = np.fromfile(base_path + '.ZGF', fmt)
        elif self.pars['ZTYP'].value == 'NTUP':  # currently not supported
            raise IOError('Tuple data is currently not supported by XeprData.')

        if self._z.size > 0:
            self._o = self._dta.reshape(self.z.size, self.y.size, self.x.size)
        elif self._y.size > 0:
            self._o = self._dta.reshape(self.y.size, self.x.size)
        else:
            self._o = self._dta

    def save(self, path):
        """
        Saves data and parameters to a '.DSC' file and accompanying data files.

        :param str path: Path to '.DSC' file or accompanying data files to save. Any of
            those file paths can be given, the other file names will be generated as
            necessary.
        """

        path = os.path.expanduser(path)
        base_path = path.split('.')[0]

        dsc_path = base_path + '.DSC'
        dta_path = base_path + '.DTA'

        self._dsc = self.print_dsc()

        with open(dsc_path, 'w') as f:
            f.write(self._dsc)

        self._dta.tofile(dta_path)

        if self.pars['XTYP'].value == 'IGD':
            self._x.tofile(base_path + '.XGF')

        if self.pars['YTYP'].value == 'IGD':
            self._y.tofile(base_path + '.YGF')

        if self.pars['ZTYP'].value == 'IGD':
            self._z.tofile(base_path + '.YGF')

    def print_dsc(self):
        """
        Parses all parameters as '.DSC' file content and returns the result as a string.

        :return: String containing all parameters in '.DSC' file format.
        :rtype: str
        """

        lines = []

        for layer in self.param_layers.values():
            if len(layer.groups) > 0:
                lines.append(layer.to_string())

        lines[-1] = lines[-1].strip('*')

        return '\n'.join(lines)

    def plot(self):
        """
        Plots all recorded spectra / sweeps as 2D or 3D plots.
        """

        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
        except ImportError:
            raise ImportError('Install matplotlib to support plotting.')

        fig = plt.figure()

        x_label = self.pars['XNAM'].value + ' [%s]' % self.pars['XUNI'].value

        if self.y.size == 0:
            ax = fig.add_subplot(111)
            ax.autoscale(axis='x', tight=True)
            ax.plot(self.x, self.o)

            y_label = self.pars['IRNAM'].value
            ax.set_xlabel(x_label.replace("'", ""))
            ax.set_ylabel(y_label.replace("'", ""))
        else:
            ax = fig.add_subplot(111, projection='3d')
            ax.autoscale(axis='x', tight=True)

            for y_point, z_data in zip(self.y, self.o):
                y_data = np.full_like(self.x, y_point)
                ax.plot(self.x, y_data, z_data)

            y_label = self.pars['YNAM'].value + ' [%s]' % self.pars['YUNI'].value
            z_label = self.pars['IRNAM'].value

            ax.set_xlabel(x_label.replace("'", ""))
            ax.set_ylabel(y_label.replace("'", ""))
            ax.set_zlabel(z_label.replace("'", ""))

        fig.tight_layout()
        fig.show()
