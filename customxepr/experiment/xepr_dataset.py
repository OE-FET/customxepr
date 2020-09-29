# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
import os
import re
import numpy as np
from typing import Optional, Union, Dict, Iterator, Tuple, List

from collections.abc import MutableMapping

ParamValueType = Union[float, bool, str, np.ndarray, None]


def is_metadata(line: str) -> bool:
    # metadata lines are either empty or start with a non-alphabetic character
    return len(line) == 0 or not line[0].isalpha()


def num2str(number: float) -> str:
    if isinstance(number, (float, np.float64)):
        return "{:.6e}".format(number)
    elif isinstance(number, (int, np.int64)):
        return str(number)
    else:
        raise ValueError("Number must be float or str")


def str2num(string: str) -> float:
    try:
        return int(string)
    except ValueError:
        return float(string)


class XeprParam:
    """
    Holds a Bruker measurement parameter in the BES3T file format.

    :param value: The parameter value.
    :param unit: String containing the unit. Defaults to an empty string.
    :param comment: Defaults to an empty string.
    """

    HEADER_REGEX = r"{(?P<ndmin>\d*);(?P<shape>[\d,]*);(?P<default>[0-9\.e+-]*)\[?(?P<unit>\w*)\]?}"

    def __init__(
        self, value: ParamValueType = None, unit: str = "", comment: str = ""
    ) -> None:

        self._value = value
        self._matrix_default_value = 0
        self._unit = unit
        self._comment = comment

        self._string = None

    @property
    def value(self) -> ParamValueType:
        return self._value

    @value.setter
    def value(self, value: ParamValueType):
        self._value = value
        self._string = None

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, unit: str):
        self._unit = unit
        self._string = None

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comment: str):
        self._comment = comment
        self._string = None

    def to_string(self) -> str:
        """
        Prints a parameter as string in the Bruker BES3T format.

        :return: Parsed parameter.
        """
        # return original parsed version, if present

        if not self._string:
            self._string = self._to_string()

        return self._string

    def _to_string(self) -> str:

        return_list = []

        if self.value is not None:

            is_matrix = isinstance(self.value, np.ndarray)

            if is_matrix:
                value_str = ",".join([num2str(x) for x in self.value.flatten()])
                shape_str = ",".join(num2str(x) for x in self.value.shape)
                if self.unit:
                    header_str = "{{{0};{1};{2}[{3}]}}".format(
                        self.value.ndim,
                        shape_str,
                        num2str(self._matrix_default_value),
                        self.unit,
                    )
                else:
                    header_str = "{{{0};{1};{2}}}".format(
                        self.value.ndim, shape_str, num2str(self._matrix_default_value)
                    )

                return_list.append(header_str)
                return_list.append(value_str)
            else:  # => take default string representation
                if isinstance(self.value, (float, int)):
                    value_str = num2str(self.value)
                elif isinstance(self.value, str):
                    value_str = self.value
                else:
                    value_str = str(self.value)

                return_list.append(value_str)

                if self.unit:
                    return_list.append(self.unit)

        if self.comment:

            if self.comment.startswith("*"):
                comment_str = self.comment
            else:
                comment_str = "* " + self.comment

            return_list.append(comment_str)

        return " ".join([r for r in return_list])

    def from_string(self, string: str) -> None:
        """
        Parses a parameter from string given in the Bruker BES3T format.

        :param str string: String to parse.
        """

        self._string = string
        self._value = None
        self._unit = ""
        self._comment = ""

        contents = string.split()

        if not contents:
            return

        # remove trailing comments
        if contents[-1].startswith("*"):
            self._comment = contents[-1].lstrip("*")
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
            if re.match(r"{.*}", contents[0]):  # first block is a header
                par_header = contents[0]
                par_value = contents[1]
            else:
                try:
                    float(contents[0])
                    par_value = contents[0]
                    # if first block is a number, second block must be a unit
                    self._unit = contents[1]
                except ValueError:  # a string with spaces
                    par_value = " ".join(contents)
        else:  # otherwise just save as string
            par_value = " ".join(contents)

        if par_header:  # follow header instructions to parse the value
            array = np.array([str2num(x) for x in par_value.split(",")])
            match = re.match(XeprParam.HEADER_REGEX, par_header)
            ndim = str2num(match["ndmin"])
            shape = [str2num(x) for x in match["shape"].split(",")]
            self._matrix_default_value = str2num(match["default"])

            if len(shape) != ndim:
                raise ValueError(
                    "Inconsistent matrix dimensions: got "
                    "{} dimensions but shape is {}".format(ndim, shape)
                )

            self._unit = match["unit"]
            self._value = array.reshape(shape)
        else:  # try to convert the value to Python types int / float / bool / str
            try:
                self._value = str2num(par_value)
            except ValueError:
                if par_value in ("True", "False"):
                    self._value = bool(par_value)
                else:
                    self._value = par_value

    def __repr__(self) -> str:
        return "<{0}({1})>".format(self.__class__.__name__, self.to_string())


