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
import itertools
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

    UNITS = ['s', 'Hz', 'G', 'T', 'K', 'dB', 'W']
    PREFIXES = ['', 'E', 'P', 'T', 'G', 'M', 'k', 'h',
                'D', 'd', 'c', 'm', 'u', 'n', 'p', 'f', 'a']

    ALL_UNITS = [p + u for p, u in itertools.product(PREFIXES, UNITS)]

    def __init__(self, value=None, unit='', comment=''):

        self.value = value
        self.unit = unit
        self.comment = comment

    def to_string(self):
        """
        Prints a parameter as string in the Bruker BES3T format.

        :return: Parsed parameter.
        :rtype: str
        """
        is_array = isinstance(self.value, np.ndarray)

        if is_array:
            value_str = ','.join([str(x) for x in self.value.flatten()])
            shape_str = str(self.value.shape).lstrip('(').strip(')').replace(' ', '')
            header = '{{{0};{1};{2}}}'.format(self.value.ndim, shape_str, 0)

        if self.value is None:
            return_str = ''
        elif is_array and self.unit:
            return_str = ' '.join([header, str(self.unit), value_str])
        elif is_array and not self.unit:
            return_str = ' '.join([header, value_str])
        elif not self.unit:
            return_str = str(self.value)
        else:
            return_str = ' '.join([str(self.value), str(self.unit)])

        if self.comment:
            return_str = ' '.join([return_str, self.comment])

        return return_str

    def from_string(self, string):
        """
        Parses a parameter from string given in the Bruker BES3T format.

        :param str string: String to parse.
        """
        self.value = None
        self.unit = ''
        self.comment = ''

        contents = string.split()

        if not contents:
            return

        # remove trailing comments
        if contents[-1].startswith('*'):
            self.comment = contents[-1]
            del contents[-1]

        par_header = ''

        if len(contents) == 0:
            # return if string only was a comment
            return
        elif len(contents) == 1:
            # set single field as value
            par_value = contents[0]
        elif len(contents) == 2:
            # check if we have a header-value pair, a value-unit pair, or a single value
            if re.match(r'\{.*\}', contents[0]):  # header-value pair
                par_header = contents[0]
                par_value = contents[1]
            elif contents[1] in self.ALL_UNITS:  # value-unit pair
                par_value = contents[0]
                self.unit = contents[1]
            else:  # single value with space
                par_value = ' '.join(contents)

        elif len(contents) > 2:
            # check if we have a header-unit-value triple, otherwise just save as string
            if re.match(r'\{.*\}', contents[0]):
                par_header = contents[0]
                self.unit = contents[1]
                par_value = contents[2]
            else:
                par_value = ' '.join(contents)

        # if we have a header, follow its instructions to parse the value
        if par_header:
            array = np.array([float(x) for x in par_value.split(',')])
            shape = [int(x) for x in par_header.split(';')[1].split(',')]
            self.value = array.reshape(shape)
        # otherwise, try to convert the value to Python types int / float / bool / str
        else:
            try:
                if '.' in par_value:
                    self.value = float(par_value)
                else:
                    self.value = int(par_value)
            except ValueError:
                if par_value == 'True':
                    self.value = True
                elif par_value == 'False':
                    self.value = False
                else:
                    self.value = par_value

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
        lines = [self.HEADER_FMT.format(self.name)]

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

    HEADER_FMT = '{0}'
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

    It is not currently possible to change the x/y/z-axis data. Ordinate data can be
    changed, but must match the previous dimensions.

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
        self._dta = np.array([], dtype='>f8')

        self._x = np.array([], dtype='>f8')
        self._y = np.array([], dtype='>f8')
        self._z = np.array([], dtype='>f8')
        self._o = np.array([], dtype='>f8')

        if path:
            self.load(path)

    @property
    def x(self):
        return self._x.astype('float64')

    @property
    def y(self):
        return self._y.astype('float64')

    @property
    def z(self):
        return self._z.astype('float64')

    @property
    def o(self):
        return self._o.astype('float64')

    @o.setter
    def o(self, array_like):
        tmp_array = np.array(array_like, dtype='>f8')

        if not tmp_array.shape == self._o.shape:
            err_msg = 'Ordinate array must have the shape {0!r} to match the axis data.'
            raise ValueError(err_msg.format(self._o.shape))

        self._o = tmp_array
        self._dta = self._o.flatten()

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

    def _load_dta(self, base_path):

        dta_path = base_path + '.DTA'

        self._dta = np.fromfile(dta_path, '>f8')

        if self.pars['XTYP'].value == 'IDX':
            x_min = self.pars['XMIN'].value
            x_max = x_min + self.pars['XWID'].value
            x_pts = self.pars['XPTS'].value
            self._x = np.linspace(x_min, x_max, x_pts, dtype='>f8')
        elif self.pars['XTYP'].value == 'IGD':
            self._x = np.fromfile(base_path + '.XGF', '>f8')

        if self.pars['YTYP'].value == 'IDX':
            y_min = self.pars['YMIN'].value
            y_max = y_min + self.pars['YWID'].value
            y_pts = self.pars['YPTS'].value
            self._y = np.linspace(y_min, y_max, y_pts, dtype='>f8')
        elif self.pars['YTYP'].value == 'IGD':
            self._y = np.fromfile(base_path + '.YGF', '>f8')

        if self.pars['ZTYP'].value == 'IDX':
            z_min = self.pars['ZMIN'].value
            z_max = z_min + self.pars['ZWID'].value
            z_pts = self.pars['ZPTS'].value
            self._z = np.linspace(z_min, z_max, z_pts, dtype='>f8')
        elif self.pars['ZTYP'].value == 'IGD':
            self._z = np.fromfile(base_path + '.ZGF', '>f8')

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