class ParamGroup:
    """
    Class to hold an Xepr experiment parameter group, which is part of a layer.

    :cvar HEADER_FMT: Format of parameter group header.
    :cvar CELL_LENGTH: Length of cell containing the parameter name.
    :cvar DELIM: Delimiter between parameter name and value.

    :ivar name: The parameter group's name.
    :ivar pars: Dictionary containing all :class:`XeprParam` instances belonging to the
    group.
    """

    HEADER_FMT = "* {0}"
    CELL_LENGTH = 19
    DELIM = ""

    def __init__(
        self, name: str = "", pars: Optional[Dict[str, XeprParam]] = None
    ) -> None:
        self.name = name
        if pars is None:
            self.pars = dict()
        else:
            self.pars = dict(pars)

    def to_string(self) -> str:
        """
        Prints a parameter group as string.
        """
        if self.HEADER_FMT:
            lines = [self.HEADER_FMT.format(self.name)]
        else:
            lines = []

        for name, param in self.pars.items():
            new_line = "{0}{1}{2}".format(
                name.ljust(self.CELL_LENGTH), self.DELIM, param.to_string()
            )
            lines.append(new_line)

        return "\n".join(lines)

    def from_string(self, string: str) -> None:
        """
        Parses a parameter group from given string.

        :param string: Parameter group string from Bruker .DSC file.
        """

        lines = string.split("\n")

        for line in lines:
            if not is_metadata(line):
                contents = line.split()
                par_name = contents[0]
                par_string = " ".join(contents[1:])

                new_param = XeprParam()
                new_param.from_string(par_string)
                self.pars[par_name] = new_param

    def __repr__(self) -> str:
        return "<{0}({1})>".format(self.__class__.__name__, self.name)


class ParamGroupDESC(ParamGroup):
    """
    Class to hold an Xepr experiment parameter group which forms a section
    of the Descriptor Layer (DESC).
    """

    HEADER_FMT = "*\n*	{0}:\n*"
    CELL_LENGTH = 0
    DELIM = "\t"


class ParamGroupSPL(ParamGroup):
    """
    Class to hold an Xepr experiment parameter group associated with a functional unit,
    part of the Standard Parameter Layer (SPL).
    """

    HEADER_FMT = None
    CELL_LENGTH = 8
    DELIM = ""


class ParamGroupDSL(ParamGroup):
    """
    Class to hold an Xepr experiment parameter group associated with a functional unit,
    part of the Device Specific Layer (DSL).
    """

    VERSION = "1.0"
    HEADER_FMT = "\n.DVC     {0}, %s\n" % VERSION
    CELL_LENGTH = 19
    DELIM = ""


class ParamGroupMHL(ParamGroup):
    """
    Class to hold an Xepr experiment parameter group which forms a section
    of the Manipulation History Layer (MHL).
    """

    HEADER_FMT = "*\n*	{0}:\n*"
    CELL_LENGTH = 8
    DELIM = ""


class ParamLayer:
    """
    Parameter layer object. Contains a top level parameter section of a Bruker BES3T file.
    This should be subclassed, depending on the actual parameter layer type.

    :cvar TYPE: Parameter layer type. Can be 'DESC' for a Descriptor Layer, 'SPL' for a
        Standard Parameter Layer, 'DSL' for a Device Specific Layer or 'MHL' for a
        Manipulation History Layer.
    :cvar NAME: Parameter layer name.
    :cvar VERSION: Parameter layer version. This identifies the implemented BES3T file
        format specification used when parsing the information.
    :cvar HEADER_FMT: Header format for the parameter layer.
    :cvar END: Characters to indicate the end of layer in '.DSC' file.
    """

    TYPE = "TEMP"
    NAME = "TEMPLATE LAYER"
    VERSION = "1.0"
    SUPPORTED_VERSIONS = (
        "1.0",
        "1.2",
        "2.0",
    )

    HEADER_FMT = "#{0}	{1} * {2}\n*"
    LB = "\n"
    END = "*\n" + "*" * 60 + "\n*"

    GROUP_CLASS = ParamGroup

    def __init__(self, groups: Optional[Dict[str, ParamGroup]] = None) -> None:

        self.groups = dict() if groups is None else groups

    def to_string(self) -> str:
        """
        Prints the parameter layer as string.

        :return: Parameter layer string in as found in '.DSC' file.
        :rtype: str
        """
        lines = [self.HEADER_FMT.format(self.TYPE, self.VERSION, self.NAME)]

        for group in self.groups.values():
            lines.append(group.to_string())

        lines.append(self.END)

        return "\n".join(lines)

    def from_string(self, string: str) -> None:
        """
        Parses parameter layer string to contained parameters

        :param str string: Parameter layer string in as found in '.DSC' file.
        """
        self.groups = dict()

        # use only alphabetic characters in `unique`
        # otherwise `re.escape` may inadvertently escape them in Python < 3.7
        unique = "UNIQUESTRING"
        fmt = self.GROUP_CLASS.HEADER_FMT
        assert unique not in fmt

        regexp1 = re.escape(fmt.format(unique)).replace(unique, "(.*)")
        regexp2 = re.escape(fmt.format(unique)).replace(unique, ".*")

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

    TYPE = "DESC"
    NAME = "DESCRIPTOR INFORMATION"
    VERSION = "1.2"
    SUPPORTED_VERSIONS = ("1.2",)

    HEADER_FMT = "#{0}	{1} * {2} ***********************"

    GROUP_CLASS = ParamGroupDESC


class StandardParameterLayer(ParamLayer):
    """
    Standard Parameter Layer class.
    """

    TYPE = "SPL"
    NAME = "STANDARD PARAMETER LAYER"
    VERSION = "1.2"
    SUPPORTED_VERSIONS = ("1.2",)

    GROUP_CLASS = ParamGroupSPL

    def from_string(self, string):
        self.groups = dict()

        new_group = self.GROUP_CLASS()
        new_group.from_string(string)
        self.groups[""] = new_group


class DeviceSpecificLayer(ParamLayer):
    """
    Device Specific Parameter Layer class.
    """

    TYPE = "DSL"
    NAME = "DEVICE SPECIFIC LAYER"
    VERSION = "1.0"
    SUPPORTED_VERSIONS = ("1.0",)

    END = "\n*\n" + "*" * 60 + "\n*"

    GROUP_CLASS = ParamGroupDSL


class ManipulationHistoryLayer(ParamLayer):
    """
    Manipulation History Parameter Layer class.
    """

    TYPE = "MHL"
    NAME = "MANIPULATION HISTORY LAYER by BRUKER"
    VERSION = "1.0"
    SUPPORTED_VERSIONS = ("1.0",)

    GROUP_CLASS = ParamGroupMHL


class ParamDict(MutableMapping):
    """
    Object to allow dictionary-like access to all measurement parameters.
    """

    def __init__(self, layers: Dict[str, ParamLayer]) -> None:

        self.layers = layers

    def _flatten(self) -> Dict[str, XeprParam]:

        flat_dict = dict()

        for layer in self.layers.values():
            for group in layer.groups.values():
                flat_dict.update(group.pars)

        return flat_dict

    def __getitem__(self, key: str) -> XeprParam:

        flat_dict = self._flatten()

        return flat_dict[key]

    def __setitem__(self, key: str, value: Union[XeprParam, ParamValueType]) -> None:

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
        if "customXepr" not in self.layers["DSL"].groups:
            self.layers["DSL"].groups["customXepr"] = ParamGroupDSL("customXepr")

        self.layers["DSL"].groups["customXepr"].pars[key] = value

    def __delitem__(self, key: str) -> None:

        is_deleted = False

        for layer in self.layers.values():
            for group in layer.groups.values():
                if key in group.pars.keys():
                    del group.pars[key]
                    is_deleted = True

        if not is_deleted:
            raise KeyError('Parameter "%s" does not exist.' % key)

    def __iter__(self) -> Iterator[str]:
        flat_dict = self._flatten()
        return iter(flat_dict)

    def __len__(self) -> int:
        flat_dict = self._flatten()
        return len(flat_dict)


class PulseChannel:

    MAXIMUM_PULSES = 32

    def __init__(self, name: str, param: XeprParam) -> None:
        pass


class PulseSequence:

    channel_to_title = {
        "Psd1": "Pulse Gate",
        "Psd2": "Decoupler",
        "Psd3": "Reciever Protection 1",
        "Psd4": "Reciever Protection 2",
        "Psd5": "TWT",
        "Psd6": "Acquisition trigger",
        "Psd7": "+x",
        "Psd8": "+<x>",
        "Psd9": "-x",
        "Psd10": "-<x>",
        "Psd11": "+y",
        "Psd12": "+<y>",
        "Psd13": "-y",
        "Psd14": "-<y>",
        "Psd15": "ELDOR",
        "Psd16": "Low Power Arm",
        "Psd17": "RF1 Gate",
        "Psd18": "RF1 Advance",
        "Psd19": "RF2 Gate",
        "Psd20": "RF2 Advance",
        "Psd21": "U1",
        "Psd22": "U2",
        "Psd23": "U3",
        "Psd24": "U4",
        "Psd25": "U5",
        "Psd26": "U6",
        "Psd27": "AM Protection",
        "Psd28": "Grad trigger",
        "Psd29": "AWG1 Trigger",
        "Psd30": "RF1",
        "Psd31": "RF2",
        "Psd32": "AWG1",
        "Psd33": "AWG2",
        "Psd34": "AWG3",
        "Psd35": "AWG4",
        "Psd36": "Grad Strength",
    }

    def __init__(self, dset: "XeprData") -> None:
        pass


# noinspection PyTypeChecker
class XeprData:
    """
    Holds a Bruker EPR measurement result, including all measurement parameters.
    Supports importing and exporting to the Bruker BES3T file format ('.DSC',
    '.DTA' and possible associated '.XGF', '.YGF' and '.ZGF' files) in the 1.2
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
    :ivar pars: Dictionary-like object giving direct access to all measurement parameters.
        Allows for quickly reading and setting parameter values.

    Setting the value of an existing parameter will automatically
    update it in the appropriate parameter layer. Setting a new parameter value will
    add it to a 'customXepr' device group in the :class:`DeviceSpecificLayer`.

    The actual data is accessible as numpy arrays :attr:`x`, :attr:`y`, :attr:`z` and
    :attr:`o`. Only the the ordinate data may be changed and the new data must have
    the same size and format as :attr:`o`. It is not currently possible to change the
    x/y/z-axis data.

    .. warning::

        Changing the parameters in the Descriptor Layer may result in inconsistencies
        between the parameter file (DSC) and the actual data files (DTA, XGF, YGF, ZGF)
        and therefore may result in corrupted files.

    :Examples:

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

        >>> dset.save('/path/to/file.DSC')

    """

    IRFMTS_DICT = {"D": "f8", "F": "f4", "I": "i4", "NODATA": "", "0": ""}

    byte_order = ">"  # Bruker data files default to 'big-endian' byte-order

    def __init__(self, path: Optional[str] = None) -> None:
        """
        :param str path: If given, the data file will be loaded from ``path``.
        """

        self.desc = DescriptorLayer()  # Descriptor Layer (mandatory)
        self.spl = StandardParameterLayer()  # Standard Parameter Layer (optional)
        self.dsl = DeviceSpecificLayer()  # Device Specific Layer (optional)
        self.mhl = ManipulationHistoryLayer()  # Manipulation History Layer (optional)

        self.param_layers = dict(
            DESC=self.desc, SPL=self.spl, DSL=self.dsl, MHL=self.mhl
        )
        self.pars = ParamDict(layers=self.param_layers)

        self._dsc = None
        self._dta = np.array([])

        self._x = np.array([])
        self._y = np.array([])
        self._z = np.array([])
        self._o = np.array([])

        if path:
            self.load(path)

    def __len__(self) -> int:
        return len(self._x)

    @property
    def shape(self) -> Tuple[int, ...]:
        return tuple(len(a) for a in (self._x, self._y, self._z) if len(a) > 0)

    @property
    def x(self) -> np.ndarray:
        """Returns x-axis data as numpy array."""
        return self._x.astype(float)

    @property
    def y(self) -> np.ndarray:
        """Returns y-axis data as numpy array."""
        return self._y.astype(float)

    @property
    def z(self) -> np.ndarray:
        """Returns z-axis data as numpy array."""
        return self._z.astype(float)

    @property
    def o(self) -> np.ndarray:
        """
        Returns ordinate data as numpy array or as a tuple of arrays containing all
        ordinate data sets. If real and imaginary parts are present, they will be
        combined to a complex numpy array.
        """

        ikkf = self.pars["IKKF"].value.split(",")  # get ordinate types: real or complex

        # split self._o into numpy arrays, combine real and imaginary parts
        r_list = []
        for i in range(len(ikkf)):
            if ikkf[i] == "CPLX":
                r = self._o["o%s real" % i] + 1j * self._o["o%s imag" % i]
            else:
                r = self._o["o%s real" % i]

            r_list.append(r.astype("complex128"))

        return r_list[0] if len(r_list) == 1 else tuple(r_list)

    @o.setter
    def o(self, array_like) -> None:

        ikkf = self.pars["IKKF"].value.split(",")  # get ordinate type: real or complex

        if len(ikkf) == 1:
            tmp_arrays = [np.array(array_like)]
        else:
            tmp_arrays = [np.array(a) for a in array_like]

        # raise error if wrong number of data sets is provided
        if not len(tmp_arrays) == len(ikkf):
            err_msg = "Need exactly {0} ordinate data sets, only {1} given."
            raise ValueError(err_msg.format(len(ikkf), len(tmp_arrays)))

        for i in range(len(ikkf)):

            if not tmp_arrays[i].shape == self._o.shape:
                err_msg = (
                    "Ordinate array must have the shape {0!r} to match the "
                    "axis data."
                )
                raise ValueError(err_msg.format(self._o.shape))

            if ikkf[i] == "CPLX":
                self._o["o%s real" % i] = tmp_arrays[i].real
                self._o["o%s imag" % i] = tmp_arrays[i].imag
            else:
                self._o["o%s real" % i] = tmp_arrays[i].real

            self._dta = self._o.flatten()

    def load(self, path: str) -> None:
        """
        Loads data and parameters from a '.DSC' file and accompanying data files.

        :param str path: Path to '.DSC' file or accompanying data files to load. Any of
            those file paths can be given, the other files belonging to the same data set
            will be found automatically if in the same directory.
        """

        path = os.path.expanduser(path)
        base_path = path.split(".")[0]

        dsc_path = base_path + ".DSC"

        if not os.path.isfile(dsc_path):
            raise ValueError("No such file: %s" % dsc_path)

        self._load_dsc(base_path)
        self._load_dta(base_path)

    def _load_dsc(self, base_path: str) -> None:

        dsc_path = base_path + ".DSC"

        with open(dsc_path, "r") as f:
            self._dsc = f.read()

        # separate layer sections, delimited by '#'
        layer_strings = self._dsc.split("#")[1:]

        # read layer sections
        for string in layer_strings:
            # separate strings into header and body
            head, sep, tail = string.partition("\n")
            # identify layer type and format version from header
            layer_type, version = head.split()[0:2]

            # check if type and version are supported, raise error or warn otherwise
            if layer_type not in self.param_layers.keys():
                raise IOError(
                    'Parameter layer "{0}" not recognized.'.format(layer_type)
                )
            if version not in self.param_layers[layer_type].SUPPORTED_VERSIONS:
                print(
                    "Version {0} of {1} format is not ".format(version, layer_type)
                    + "supported. You may encounter parsing errors and data corruption."
                )

            # parse content to respective parameter layer objects
            self.param_layers[layer_type].from_string(tail)
            self.param_layers[layer_type].VERSION = version

        # determine byte order of data from DSC file
        if self.pars["BSEQ"].value == "BIG":
            self._byte_order = ">"
        elif self.pars["BSEQ"].value == "LIT":
            self._byte_order = "<"
        else:
            raise IOError("Byte-order of data file is not supported.")

    def _get_dta_dtype(self) -> List[Tuple[str, str]]:

        # determine if acquired quantities are real or complex
        ikkfs = self.pars["IKKF"].value.split(",")

        # determine type of data: int 32-bit, float 32-bit or float 64-bit
        if "CPLX" in ikkfs:
            irfmts = self.pars["IRFMT"].value.split(",")
            iifmts = self.pars["IRFMT"].value.split(",")
        else:
            irfmts = self.pars["IRFMT"].value.split(",")
            iifmts = len(irfmts) * ["0"]

        # convert to numpy data types
        try:
            dtypes_real = [self.IRFMTS_DICT[irfmt] for irfmt in irfmts]
            dtypes_imag = [self.IRFMTS_DICT[iifmt] for iifmt in iifmts]
        except KeyError:
            raise IOError(
                "Data file has a not-supported data-type. Data type must "
                + "be double (64-bit), float(32-bit), or int (32-bit)."
            )

        # assert that we have data types for each quantity
        assert len(dtypes_real) == len(ikkfs)
        assert len(dtypes_imag) == len(ikkfs)

        # create lists containing field names and numpy data types
        field_names = []
        data_types = []
        for n, dtype_r, dtype_i in zip(range(len(ikkfs)), dtypes_real, dtypes_imag):
            data_types.append(self._byte_order + dtype_r)
            field_names.append("o%s real" % n)
            if not dtype_i == "":
                data_types.append(self._byte_order + dtype_i)
                field_names.append("o%s imag" % n)

        # return list of tuples (field name, data type)
        return list((fn, dt) for fn, dt in zip(field_names, data_types))

    def _get_axis_dtype(self, axis: str = "x") -> str:

        # determine type of data: int 32-bit, float 32-bit or float 64-bit
        par_name = axis.capitalize() + "FMT"
        try:
            dtype = self.IRFMTS_DICT[self.pars[par_name].value]
        except KeyError:
            raise IOError(
                "Axis data file has a not-supported data-type. Data type "
                + "must be double (64-bit), float(32-bit), or int (32-bit)."
            )
        return self._byte_order + dtype

    def _load_dta(self, base_path: str) -> None:

        dta_path = base_path + ".DTA"
        fmt = self._get_dta_dtype()

        self._dta = np.fromfile(dta_path, fmt)

        if self.pars["XTYP"].value == "IDX":  # indexed data
            ax_min = self.pars["XMIN"].value
            ax_max = ax_min + self.pars["XWID"].value
            ax_pts = self.pars["XPTS"].value
            self._x = np.linspace(ax_min, ax_max, ax_pts)
        elif self.pars["XTYP"].value == "IGD":  # data points saved in file
            fmt = self._get_axis_dtype("X")
            self._x = np.fromfile(base_path + ".XGF", fmt)
        elif self.pars["XTYP"].value == "NTUP":  # currently not supported
            raise IOError("Tuple data is currently not supported by XeprData.")

        if self.pars["YTYP"].value == "IDX":  # indexed data
            ax_min = self.pars["YMIN"].value
            ax_max = ax_min + self.pars["YWID"].value
            ax_pts = self.pars["YPTS"].value
            self._y = np.linspace(ax_min, ax_max, ax_pts)
        elif self.pars["YTYP"].value == "IGD":  # data points saved in file
            fmt = self._get_axis_dtype("Y")
            self._y = np.fromfile(base_path + ".YGF", fmt)
        elif self.pars["YTYP"].value == "NTUP":  # currently not supported
            raise IOError("Tuple data is currently not supported by XeprData.")

        if self.pars["ZTYP"].value == "IDX":  # indexed data
            ax_min = self.pars["ZMIN"].value
            ax_max = ax_min + self.pars["ZWID"].value
            ax_pts = self.pars["ZPTS"].value
            self._z = np.linspace(ax_min, ax_max, ax_pts)
        elif self.pars["ZTYP"].value == "IGD":  # data points saved in file
            fmt = self._get_axis_dtype("Z")
            self._z = np.fromfile(base_path + ".ZGF", fmt)
        elif self.pars["ZTYP"].value == "NTUP":  # currently not supported
            raise IOError("Tuple data is currently not supported by XeprData.")

        if self._z.size > 0:
            self._o = self._dta.reshape(self.z.size, self.y.size, self.x.size)
        elif self._y.size > 0:
            self._o = self._dta.reshape(self.y.size, self.x.size)
        else:
            self._o = self._dta

    def save(self, path: str) -> None:
        """
        Saves data and parameters to a '.DSC' file and accompanying data files.

        :param str path: Path to '.DSC' file or accompanying data files to save. Any of
            those file paths can be given, the other file names will be generated as
            necessary.
        """

        path = os.path.expanduser(path)
        base_path = path.split(".")[0]

        dsc_path = base_path + ".DSC"
        dta_path = base_path + ".DTA"

        self._dsc = self.print_dsc()

        with open(dsc_path, "w") as f:
            f.write(self._dsc)

        self._dta.tofile(dta_path)

        if self.pars["XTYP"].value == "IGD":
            self._x.tofile(base_path + ".XGF")

        if self.pars["YTYP"].value == "IGD":
            self._y.tofile(base_path + ".YGF")

        if self.pars["ZTYP"].value == "IGD":
            self._z.tofile(base_path + ".YGF")

    def print_dsc(self) -> str:
        """
        Parses all parameters as '.DSC' file content and returns the result as a string.

        :return: String containing all parameters in '.DSC' file format.
        :rtype: str
        """

        lines = []

        for layer in self.param_layers.values():
            if len(layer.groups) > 0:
                lines.append(layer.to_string())

        lines[-1] = lines[-1].strip("*")

        return "\n".join(lines)

    def plot(self) -> None:
        """
        Plots all recorded spectra / sweeps as 2D or 3D plots. Requires matplotlib.
        """

        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
        except ImportError:
            raise ImportError("Install matplotlib to support plotting.")

        fig = plt.figure()

        x_label = "{} [{}]".format(self.pars["XNAM"].value, self.pars["XUNI"].value)

        if self.y.size == 0:
            ax = fig.add_subplot(111)
            ax.autoscale(axis="x", tight=True)
            if isinstance(self.o, tuple):
                for o in self.o:
                    ax.plot(self.x, o)
            else:
                ax.plot(self.x, self.o)

            y_label = self.pars["IRNAM"].value
            ax.set_xlabel(x_label.replace("'", ""))
            ax.set_ylabel(y_label.replace("'", ""))
        else:
            ax = fig.add_subplot(111, projection="3d")
            ax.autoscale(axis="x", tight=True)

            for y_point, z_data in zip(self.y, self.o):
                y_data = np.full_like(self.x, y_point)
                if isinstance(z_data, tuple):
                    for z in z_data:
                        ax.plot(self.x, y_data, z)
                else:
                    ax.plot(self.x, y_data, z_data)

            y_label = "{} [{}]".format(self.pars["YNAM"].value, self.pars["YUNI"].value)
            z_label = self.pars["IRNAM"].value

            ax.set_xlabel(x_label.replace("'", ""))
            ax.set_ylabel(y_label.replace("'", ""))
            ax.set_zlabel(z_label.replace("'", ""))

        fig.tight_layout()
        fig.show()

    def is_1d(self) -> bool:
        return len(self.shape) == 1

    def is_2d(self) -> bool:
        return len(self.shape) == 2

    def is_3d(self) -> bool:
        return len(self.shape) == 3

    def is_pulsed(self) -> bool:
        dsl = self.param_layers.get("DSL")
        if dsl:
            return "ftEpr" in dsl.groups
        else:
            return False

    def is_cw(self) -> bool:
        dsl = self.param_layers.get("DSL")
        if dsl:
            return "ftEpr" not in dsl.groups
        else:
            return False

    def __repr__(self) -> str:
        return "<{0}({1})>".format(self.__class__.__name__, self.pars["TITL"].value)
