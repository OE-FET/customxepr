 1/1: clear
 1/2: !conda install matplotlib
 1/3: !conda install pyvisa
 1/4: !conda install yagmail
 1/5: !conda install -c jrkerns yagmail
 2/1: import matplotlib
 2/2: import decorator
 2/3: import pyvisa
 2/4: import qtpy
 2/5: import lmfit
 2/6: import numpy
 2/7: import pyenchant
 2/8: import pyenchant
 2/9: clear
2/10: import pip install pyenchant
2/11: import pyenchant
2/12: import yagmail
2/13: import pyqtgraph
2/14: import pyqtgraph
2/15: clear
2/16: import
2/17: import qdarkstyle
2/18: import jupyter_qtconsole_colorschemes
 3/1: import pyqtgraph
 3/2: import pyenchant
 3/3: clear
 3/4: import pyqtgraph
 3/5: import pyenchant
 3/6: import enchant
 3/7: clear
 5/1: clear
 9/1: tmp = [5, 10, 20, 30, 50, 80, 110, 140, 170, 200, 230, 260, 290]
 9/2: tmp.reverse()
 9/3: tmp
 9/4: clc
 9/5: clear
12/1: clear
13/1: clear
14/1: clear
15/1: 3 <=3
15/2: clear
16/1: clear
17/1: clear
17/2: cmp(0,1)
17/3: clear
20/1: clear
20/2: import maplotlib
20/3: clear
20/4: import matplotlib
20/5: import decorator
20/6: import qtpy
20/7: import lmfit
20/8: import numpy
20/9: iport pyenchant
20/10: import pyenchant
20/11: clear
20/12:
from pkgutil import iter_modules
modules = set(x[1] for x in iter_modules())

with open('Dependencies.txt', 'rb') as f:
    for line in f:
        requirement = line.rstrip()
        if not requirement in modules:
            print requirement
20/13: modules
20/14: clear
20/15:
ith open('Dependencies.txt', 'rb') as f:
    for line in f:
        requirement = line.rstrip()
        if not requirement in modules:
            print requirement
20/16: clear
20/17:
from pkgutil import iter_modules
modules = set(x[1] for x in iter_modules())

with open('Dependencies.txt', 'rb') as f:
    for line in f:
        requirement = line.rstrip()
        if not requirement in modules:
            print requirement
20/18: clear
20/19:
modules = set(x[1] for x in iter_modules())

with open('Dependencies.txt', 'rb') as f:
    for line in f:
        requirement = line.rstrip()
        if not requirement in modules:
            print requirement
20/20: !pip install pyenchant
20/21: clear
20/22:
from pkgutil import iter_modules
modules = set(x[1] for x in iter_modules())

with open('dependencies.txt', 'rb') as f:
    for line in f:
        requirement = line.rstrip()
        if not requirement in modules:
            print('Error: could not find module ' + requirement + '.\nPlease' +
                  'install to run CustomXepr.')
20/23: clear
20/24: import os
20/25: os.path.join(direct, 'mpl_dark_style.mplstyle')
20/26: clear
20/27:
with open('dependencies.txt', 'rb') as f:
    for line in f:
        requirement = line.rstrip()
        if not requirement in modules:
            print('Error: could not find module ' + requirement + '.\nPlease' +
                  'install to run CustomXepr.')
20/28: clear
20/29:
with open('dependencies.txt', 'rb') as f:
    for line in f:
        requirement = line.rstrip()
        if not requirement in modules:
            print('Error: could not find module ' + requirement + '.\nPlease' +
                  ' install to run CustomXepr.')
20/30:
with open('dependencies.txt', 'rb') as f:
    for line in f:
        requirement = line.rstrip()
        if not requirement in modules:
            print('Error: could not find module ' + requirement + '. Please ' +
                  'install to run CustomXepr.')
20/31: import pyenchant
20/32: clear
20/33: !pip install pyenchant
20/34: clear
20/35:
with open('dependencies.txt', 'rb') as f:
    for line in f:
        requirement = line.rstrip()
        if not requirement in modules:
            print('Error: Could not find module ' + requirement + '. Please ' +
                  'install to run CustomXepr.')
20/36: clear
20/37: errorCount +=1
20/38: errorCount = 0
20/39: errorCount +=1
20/40: errorCount
20/41: clear
20/42: from HelpFunctions import check_dependencies
20/43: exit_code = check_dependencies('dependencies.txt')
20/44: exit_code
20/45: exit_code = check_dependencies('dependencies.txt')
20/46: from HelpFunctions import check_dependencies
20/47: exit_code = check_dependencies('dependencies.txt')
21/1:
from HelpFunctions import check_dependencies
exit_code = check_dependencies('dependencies.txt')
21/2: import pyenchant
21/3: clear
21/4: exit_code = check_dependencies('dependencies.txt')
21/5: exit_code
21/6: clear
22/1:
if exit_code >0:
    return
22/2: clear
24/1: clear
24/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
25/1: clear
25/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
25/3: clear
25/4: customXeprGUI.resultQueueDisplay.selectedIndexes()
25/5: clear
26/1: clear
26/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
26/3: clear
26/4: logger = logging.getLogger('XeprTools.CustomXepr')
26/5: logger.warning("Temperature is taking too long to stablize")
26/6: clear
26/7: logger.warning("Mercury iTC: Temperature is stable at 260K")
26/8: clear
26/9: logger.info("Tuning")
26/10: logger.info("Tuning")
26/11: logger.info("Reading Q-value.")
26/12: logger.info("Q = 8220.")
26/13: logger.info("Measurement "Experiment" running. Estimated time: 18 min, ETA: 14:49.")
26/14: clear
26/15: logger.info('Measurement "Experiment" running. Estimated time: 18 min, ETA: 14:49.')
26/16: logger.info('Temperature stable at (260.00±0.04)K during scans.')
26/17: logger.info('All scans complete.')
26/18: logger.info('Data saved to /home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG_260K')
26/19: clear
26/20: customXepr.setTemperature(290)
26/21: customXepr.setTemperature(290)
26/22: customXepr.customtune()
26/23: customXepr.customtune()
26/24: customXepr.getQValueCalc(290)
26/25: customXepr.runExperiment(Exp, ModAmp=1.2, NbScansToDo=12,PowerAtten=20)
26/26: Exp = 'Exp'
26/27: customXepr.runExperiment(Exp, ModAmp=1.2, NbScansToDo=12,PowerAtten=20)
26/28: logger.status('PAUSED')
26/29: clear
26/30: from XeprTools import ModePictureClass.ModePicture as ModePicture
26/31: from XeprTools import ModePicture
26/32: clear
26/33: modePic = ModePicture()
26/34: customXepr.result_queue.put(modePic)
26/35: clear
26/36: goBright()
26/37: goDark()
26/38: clear
26/39: from XeprTools import ModePicture
26/40: modePic = ModePicture()
26/41: customXepr.result_queue.put(modePic)
26/42: ipython.magic("%autoreload 1")
26/43: modePic = ModePicture()
26/44: customXepr.result_queue.put(modePic)
26/45: customXeprGUI.show()
26/46: goBright()
26/47: clear
27/1: clear
27/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
27/3: goDark()
27/4: clear
27/5: logger = logging.getLogger('XeprTools.CustomXepr')
27/6:
logger.warning("Temperature is taking too long to stablize")
clear
logger.warning("Mercury iTC: Temperature is stable at 260K")
clear
logger.info("Tuning")
logger.info("Reading Q-value.")
logger.info("Q = 8220.")
logger.info('Measurement "Experiment" running. Estimated time: 18 min, ETA: 14:49.')
logger.info('Temperature stable at (260.00±0.04)K during scans.')
logger.info('All scans complete.')
logger.info('Data saved to /home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG_260K')
customXepr.setTemperature(290)
customXepr.customtune()
customXepr.getQValueCalc(290)
Exp = 'Exp'
customXepr.runExperiment(Exp, ModAmp=1.2, NbScansToDo=12,PowerAtten=20)
logger.status('PAUSED')
27/7: clear
27/8:
logger.warning("Temperature is taking too long to stablize")
logger.warning("Mercury iTC: Temperature is stable at 260K")
logger.info("Tuning")
logger.info("Reading Q-value.")
logger.info("Q = 8220.")
logger.info('Measurement "Experiment" running. Estimated time: 18 min, ETA: 14:49.')
logger.info('Temperature stable at (260.00±0.04)K during scans.')
logger.info('All scans complete.')
logger.info('Data saved to /home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG_260K')
customXepr.setTemperature(290)
customXepr.customtune()
customXepr.getQValueCalc(290)
Exp = 'Exp'
customXepr.runExperiment(Exp, ModAmp=1.2, NbScansToDo=12,PowerAtten=20)
logger.status('PAUSED')
27/9: clear
27/10:
from XeprTools import ModePicture
modePic = ModePicture()
customXepr.result_queue.put(modePic)
28/1: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
28/2: goDark()
28/3: clear
28/4:
logger.info("Tuning")
logger.info("Reading Q-value.")
logger.info("Q = 8220.")
logger.info('Measurement "Experiment" running. Estimated time: 18 min, ETA: 14:49.')
logger.info('Temperature stable at (260.00±0.04)K during scans.')
logger.info('All scans complete.')
logger.info('Data saved to /home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG_260K')
28/5: logger = logging.getLogger('XeprTools.CustomXepr')
28/6: clear
28/7:
logger.info("Tuning")
logger.info("Reading Q-value.")
logger.info("Q = 8220.")
logger.info('Measurement "Experiment" running. Estimated time: 18 min, ETA: 14:49.')
logger.info('Temperature stable at (260.00±0.04)K during scans.')
logger.info('All scans complete.')
logger.info('Data saved to /home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG_260K')
28/8:
customXepr.setTemperature(290)
customXepr.customtune()
customXepr.getQValueCalc(290)
Exp = 'Exp'
customXepr.runExperiment(Exp, ModAmp=1.2, NbScansToDo=12,PowerAtten=20)
logger.status('PAUSED')
28/9: clear
28/10:
from XeprTools import ModePicture
modePic = ModePicture()
customXepr.result_queue.put(modePic)
28/11: clear
28/12: logger.status('PAUSED')
28/13: clear
28/14: customXeprGUI.show()
28/15: clear
28/16: keithleyGUI._gui_state_idle()
28/17: keithleyGUI.led.setChecked(True)
28/18: customXeprGUI.show()
28/19: goBright()
28/20: logging.status('PAUSED')
28/21: logger.status('PAUSED')
28/22: clear
28/23: from Keithley import SweepData
28/24: sweepData = SweepData()
28/25: goDark()
28/26: customXeprGUI.show()
28/27: clear
28/28: np
28/29: clear
28/30: import nupy as np
28/31: import numpy as np
28/32: clesr
28/33: clear
28/34:
if filepath is None:
    text = 'Please select file with mode IV curve data:'
    filepath = QtWidgets.QFileDialog.getOpenFileName(caption=text)
    filepath = filepath[0]
28/35: filepath=None
28/36: clear
28/37:
if filepath is None:
    text = 'Please select file with mode IV curve data:'
    filepath = QtWidgets.QFileDialog.getOpenFileName(caption=text)
    filepath = filepath[0]
28/38: clear
28/39: len(filepath)
28/40: data_matrix = np.loadtxt(filepath, skiprows=3)
28/41: data_matrix
28/42: clear
28/43: data_matrix = np.loadtxt(filepath, skiprows=2)
28/44:
with open(filepath) as f:
    info_string = f.readline().strip()
28/45: info_string
28/46: info_string.find('transfer')
28/47: info_string.find('output')
28/48: clear
28/49: data_matrix = np.loadtxt(filepath, skiprows=1)
28/50: clear
28/51:
# get info string and header
with open(filepath) as f:
    info_string = f.readline().strip()
    header = f.readline().strip()
28/52: header
28/53: info_string
28/54: clear
28/55: Vg = data_matrix[:, 0]
28/56: Vg
28/57: clear
28/58: data_matrix
28/59: clear
28/60: len(data_matrix)
28/61: data_matrix.size()
28/62: data_matrix.size
28/63: clear
28/64: data_matrix.shape
28/65: data_matrix.shape[1]
28/66: nStep = (data_matrix.shape[1] - 1/2)
28/67: nStep
28/68: nStep = (data_matrix.shape[1] - 1)/2
28/69: clear
28/70: nStep
28/71:
def _find_floats(self, string):
    """
    Finds all floats in a string, for example in a header from a txt file.
    """
    list_of_floats = []
    for t in string.split():
        try:
            list_of_floats.append(float(t))
        except ValueError:
            pass

    return list_of_floats
28/72:
def _find_floats(string):
    """
    Finds all floats in a string, for example in a header from a txt file.
    """
    list_of_floats = []
    for t in string.split():
        try:
            list_of_floats.append(float(t))
        except ValueError:
            pass

    return list_of_floats
28/73: _find_floats(header)
28/74: header
28/75: header.split()
28/76: clear
28/77: re.findall(r'\d+', header)
28/78: import re
28/79: re.findall(r'\d+', header)
28/80: clear
28/81: re.findall(r'-\d+', header)
28/82: re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", header)
28/83: fmt = "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?"
28/84: fmt
28/85: string_list = re.findall(fmt, header)
28/86: string_list
28/87: clear
28/88: float(string_list)
28/89: float_list = [float(s) for s in string_list]
28/90: float_list
28/91: clear
28/92: len(data_matrix)
28/93: range(1,nStep)
28/94: range(1,nStep+1)
28/95: range(1,nStep+2,2)
28/96: range(1,nStep+2,2) +
28/97: range(1,nStep+2,2) +1
28/98: clear
28/99: range(1,2*nStep,2) +
28/100: clear
28/101: range(1,2*nStep,2)
28/102: range(1,2*4,2)
28/103: clear
28/104: i = 0
28/105: i + 1
28/106: 2*(i + 1)
28/107: 2*i
28/108: 2*i + 3
28/109: i + 2*nStep
28/110: i + nStep
28/111: i + 1 + nStep
28/112: nStep = 4
28/113: nStep = 3
28/114: i+1
28/115: i + 1 + nStep
28/116: i = 1
28/117: i+1
28/118: i + 1 + nStep
28/119: clear
28/120: np.ones(len(data_matrix))
28/121: np.ones(3)
28/122: np.ones(len(data_matrix)) * -5
28/123: clear
28/124: np.ones(len(data_matrix)) * .vStep[i]
28/125: vStep = _find_numbers(header)
28/126:
def _find_numbers(string):
    """
    Finds all numbers in a string, for example in a header from a txt file.
    """
    fmt = '[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?'
    string_list = re.findall(fmt, header)
    float_list = [float(s) for s in string_list]

    return float_list
28/127: clear
28/128: vStep = _find_numbers(header)
28/129: vStep
28/130: clear
28/131: Vd = np.ones(len(data_matrix)) * vStep[i]
28/132: Vd
28/133: clear
28/134: i
28/135: clear
28/136: i
28/137: clear
28/138:
keithleyGUI._gui_state_idle()
keithleyGUI.led.setChecked(True)
29/1: clear
29/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
29/3: clear
29/4: goDark()
29/5:
keithleyGUI._gui_state_idle()
keithleyGUI.led.setChecked(True)
29/6: clear
29/7: keithleyGUI.sweepData = SweepData()
29/8: from Keithley import SweepData
29/9: keithleyGUI.sweepData = SweepData()
29/10: keithleyGUI.sweepData.load()
29/11: keithleyGUI.plot_new_data()
29/12: sd = keithleyGUI.sweepData
29/13: clear
29/14: sd.vStep
29/15: sd.nStep
29/16: clear
29/17: sd.load()
29/18: sd.vStep
29/19: sd.sweepType
29/20:
filepath = QtWidgets.QFileDialog.getOpenFileName(caption=text)
filepath = filepath[0]
29/21: clear
29/22:
text = 'Please select file with mode IV curve data:'
filepath = QtWidgets.QFileDialog.getOpenFileName(caption=text)
filepath = filepath[0]
29/23:
info_string = f.readline().strip()
header = f.readline().strip()
29/24: clear
29/25:
with open(filepath) as f:
    info_string = f.readline().strip()
    header = f.readline().strip()
29/26: info_string
29/27: header
29/28: data_matrix = np.loadtxt(filepath, skiprows=2)
29/29: import numpy as np
29/30: import re
29/31: clear
29/32: data_matrix = np.loadtxt(filepath, skiprows=2)
29/33: (data_matrix.shape[1] - 1)/2
29/34: vStep = self._find_numbers(header)
29/35: sd.vStep = sd._find_numbers(header)
29/36: sd.vStep
29/37: Vg = data_matrix[:, 0]
29/38: sd.nStep = (data_matrix.shape[1] - 1)/2
29/39: self = sd
29/40: clear
29/41:
for i in range(0, self.nStep):
    Id = data_matrix[:, i + 1]
    Ig = data_matrix[:, i + 1 + self.nStep]
    Vd = np.ones(len(data_matrix)) * self.vStep[i]
29/42:
for i in range(0, self.nStep):
    Id = data_matrix[:, i + 1]
    Ig = data_matrix[:, i + 1 + self.nStep]
    Vd = np.ones(len(data_matrix)) * self.vStep[i]
    self.append(Vg, Vd, Ig, Id)
29/43: self._updateVstep()
29/44: keithleyGUI.plot_new_data()
29/45: clear
29/46: keithleyGUI.sweepData.nStep
29/47: keithleyGUI.sweepData.vStep
29/48: header
29/49: i = 0
29/50: self.vStep[i]
29/51: self.vStep = self._find_numbers(header)
29/52: self.vStep[i]
29/53: clear
29/54:
if info_string.find('transfer') > 0:
    self.sweepType = 'transfer'
    self.nStep = (data_matrix.shape[1] - 1)/2
    self.vStep = self._find_numbers(header)
    Vg = data_matrix[:, 0]

    for i in range(0, self.nStep):
        Id = data_matrix[:, i + 1]
        Ig = data_matrix[:, i + 1 + self.nStep]
        Vd = np.ones(len(data_matrix)) * self.vStep[i]
        self.append(Vg, Vd, Ig, Id)
29/55: self._updateVstep()
29/56: keithleyGUI.plot_new_data()
30/1: clear
30/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
30/3: clear
30/4: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
30/5: clear
30/6: xit
31/1: clear
31/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
31/3: clear
31/4: self = keithleyGUI.sweepData
31/5: clear
31/6:
if filepath is None:
    text = 'Please select file with mode IV curve data:'
    filepath = QtWidgets.QFile
31/7: clear
31/8:
text = 'Please select file with mode IV curve data:'
filepath = QtWidgets.QFileDialog.getOpenFileName(caption=text)
filepath = filepath[0]
31/9: clear
31/10:
with open(filepath) as f:
    info_string = f.readline().strip()
    header = f.readline().strip()
31/11: info_string
31/12: header
31/13: data_matrix = np.loadtxt(filepath, skiprows=2)
31/14: import numpy as np
31/15: import re
31/16: clear
31/17: data_matrix = np.loadtxt(filepath, skiprows=2)
31/18: data_matrix
31/19: clear
31/20: self.sweepType = 'transfer'
31/21: self.nStep = (data_matrix.shape[1] - 1)/2
31/22: self.nStep
31/23: self.vStep = self._find_numbers(header)
31/24: self.vStep
31/25: Vg = data_matrix[:, 0]
31/26: Vg
31/27: clear
31/28: i = 0
31/29: Id = data_matrix[:, i + 1]
31/30: Id
31/31: Ig = data_matrix[:, i + 1 + self.nStep]
31/32: Ig
31/33: Vd = np.ones(len(data_matrix)) * self.vStep[i]
31/34: Vd
31/35: self.append(Vg, Vd, Ig, Id)
31/36: clear
31/37: clear
32/1: clear
32/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
32/3: clear
32/4: goDark()
32/5: clear
32/6:
keithleyGUI._gui_state_idle()
keithleyGUI.led.setChecked(True)
32/7: clear
32/8: goBright()
32/9: goDark()
32/10: clear
32/11: keithleyGUI.show()
32/12: mercuryGUI
32/13: mercuryGUI.CurrentXData
32/14: clear
32/15: self = mercuryGUI
32/16: clear
32/17: self._display_message('Connection established.')
32/18:
self.connectAction.setEnabled(False)
            self.disconnectAction.setEnabled(True)
            self.modulesAction.setEnabled(True)
            self.readingsAction.setEnabled(True)
32/19:
self.connectAction.setEnabled(False)
self.disconnectAction.setEnabled(True)
self.modulesAction.setEnabled(True)
self.readingsAction.setEnabled(True)
32/20: clear
32/21: self.led.setChecked(True)
32/22: self._check_slots()
32/23: self._connect_slots()
32/24: clear
32/25: self.h1_label.setText('Heater, %s V:' % 24.5)
32/26: self.h1_label.setText('Heater, %s V:' % 24.23)
32/27: self.h1_label.setText('Heater, %s V:' % 24.230086)
32/28: self.g1_label.setText('Gas flow (min = %s%%):' % 18)
32/29: self.gf_label.setText('Gas flow (min = %s%%):' % 18)
32/30: self.gf1_label.setText('Gas flow (min = %s%%):' % 18)
32/31: self.t1_reading.setText('289.99')
32/32: round(289.998, 3)
32/33: self.t1_reading.setText('289.998')
32/34: self.t1_reading.setText('290.001')
32/35: clear
32/36:
if filepath is None:
    text = 'Please select file with mode picture data:'
    filepath = QtWidgets.QFileDialog.getOpenFileName(caption=text)
    filepath = filepath[0]
32/37: clear
32/38:
text = 'Please select file with mode picture data:'
filepath = QtWidgets.QFileDialog.getOpenFileName(caption=text)
filepath = filepath[0]
32/39:
text = 'Please select file with mode picture data:'
filepath = QtWidgets.QFileDialog.getOpenFileName(caption=text)
filepath = filepath[0]
32/40: clear
32/41:
with open(filepath) as f:
    info_string = f.readline().strip()
    header = f.readline().strip()
32/42: info_string
32/43: header
32/44: clear
32/45: data_matrix = np.loadtxt(filepath, skiprows=2)
32/46: import numpy as np
32/47: data_matrix = np.loadtxt(filepath, skiprows=2)
32/48: clear
32/49: data_matrix
32/50: self
32/51: clear
32/52: self.xData = data_matrix[:,0]
32/53: self.yData = data_matrix[:,1]
32/54:
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))
32/55:
# system imports
import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor
32/56: clear
32/57:
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))
32/58: self._update_slider()
32/59: len(self.xData)
32/60: self.xData = self.xData[1:43200]
32/61: self.yData = self.yData[1:43200]
32/62:
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
32/63: clear
32/64:
logger = logging.getLogger('XeprTools.CustomXepr')
logger.warning("Temperature is taking too long to stablize")
clear
logger.warning("Mercury iTC: Temperature is stable at 260K")
clear
logger.info("Tuning")
logger.info("Reading Q-value.")
logger.info("Q = 8220.")
logger.info('Measurement "Experiment" running. Estimated time: 18 min, ETA: 14:49.')
logger.info('Temperature stable at (260.00±0.04)K during scans.')
logger.info('All scans complete.')
logger.info('Data saved to /home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG_260K')
customXepr.setTemperature(290)
customXepr.customtune()
customXepr.getQValueCalc(290)
Exp = 'Exp'
customXepr.runExperiment(Exp, ModAmp=1.2, NbScansToDo=12,PowerAtten=20)
logger.status('PAUSED')
32/65: logger.warning("Mercury iTC: Temperature is stable at 260K")
32/66:
logger.info("Tuning")
logger.info("Reading Q-value.")
logger.info("Q = 8220.")
logger.info('Measurement "Experiment" running. Estimated time: 18 min, ETA: 14:49.')
logger.info('Temperature stable at (260.00±0.04)K during scans.')
logger.info('All scans complete.')
logger.info('Data saved to /home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG_260K')
customXepr.setTemperature(290)
customXepr.customtune()
customXepr.getQValueCalc(290)
Exp = 'Exp'
customXepr.runExperiment(Exp, ModAmp=1.2, NbScansToDo=12,PowerAtten=20)
logger.status('PAUSED')
32/67: clear
32/68:
modePic = ModePicture()
customXepr.result_queue.put(modePic)
32/69: from MercuryGUI import ModePic
32/70: from XeprTools import ModePic
32/71: from XeprTools import ModePicture
32/72: clear
32/73:
modePic = ModePicture()
customXepr.result_queue.put(modePic)
32/74: clear
32/75: clear
32/76: goBright()
32/77: goDark()
32/78: logger.status('PAUSED')
32/79: clear
33/1: clear
34/1: clear
34/2: clear
35/1: clear
36/1: clear
36/2: from Queue import Queue
36/3: testQ = Queue()
36/4: testQ.all_tasks_done()
36/5: testQ.all_tasks_done
36/6: clear
36/7: testQ.unfinished_tasks
36/8: testQ.put(2)
36/9: testQ.unfinished_tasks
36/10: testQ.put(4)
36/11: testQ.unfinished_tasks
36/12: testQ.pop()
36/13: testQ.get()
36/14: testQ.unfinished_tasks
36/15: testQ.task_done()
36/16: testQ.unfinished_tasks
36/17: clear
38/1: clear
40/1: clear
40/2:
from qtpy.QtWidgets import (QAction, QApplication, QDockWidget, QMainWindow,
                            QMenu, QMessageBox, QShortcut, QSplashScreen,
                            QStyleFactory)
40/3: clear
40/4: SPLASH = QSplashScreen()
40/5:
SPLASH_FONT = SPLASH.font()
SPLASH_FONT.setPixelSize(10)
SPLASH.setFont(SPLASH_FONT)
SPLASH.show()
40/6:
SPLASH.showMessage(_("Initializing..."), Qt.AlignBottom | Qt.AlignCenter |
                Qt.AlignAbsolute, QColor(Qt.white))
40/7:
SPLASH.showMessage("Initializing...", Qt.AlignBottom | Qt.AlignCenter |
                Qt.AlignAbsolute, QColor(Qt.white))
40/8:
from qtpy import API, PYQT5
from qtpy.compat import from_qvariant
from qtpy.QtCore import (QByteArray, QCoreApplication, QPoint, QSize, Qt,
                         QThread, QTimer, QUrl, Signal, Slot)
from qtpy.QtGui import QColor, QDesktopServices, QIcon, QKeySequence, QPixmap
from qtpy.QtWidgets import (QAction, QApplication, QDockWidget, QMainWindow,
                            QMenu, QMessageBox, QShortcut, QSplashScreen,
                            QStyleFactory)
40/9:
SPLASH.showMessage(_("Initializing..."), Qt.AlignBottom | Qt.AlignCenter |
                Qt.AlignAbsolute, QColor(Qt.white))
40/10: clear
40/11:
SPLASH.showMessage("Initializing...", Qt.AlignBottom | Qt.AlignCenter |
                Qt.AlignAbsolute, QColor(Qt.white))
40/12: QApplication.processEvents()
40/13: qpxmp = QPixmap('/Users/samschott/Desktop/CustomXeprSplash.pdf')
40/14: qpxmp
40/15: clear
40/16: SPLASH = QSplashScreen(QPixmap('/Users/samschott/Desktop/CustomXeprSplash.pdf'))
40/17:
SPLASH_FONT = SPLASH.font()
SPLASH_FONT.setPixelSize(10)
SPLASH.setFont(SPLASH_FONT)
40/18: SPLASH.show()
40/19: QApplication.processEvents()
40/20: SPLASH = QSplashScreen(QPixmap('/Users/samschott/Desktop/CustomXeprSplash.pdf'), Qt.WindowStaysOnTopHint)
40/21: SPLASH.show()
40/22: SPLASH.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
40/23: SPLASH.show()
40/24: SPLASH = QSplashScreen(QPixmap('/Users/samschott/Desktop/CustomXeprSplash.png'), Qt.WindowStaysOnTopHint)
40/25: SPLASH.show()
40/26: SPLASH = QSplashScreen(QPixmap('/Users/samschott/Desktop/CustomXeprSplash.pdf'), Qt.WindowStaysOnTopHint)
40/27: SPLASH.show()
40/28: SPLASH.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
40/29: clear
40/30: SPLASH.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
40/31: SPLASH.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
40/32: SPLASH.show()
40/33: QApplication
40/34: qapp = QApplication.instance()
40/35: qapp.setAttribute(Qt.AA_UseHighDpiPixmaps)
40/36: clear
40/37: splash = QSplashScreen(QPixmap('/Users/samschott/Desktop/CustomXeprSplash.pdf'), Qt.WindowStaysOnTopHint)
40/38: splash = QSplashScreen(QPixmap('/Users/samschott/Desktop/CustomXeprSplash.png'), Qt.WindowStaysOnTopHint)
40/39: splash.show()
40/40: splash.finish()
40/41: clear
40/42: QtWidgets
40/43: clear
40/44: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
40/45: goDark()
41/1: from qtpy import QtCore, QtWidgets, QtGui
41/2: app = QtCore.QCoreApplication.instance()
41/3: splash = QtWidgets.QSplashScreen(QtGui.QPixmap('/Users/samschott/Desktop/CustomXeprSplash.pdf'))
41/4: splash.show()
41/5: splash.autoFillBackground()
41/6: splash.repaint()
41/7: splash.repaint()
41/8: splash.repaint()
41/9: splash.repaint()
41/10: splash.repaint()
41/11: splash.showMessage("TEST")
41/12: splash.repaint()
41/13: splash.repaint()
41/14: splash.show()
41/15: clear
41/16: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
44/1: clear
44/2: image = QtGui.QPixmap('/Users/samschott/Desktop/CustomXeprSplash.png')
44/3: from qtpy import QtCore, QtWidgets, QtGui
44/4: image = QtGui.QPixmap('/Users/samschott/Desktop/CustomXeprSplash.png')
44/5: image.QPixmap.scaledToWidth
44/6: image.scaledToWidth(800)
44/7: clear
44/8: image.height
44/9: image.height()
44/10: image.scaledToWidth(200)
44/11: image.height()
44/12: image.scaledToHeight(500)
44/13: image.height()
44/14: image = image.scaledToHeight(500)
44/15: image.height()
44/16: clear
44/17: image = QtGui.QPixmap('/Users/samschott/Desktop/CustomXeprSplash.png')
44/18: image.devicePixelRatioFScale
44/19: image.devicePixelRatioFScale()
44/20: image.setDevicePixelRatio(2)
44/21: clear
65/1: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
67/1: clear
67/2: raise('test')
67/3: raise 'test'
67/4:
raise TypeError('"modePicData" must be a dictionary containing the +'
                         'mode pictures for the respective zoom factors.')
67/5: clear
67/6: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
69/1: goBright()
69/2: goDark()
68/1: clear
68/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
68/3: splash
68/4: splash.deleteLaterf
70/1: clear
70/2: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
70/3: customXepr
70/4: customXepr.__version__
70/5: clear
70/6: CustomXepr.__version__
70/7: CustomXepr
70/8: clear
77/1: runfile('/Users/samschott/Dropbox (Cambridge University)/Python/CustomXepr_startup.py', wdir='/Users/samschott/Dropbox (Cambridge University)/Python')
86/1: import os
86/2: clear
86/3: homePath = os.path.expanduser('~')
86/4: homePath
86/5: clear
86/6: homePath
86/7: loggingPath = '/.CustomXepr/LOG_FILES'
86/8: loggingPath
86/9: os.path.join(homePath,loggingPath)
86/10: homePath
86/11: loggingPath
86/12: os.path.join(homePath,'.CustomXepr/LOG_FILES')
86/13: fullPath = os.path.join(homePath, loggingPath)
86/14: fullPath
86/15: loggingPath = '.CustomXepr/LOG_FILES'
86/16: fullPath = os.path.join(homePath, loggingPath)
86/17: fullPath
86/18:
logFile = os.path.join(fullPath, 'root_logger '
                               + time.strftime("%Y-%m-%d_%H-%M-%S"))
86/19: import time
86/20:
logFile = os.path.join(fullPath, 'root_logger '
                               + time.strftime("%Y-%m-%d_%H-%M-%S"))
86/21: logFile
86/22: clear
87/1: clear
97/1: clear
97/2: DEFAULTS = [('main',{'DARK': True}]), ('CustomXepr',{'notify_address':'ss2151@cam.ac.uk','temp_wait_time': 120, 'temperature_tolerance': 0.1}), ('MercuryFeed',{'MERCURY_IP':'172.20.91.43','temperature_module': 1, 'gasflow_module': 1, 'heater_module': 1}), ('Keithley', {'KEITHLEY_IP': '192.168.2.121', 'VgStart': 10, 'VgStop': -60, 'VgStep': 1, 'VdList': [-5, -60], 'VdStart': 0, 'VdStop': -60,  'VdStep': 1, 'VgList': [0, -20, -40, -60], 'tInt': 0.1, 'pulsed': False, 'delay': -1})]
97/3: clear
97/4:
import getpass
username = getpass.getuser()
print username
97/5: repr(3)
97/6: clear
97/7:

import locale
import os.path as osp
import os
import shutil
import sys
import getpass
import tempfile
97/8:
def get_home_dir():
    """
    Return user home directory
    """
    try:
        # expanduser() returns a raw byte string which needs to be
        # decoded with the codec that the OS is using to represent
        # file paths.
        path = encoding.to_unicode_from_fs(osp.expanduser('~'))
    except Exception:
        path = ''

    if osp.isdir(path):
        return path
    else:
        # Get home from alternative locations
        for env_var in ('HOME', 'USERPROFILE', 'TMP'):
            # os.environ.get() returns a raw byte string which needs to be
            # decoded with the codec that the OS is using to represent
            # environment variables.
            path = encoding.to_unicode_from_fs(os.environ.get(env_var, ''))
            if osp.isdir(path):
                return path
            else:
                path = ''

        if not path:
            raise RuntimeError('Please set the environment variable HOME to '
                               'your user/home directory path so Spyder can '
                               'start properly.')
97/9: get_home_dir
97/10: get_home_dir()
97/11: import codecs
97/12: get_home_dir()
97/13: osp
97/14:
def get_home_dir():
    """
    Return user home directory
    """
    try:
        # expanduser() returns a raw byte string which needs to be
        # decoded with the codec that the OS is using to represent
        # file paths.
        path = osp.expanduser('~')
    except Exception:
        path = ''

    if osp.isdir(path):
        return path
    else:
        # Get home from alternative locations
        for env_var in ('HOME', 'USERPROFILE', 'TMP'):
            # os.environ.get() returns a raw byte string which needs to be
            # decoded with the codec that the OS is using to represent
            # environment variables.
            path = encoding.to_unicode_from_fs(os.environ.get(env_var, ''))
            if osp.isdir(path):
                return path
            else:
                path = ''

        if not path:
            raise RuntimeError('Please set the environment variable HOME to '
                               'your user/home directory path so Spyder can '
                               'start properly.')
97/15: get_home_dir()
97/16: clear
97/17: SUBFOLDER = '.CustomXepr'
97/18: conf_dir = osp.join(get_home_dir(), SUBFOLDER)
97/19: conf_dir
97/20: import ConfigParser
97/21: clear
97/22: type('test') is str
97/23: test = unicode(3)
97/24: test
97/25: type(test)
97/26: type(test) is str
97/27: clear
97/28: type(test) is basestring
97/29: isinstance(type, basestring)
97/30: clear
97/31:
# Local import
from Config.base import SUBFOLDER
from Config.user import UserConfig
97/32: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py', wdir='/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config')
97/33: clear
97/34: DefaultsConfig
97/35: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py', wdir='/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config')
97/36: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py', wdir='/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config')
97/37: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py', wdir='/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config')
98/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py', wdir='/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config')
98/2: clear
98/3: from Config.base import SUBFOLDER
99/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py', wdir='/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config')
99/2: clear
99/3: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py')
99/4: clear
99/5: from ConfigParser import ConfigParser
99/6: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py')
99/7: CONF
99/8: CONF.write()
99/9: clear
99/10: CONF.set_as_defaults()
99/11: CONF.get('main','DARK')
99/12: CONF.get('Keithley','KEITHLEY_IP')
99/13: CONF.set('main','DARK',False)
100/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py')
100/2: CONF.set('main','DARK',False)
100/3: clear
100/4: CONF.get('CustomXepr', 'temp_wait_time')
100/5: type(CONF.get('CustomXepr', 'temp_wait_time'))
100/6: clear
100/7: CONF.get('CustomXepr', 'temperature_tolerance')
100/8: clear
100/9: getpass
100/10: import getpass
100/11: getpass.username()
100/12: getpass.getuser()
100/13: clear
100/14: CONF.get('MercuryFeed', 'MERCURY_IP')#
100/15: clear
100/16: CONF.get('Keithley', 'VgList')
100/17: clear
100/18: NOTIFY = [getpass.getuser() + '@cam.ac.uk', ]
100/19: NOTIFY
100/20: clear
100/21: import os
100/22: logFile
100/23:
homePath = os.path.expanduser('~')
loggingPath = '.CustomXepr/LOG_FILES'
100/24: fullPath = os.path.join(homePath, loggingPath)
100/25: import time
100/26: clear
100/27:
logFile = os.path.join(fullPath, 'root_logger '
                       + time.strftime("%Y-%m-%d_%H-%M-%S"))
100/28: logFile
100/29: os.path.dirname(logFile)
100/30: '/'.join(logFile.split('/')[0:-1])
100/31: clear
100/32: homePath = os.path.expanduser('~')
100/33: loggingPath = os.path.join('.CustomXepr', 'LOG_FILES')
100/34: loggingPath
100/35: fullPath = os.path.join(homePath, loggingPath)
100/36: fullPath
100/37: clear
100/38: loggingPath
100/39: os.path.exists(os.path.join(homePath, loggingPath))
100/40: os.path.join(homePath, '.CustomXepr', 'LOG_FILES')
100/41: clear
100/42:
DEFAULTS = [
            ('main',
             {
              'DARK': True
              }),
            ('CustomXepr',
             {
              'notify_address': None,
              'email_handler_level': 40,
              'temp_wait_time': 120,
              'temperature_tolerance': 0.1
              }),
            (
             'MercuryFeed',
             {
              'MERCURY_IP': '172.20.91.43',
              'MERCURY_PORT': '7020',
              'temperature_module': 0,
              'gasflow_module': 0,
              'heater_module': 0
              }),
            ('Keithley',
             {
              'KEITHLEY_IP': '192.168.2.121',
              'VgStart': 10,
              'VgStop': -60,
              'VgStep': 1,
              'VdList': [-5, -60],
              'VdStart': 0,
              'VdStop': -60,
              'VdStep': 1,
              'VgList': [0, -20, -40, -60],
              'tInt': 0.1,
              'pulsed': False,
              'delay': -1
             })
            ]
100/43: DEFAULTS
100/44: clear
100/45: DEFAULTS[1]
100/46: DEFAULTS['Keithley']
100/47: clear
100/48: DEFAULTS[2]
100/49: DEFAULTS[3]
100/50: type(DEFAULTS)
100/51: type(DEFAULTS[3])
100/52: type(DEFAULTS[3][1])
100/53: CONF.sections
100/54: CONF.sections()
100/55: DEFAULTS.sections()
100/56: CONF.get('Keithley')
100/57: CONF.items('Keithley')
100/58: clear
100/59: dict(CONF.items('Keithley'))
100/60: CONF.get('Keithley', 'VgList')
100/61: CONF.get('Keithley', 'vglist')
100/62: test = dict(CONF.items('Keithley'))
100/63: test['VgList']
100/64: test['vglist']
100/65: CONF.optionxform
100/66: CONF.optionxform = str
100/67: dict(CONF.items('Keithley'))
100/68: clear
101/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py')
101/2: clear
101/3: CONF
101/4: dict(CONF.items('Keithley'))
102/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py')
102/2: dict(CONF.items('Keithley'))
102/3: clear
102/4: CONF.get('Keithley', 'VgList')
102/5: clear
102/6: CONF.get('Keithley', 'tInt')
102/7: CONF.get('Keithley', 'VgStep')
102/8: CONF.get('Keithley', 'VgStep')
102/9: CONF.get('Keithley', 'Vd')
102/10: clear
102/11: CONF.get('Keithley', 'KEITHLEY_IP')
102/12: clear
102/13: CONF.get('Keithley', 'gate')
102/14: clear
102/15: VdListString = '-5, trailing'
102/16: VdList = [-5, 'trailing']
102/17: VdList
102/18: str(VdList).strip('[]')
102/19: VdListString = "-5, 'trailing'"
102/20: VdStringList = VdListString.split(',')
102/21: VdStringList
102/22: [float(x) for x in VdStringList]
102/23: VdStringList
102/24: clear
102/25: is_text_string(VdStringList[0])
102/26:
def is_text_string(obj):
    """Return True if `obj` is a text string, False if it is anything else,
    like binary data (Python 3) or QString (Python 2, PyQt API #1)"""
    return isinstance(obj, basestring)
102/27: is_text_string(VdStringList[0])
102/28: is_text_string(VdStringList[1])
102/29: clear
102/30: [float(x) for x in VdStringList]
102/31: clear
102/32: VdStringList[0]
102/33: VdStringList[1].strip()
102/34: VdStringList[1].strip() == 'trailing'
102/35: VdStringList[1].strip() == "'trailing'"
102/36: VdStringList[1].strip().find('trailing')
102/37: clear
103/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py')
104/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Config/main.py')
104/2:

"""
CustomXepr configuration options

Note: Leave this file free of Qt related imports, so that it can be used to
quickly load a user config file
"""

# Local import
from Config.base import SUBFOLDER
from Config.user import UserConfig

# =============================================================================
#  Defaults
# =============================================================================
DEFAULTS = [
            ('main',
             {
              'DARK': True
              }),
            ('CustomXepr',
             {
              'notify_address': None,
              'email_handler_level': 40,
              'temp_wait_time': 120,
              'temperature_tolerance': 0.1
              }),
            (
             'MercuryFeed',
             {
              'MERCURY_IP': '172.20.91.43',
              'MERCURY_PORT': '7020',
              'temperature_module': 0,
              'gasflow_module': 0,
              'heater_module': 0
              }),
            ('Keithley',
             {
              'KEITHLEY_IP': '192.168.2.121',
              'VgStart': 10,
              'VgStop': -60,
              'VgStep': 1,
              'VdList': [-5, -60],
              'VdStart': 0,
              'VdStop': -60,
              'VdStep': 1,
              'VgList': [0, -20, -40, -60],
              'tInt': 0.1,
              'pulsed': False,
              'delay': -1,
              'gate': 'smua',
              'drain': 'smub'
             })
            ]


# =============================================================================
# Config instance
# =============================================================================
# IMPORTANT NOTES:
# 1. If you want to *change* the default value of a current option, you need to
#    do a MINOR update in config version, e.g. from 3.0.0 to 3.1.0
# 2. If you want to *remove* options that are no longer needed in our codebase,
#    or if you want to *rename* options, then you need to do a MAJOR update in
#    version, e.g. from 3.0.0 to 4.0.0
# 3. You don't need to touch this value if you're just adding a new option
CONF_VERSION = '1.0.0'

# Main configuration instance
104/3: clear
104/4:
CONF = UserConfig('CustomXepr', defaults=DEFAULTS, load=True,
                      version=CONF_VERSION, subfolder=SUBFOLDER, backup=True,
                      raw_mode=True)
104/5: CONF.get('MercuryFeed','MERCURY_PORT')
104/6: CONF.set('MercuryFeed','MERCURY_PORT','7020')
104/7: CONF.set('MercuryFeed','MERCURY_PORT','7010')
105/1: clear
105/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
105/3: clear
106/1: clear
106/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
107/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
108/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
108/2: clear
108/3: CONF.get('CustomXepr', 'notify_address')
108/4: CONF.set('CustomXepr', 'notify_address', customXepr.notify_address)
109/1: clear
109/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
110/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
110/2: clear
110/3: goBright()
110/4:

def goDark():
    from Utils import applyDarkTheme

    applyDarkTheme.goDark()
    applyDarkTheme.applyMPLDarkTheme()

    CONF.set('main', 'DARK', True)


def goBright():
    from Utils import applyDarkTheme

    applyDarkTheme.goBright()
    applyDarkTheme.applyMPLBrightTheme()

    CONF.set('main', 'DARK', False)
110/5: clear
110/6: goDark()
110/7: goBright()
110/8: clear
111/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
111/2: clear
112/1: clear
112/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
112/3: clear
113/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
114/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
125/1: import pygments
125/2: pygments.plugin.STYLE_ENTRY_POINT
125/3: pygments.styles.get_style_by_name()
125/4: pygments.styles.get_all_styles()
125/5: pygments.styles.get_all_styles
125/6: pygments.styles
125/7: pygments.styles.get_all_styles()
125/8: help(pygments)
125/9: help(pygments.styles)
125/10: pygments.styles.customxeprdark
125/11: pygments.styles.customxeprdark
125/12: pygments.styles.get_style_by_name(customxeprdark)
125/13: pygments.styles.get_style_by_name('customxeprdark')
125/14: pygments.styles.customxeprdark.CustomxeprdarkStyle
125/15: clear
126/1: import pygments
126/2: pygments.styles.customxeprdark.CustomxeprdarkStyle
126/3: from Utils import CustomxeprdarkStyle
126/4: pygments.styles.customxeprdark = CustomxeprdarkStyle
126/5: pygments.styles.customxeprdark
126/6: pygments.styles.get_style_by_name('customxeprdark')
126/7: pygments.styles.customxeprdark.CustomxeprdarkStyle
126/8: pygments.styles.customxeprdark
126/9: pygments.plugin.find_plugin_styles('customxeprdark')
126/10: clear
126/11: from IPython.qt.console import qtconsoleapp
126/12: from IPython.qtconsole import qtconsoleapp
126/13: import juptyer_client.find_connection_file
126/14: clear
126/15: from juptyer_client import find_connection_file
126/16: from IPython import juptyer_client.find_connection_file
126/17: from IPython.juptyer_client import find_connection_file
126/18: clear
126/19: from XeprTools import InternalIPKernel
126/20: kernel_window = InternalIPKernel()
126/21: kernel_window.init_ipkernel(banner=BANNER)
126/22: clear
126/23: kernel_window.init_ipkernel()
126/24: clear
126/25: kernel_window.new_qt_console()
126/26: kernel_window.init_ipkernel(banner=BANNER)
126/27: kernel_window.init_ipkernel()
126/28: clear
126/29: import pygments
126/30: pygments.get_style-by_name('customxeprdark')
126/31: pygments.styles.get_style_by_name('customxeprdark')
126/32: clear
126/33: pygments.styles.get_style_by_name('customxeprdark')
126/34: pygments.styles.get_style_by_name('bla')
126/35: pygments.ClassNotFound
126/36: pygments.util.ClassNotFound
126/37: clear
126/38:
try:
    pygments.styles.get_style_by_name('bla')
    console_style = 'customxeprdark'
except pygments.util.ClassNotFound:
    console_style = 'native'
126/39: console_style
126/40: clear
126/41:
import os
path = os.path.dirname(pygments.__file__)
126/42: path
126/43: pygments_path = osp.dirname(pygments.__file__)
126/44: import os.path as osp
126/45: clear
126/46: pygments_path = osp.dirname(pygments.__file__)
126/47: style_path = osp.join(pygments_path, 'styles')
126/48: style_path
126/49: import shutil
126/50: osp.dirname(__file__)
126/51: clear
126/52: direct = osp.dirname(os.path.realpath(__file__))
126/53: clear
126/54: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Utils/install_dark_style.py')
126/55: direct
126/56: ource_path = osp.join(direct, 'customxeprdark.py')
126/57: source_path = osp.join(direct, 'customxeprdark.py')
126/58: source_path
126/59: shutil.copy2(source_path, style_path)
126/60: shutil.copy2(source_path, style_path)
126/61: clear
128/1: test = 3
128/2: test
126/62: direct
126/63: install_dark_style()
129/1: test
129/2: test = 2
129/3: test
126/64: clear
126/65: pygments.token.Token.Menu
126/66: install_dark_style()
130/1: test = 2
130/2: test
126/67: pygments.token.Generic.
126/68: pygments.token.Generic
126/69: clear
131/1: n_out += 1  # prevent from warning again next second
131/2: clear
131/3: u'Tempearature fluctuations > \xb1%sK.' % 0.2
131/4: print(u'Tempearature fluctuations > \xb1%sK.' % 0.2)
131/5: n_out = 58
131/6: np.mod(n_out, 60)
131/7: import numpy as np
131/8: clear
131/9: np.mod(n_out, 60)
131/10: n_out = 60
131/11: np.mod(n_out, 60)
131/12: n_out = 61
131/13: np.mod(n_out, 60)
131/14: n_out += 1
131/15: n_out
131/16: np.mod(n_out, 60)
131/17: measurementTemp-np.mean(measurementTemp)
131/18: clear
131/19: np.measurementTemp = np.ones(100)
131/20: measurementTemp = np.ones(100)
131/21: measurementTemp
131/22: measurementTemp = np.ones(100) + measurementTemp = np.ones(100)*1.22
131/23: measurementTemp = np.ones(100) + measurementTemp + np.ones(100)*1.22
131/24: measurementTemp
131/25: clear
131/26: measurementTemp[50:-1] = 5
131/27: measurementTemp
131/28: np.mean(measurementTemp)
131/29: abs(measurementTemp-np.mean(measurementTemp))
131/30: (measurementTemp-np.mean(measurementTemp))
131/31: clear
131/32:
n_out = (abs(measurementTemp-np.mean(measurementTemp)) >
         2*self.temperature_tolerance).sum()
131/33:
n_out = (abs(measurementTemp-np.mean(measurementTemp)) >
         0.2).sum()
131/34: n_out
131/35: clear
131/36: measurementTemp[0]
131/37: clear
131/38:
n_out = (abs(measurementTemp - measurementTemp[0]) >
                         0.2).sum()
131/39: n_out
131/40: np.mod(n_out, 60)
131/41: np.mod(n_out, 120) == 1
131/42:
logger.warning(u'Tempearature fluctuations > \xb1%sK.'
                                   % (2*self.temperature_tolerance))
131/43: clear
131/44: np.mod(121, 120) == 1
131/45: n_out += 1
131/46: n_out
131/47: n_out=121np.mod(121, 120) == 1
131/48: n_out=121
131/49: np.mod(121, 120) == 1
131/50: n_out += 1
131/51: np.mod(121, 120) == 1
131/52: np.mod(n_out, 120) == 1
131/53: n_out
131/54: clear
131/55:
n_out = (abs(measurementTemp - measurementTemp[0]) >
                         2*self.temperature_tolerance).sum()
131/56: clear
131/57: np.mod(n_out, 120) == 0
131/58: np.mod(120, 120) == 0
131/59: np.mod(1, 120) == 0
131/60: np.mod(1, 120) == 1
131/61: clear
131/62: n_out/120
131/63: round(n_out/120)
131/64: n_out
131/65: round(n_out/120)
131/66: clear
131/67:
import time
n_out = 0
for i in range(1,300):
    n_out += 1
    if np.mod(n_out, 120) == 1:
        print(n_out)
    time.sleep(0.2)
131/68:
import time
n_out = 0
for i in range(1,300):
    n_out += 1
    if np.mod(n_out, 120) == 1:
        print(n_out)
131/69: clear
131/70: T_history = np.array([])
131/71:
for i in range(0,300):
    T_history = np.append(T_history, i)
    n_out = (abs(T_history - T_history[0]) >
             2*1).sum()
    if np.mod(n_out, 120) == 1:
        n_out += 1  # prevent from warning again next second
        print(n_out)
131/72: clear
131/73: T_history = np.array([1])
131/74:
n_out = (abs(T_history - T_history[0]) >
                         0).sum()
131/75: n_out
131/76: (abs(T_history - T_history[0]) == 0)
131/77: (abs(T_history - T_history[0]) == 0).sum()
131/78: (abs(T_history - T_history[0]) == 0).sum()
131/79: (abs(T_history - T_history[0]) == 0).sum()
131/80: clear
131/81: clear
131/82: clear
133/1: clear
133/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/3: keithley = Keithley2600()
133/4: keithley.x
133/5: keithley.real_method
133/6: keithley.smua
133/7: keithley.smua.measure
133/8: clear
133/9: keithley.bla(1,2)
133/10: clear
133/11: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/12: keithley = Keithley2600()
133/13: keithley.bla(1,2)
133/14: clear
133/15: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/16: keithley = Keithley2600()
133/17: keithley.bla(1,2)
133/18: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/19: keithley = Keithley2600()
133/20: clear
133/21: keithley.bla(1,2)
133/22: dir(keithley)
133/23: clear
133/24: keithley.smua.bla
133/25: keithley.smua.bla(1,2)
133/26: from unittest.mock import Mock
133/27: clear
133/28: from unittest.mock import Mock
133/29: clear
133/30: from unittest.mock import Mock
133/31: from mock import MagicMock
133/32: clear
133/33: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/34: keithley = Keithley2600()
133/35: keithley.smua.bla
133/36: clear
133/37: from mock import Mock
133/38: test = Mock()
133/39: test.bla
133/40: test.bla(4)
133/41: test.smua.bla
133/42: clear
133/43: test.smua
133/44: test.smua.bla
133/45: test.smua.bla = 0
133/46: test.smua.bla
133/47: test.smua.bla = 3
133/48: test.smua.bla
133/49: test.smua = 3
133/50: test.smua
133/51: test.smua.bla
133/52: clear
133/53: test.smua.bla
133/54: clear
133/55: keithley.smua.bla
133/56: keithley.clear
133/57: clear
133/58: keithley = Keithley2600()
133/59: dir(keithley)
133/60: clear
133/61: keithley.smua.bla
133/62: cleat
133/63: clear
133/64: test.smub
133/65: test.smub.trigger.
133/66: clear
133/67: test.smub.trigger = 0
133/68: test.smub.trigger
133/69: test.smub
133/70: test.smub.sourcev(30)
133/71: clear
133/72: keithley.smua
133/73: keithley.smua = 3
133/74: keithley.smua
133/75: keithley.smua
133/76: clear
133/77: keithley = Keithley2600()
133/78: keithley.smua.bla()
133/79: clear
133/80: keithley.smua.
133/81: keithley.smua.bl
133/82: keithley.smua
133/83: clear
133/84:
keithley.smua(smua
smua
1,2)
133/85: clear
133/86: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/87: keithley = Keithley2600()
133/88: keithley.smub
133/89: keithley.smub.ar
133/90: clear
133/91: test.method.method2
133/92: test.method.method2.method3
133/93: test.method.method2.method3.m4
133/94: test.method.method2.method3.m4(3,4)
133/95: result = test.method.method2.method3.m4(3,4)
133/96: result
133/97: dir(test)
133/98: dir(test.smub)
133/99: dir(test.method)
133/100: clear
133/101: test = Mock()
133/102: from mock import MagicMock
133/103: test = MagicMock()
133/104: clear
133/105: keithley.
133/106: keithley.smua
133/107: keithley.smua(3)
133/108: keithley.smua(3,4)
133/109: keithley.smua.trigger(3,4)
133/110: clear
133/111: dir(keithley)
133/112: keithley.__getattribute__
133/113: clear
133/114: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/115: test = MagicClass()
133/116: test.smua
133/117: clear
133/118: del test
133/119: clear
133/120: keithley
133/121: clear
133/122: test
133/123: keithley
133/124: clear
133/125: keithley.__instance__
133/126: keithley.__str__
133/127: keithley.__name__
133/128: dir(keithley)
133/129: keithley.__repr__
133/130: keithley.__class__
133/131: keithley.__module__
133/132: clear
133/133: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/134: test = MagicClass()
133/135: test(3)
133/136: clear
133/137: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/138: test = MagicClass()
133/139: test(3)
133/140: test.__instance__
133/141: clear
133/142: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/143: test = MagicClass()
133/144: test(3)
133/145: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
133/146: clear
133/147: keithley = MagicClass(name=keithley)
133/148: keithley
133/149: keithley(3)
134/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/2: test = MagicClass()
134/3: clear
134/4: keithley = MagicClass(keithley)
134/5: keithley = MagicClass('keithley')
134/6: assert name is str
134/7: assert 'keithley' is str
134/8: clear
134/9: assert type('keithley') is str
134/10: assert type(3) is str
134/11: clear
134/12: keithley
134/13: keithley.name
134/14: clear
134/15: keithley(3)
134/16: keithley.smua(3)
134/17: keithley.smua
134/18: clear
134/19: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/20: keithley = MagicClass('keithley')
134/21: clear
134/22: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/23: keithley = MagicClass('keithley')
134/24: clear
134/25: keithley(3)
134/26: keithley.smua(3)
134/27: keithley.smua.vlim(3)
134/28: clear
134/29: keithley.smua.vlim
134/30: dir(keithley)
134/31: clear
134/32: dir(keithley)
134/33: clear
134/34: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/35: keithley = MagicClass('keithley')
134/36: clear
134/37: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/38: keithley = MagicClass('keithley')
134/39: clear
134/40: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/41: keithley = MagicClass('keithley')
134/42: clear
134/43: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/44: keithley = MagicClass('keithley')
134/45: clear
134/46: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/47: keithley = MagicClass('keithley')
134/48: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/49: clear
134/50: keithley = MagicClass('keithley')
134/51: clear
134/52: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/53: keithley = MagicClass('keithley')
134/54: keithley.smua.source = 0
134/55: keithley.smua.source
134/56: keithley._name
134/57: keithley.smua
134/58: keithley = MagicClass('keithley')
134/59: clear
134/60: keithley.smua
134/61: keithley.smua =3
134/62: keithley.smua
134/63: keithley = MagicClass('keithley')
134/64: keithley.smua = 3
134/65: keithley.smua
134/66: keithley.__dict__
134/67: keithley.__dict__.keys()
134/68: clear
134/69: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/70: keithley = MagicClass('keithley')
134/71: MagicClass._name
134/72: clear
134/73: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/74: keithley = MagicClass('keithley')
134/75: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/76: keithley = MagicClass('keithley')
134/77: clear
134/78: dir(keithley)
134/79: clear
134/80: __dict__
134/81: keithley.__dict__
134/82: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/83: clear
134/84: keithley = MagicClass('keithley')
134/85: keithley.__dict__
134/86: keithley._name
134/87: clear
134/88: np.__dict__
134/89: clear
134/90: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/91: keithley = MagicClass('keithley')
134/92: keithley._name
134/93: keithley.__dicy__
134/94: keithley.__dicy__
134/95: clear
134/96: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/97: keithley = MagicClass('keithley')
134/98: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/99: clear
134/100: keithley = MagicClass('keithley')
134/101: keithley.__dict__
134/102: keithley
134/103: clear
134/104: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/105: keithley = MagicClass('keithley')
134/106: keithley._name
134/107: keithley.beeper.beep(1, 2400)
134/108: clear
134/109: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/110: keithley = MagicClass('keithley')
134/111: keithley.beeper.beep(1, 2400)
134/112: keithley._name
134/113: clear
134/114: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/115: keithley = MagicClass('keithley')
134/116: keithley.beeper.beep(2,2400)
134/117: keithley.beeper
134/118: cmd = keithley.beeper.beep(2,2400)
134/119: cmd
134/120: clear
134/121: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/122:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
134/123: clear
134/124: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/125:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
134/126: keithley.beeper.enable = 1
134/127: keithley.beeper.enable = 0
134/128: keithley.beeper.enable
134/129: clear
134/130: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
134/131: keithley = MagicClass('keithley')
134/132: keithley.beeper.beep(2,2400)
134/133: keithley.beeper
134/134: keithley.beeper.enable
134/135: clear
134/136: clear
134/137: clear
135/1: clear
135/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/3: keithley = MagicClass('keithley')
135/4: keithley.beeper.beep(2,2400)
135/5: keithley.beeper.beep = 20
135/6: keithley.beeper.enable = 0
135/7: keithley.beeper.enable
135/8: clear
135/9: keithley.beeper.enable
135/10: keithley.beeper.enable._name
135/11: clear
135/12: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/13: keithley = MagicClass('keithley')
135/14: keithley.beeper.beep(2,2400)
135/15: dir(keithley)
135/16: clear
135/17: dir(keithley.beeper)
135/18: clear
135/19: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/20:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
135/21: dir(keithley)
135/22: clear
135/23: keithley
135/24: keithley.beeper
135/25: keithley.beeper.beep
135/26: keithley.beeper.beep(2,2400)
135/27: keithley.beeper
135/28: keithley.beeper.beep
135/29: clear
135/30: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/31: keithley = MagicClass('keithley')
135/32: keithley.beeper.beep(2,2400)
135/33: clear
135/34: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/35:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
135/36: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/37: clear
135/38:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
135/39: keithley.beeper
135/40: keithley.beeper.beep
135/41: keithley.beeper.beep(2,2400)
135/42: keithley.beeper
135/43: keithley.beeper.beep
135/44: clear
135/45: dir(keithley)
135/46: clear
135/47: dir(keithley.beeper)
135/48: clear
135/49: keithley.beeper.beep
135/50: keithley.beep
135/51: clear
135/52: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/53:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
135/54: clear
135/55: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/56:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
135/57: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/58:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
135/59: dir(keithley)
135/60: clear
135/61: keithley.beep
135/62: keithley.beeper.beep
135/63: keithley.beep._name
135/64: keithley.beeper.beep._name
135/65: keithley.beeper.beep(2,120)
135/66: clear
135/67: keithley.beeper.enable =1
135/68: keithley.beeper.enable
135/69: out = keithley.beeper.enable
135/70: out
135/71: clear
135/72: 'test tost'.split()
135/73: dir('test tost')
135/74: clear
135/75: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/76: keithley.beeper.beep(2,2400)
135/77: float(keithley.beeper.enable)
135/78: keithley.beeper.enable
135/79: float(keithley.beeper.enable)
135/80: clear
135/81: float(keithley.beeper.enable)
135/82: clear
135/83: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/84:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
135/85: float(keithley.beeper.enable)
135/86: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/87: clear
135/88:
keithley = MagicClass('keithley')
keithley.beeper.beep(2,2400)
135/89: keithley.beeper.enable = 1
135/90: keithley.beeper.enable.get()
135/91: test = MagicMock()
135/92: from mock import MagicMock
135/93: clear
135/94: test = MagicMock()
135/95: test = MagicMock()
135/96: test.smua
135/97: test.smua.bravo(2,3)
135/98: test.smua.bravo = 2
135/99: test.smua.bravo
135/100: test.smua.bravo(2,3)
135/101: clear
135/102: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/103: keithley = MagicClass('keithley')
135/104: keithley.beeper.beep(2,2400)
135/105: clear
135/106: keithley.beeper.beep
135/107: keithley.beeper.enable
135/108: keithley.beeper.enable = 1
135/109: keithley.beeper.enable
135/110: clear
135/111: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/112: keithley = MagicClass('keithley')
135/113: keithley.beeper.beep(2,2400)
135/114: keithley.beeper.beep(2,2400)
135/115: keithley.beeper.beep(2,2400)
135/116: keithley.beeper.enable =1
135/117: keithley.beeper.enable =1
135/118: clear
135/119: keithley.beeper.enable =1
135/120: keithley.beeper.enable =1
135/121: keithley.__dict__.keys()
135/122: keithley.beeper.__dict__.keys()
135/123: clear
135/124: keithley.beeper.enable =1
135/125: keithley.beeper.enable =1
135/126: keithley.beeper.enable = 1
135/127: keithley.beeper =1
135/128: keithley.beeper
135/129: clear
135/130: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/131: clear
135/132: keithley.beeper.enable = 1
135/133: keithley = MagicClass('keithley')
135/134: keithley.beeper.enable = 1
135/135: clear
135/136: keithley.beeper.enable = 1
135/137: keithley.beeper.enable
135/138: clear
135/139: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/140: keithley = MagicClass('keithley')
135/141: keithley = MagicClass(3)
135/142: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/143: clear
135/144: keithley = MagicClass('keithley')
135/145: keithley
135/146: keithley.beeper.beep(2,3)
135/147: keithley.beeper.enable = 1
135/148: clear
135/149: keithley.beeper.enable
135/150: c = keithley.beeper.enable
135/151: c
135/152: type(c)
135/153: c.split('.')
135/154: clear
135/155: keithley.beeper.enable.get()
135/156: keithley.beeper.enable
135/157: clear
135/158: keithley.beeper.enable
135/159: keithley.beeper.enable = 1
135/160: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/161: keithley = MagicClass('keithley')
135/162: clear
135/163: keithley.beeper.beep(2,3)
135/164: keithley.beeper.enable = 1
135/165: keithley.beeper.enable
135/166: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/167: keithley = MagicClass('keithley')
135/168: keithley.beeper.beep(2,3)
135/169: keithley.beeper.enable = 1
135/170: keithley.beeper.enable
135/171: print
135/172: print keithley.beeper.enable
135/173: clear
135/174: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/175: keithley = MagicClass('keithley')
135/176: keithley.beeper.beep(2,3)
135/177: keithley.beeper.enable = 1
135/178: keithley.beeper.enable
135/179: print keithley.beeper.enable
135/180: clear
135/181: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/182: keithley = MagicClass('keithley')
135/183: keithley.beeper.beep(2,3)
135/184: keithley.beeper.beep(2,3)
135/185: keithley.beeper.enable =1
135/186: keithley.beeper.enable
135/187: clear
135/188: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/189: keithley = MagicClass('keithley')
135/190: keithley
135/191: keithley
135/192: keithley
135/193: clear
135/194: keithley.beeper.enable
135/195: keithley = 3
135/196: clear
135/197: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/198: keithley = MagicClass('keithley')
135/199: clear
135/200: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/201: keithley = MagicClass('keithley')
135/202: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/203: keithley = MagicClass('keithley')
135/204: keithley._name
135/205: clear
135/206: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/207: keithley = MagicClass('keithley')
135/208: keithley
135/209: keithley.beeper
135/210: keithley._name
135/211: clear
135/212: keithley.beeper
135/213: clear
135/214: keithley = MagicClass('keithley')
135/215: keithley.beeper
135/216: keithley
135/217: clar
135/218: clear
135/219: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/220: keithley = MagicClass('keithley')
135/221: keithley.beeper
135/222: keithley.beeper =1
135/223: keithley.beeper = 1
135/224: keithley.beeper.enable
135/225: keithley = MagicClass('keithley')
135/226: keithley.beeper
135/227: keithley.beeper.enable
135/228: keithley.beeper.enable = 1
135/229: keithley.beeper.enable
135/230: keithley.beeper.enable.get()
135/231: cleaer
135/232: clear
135/233: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/234: keithley = MagicClass('keithley')
135/235: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/236: clear
135/237: keithley = MagicClass('keithley')
135/238: keithley
135/239: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/240: keithley = MagicClass('keithley')
135/241: keithley
135/242: keithley.beeper
135/243: keithley.beeper.beep(2,3)
135/244: clear
135/245: keithley.beeper.beep(2,3)
135/246: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/247: keithley = MagicClass('keithley')
135/248: keithley.beeper.beep(2,3)
135/249: clear
135/250: keithley.beeper.enable
135/251: keithley.beeper.enable.get()
135/252: keithley.beeper.enable.set(1)
135/253: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/254: enable = CallableProperty('beeper.enable')
135/255: enable
135/256: clear
135/257: set(3)
135/258: set(1,2,3)
135/259: set([1,3,4])
135/260: a = set([1,3,4])
135/261: a.symmetric_difference()
135/262: clear
135/263: str(True)
135/264: clear
135/265: value = 'ON'
135/266: isinstance(value, str)
135/267: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/268: clear
135/269: keithley = MagicClass('keithley')
135/270: keithley.beeper.beep(1,12400)
135/271: keithley.beeper.enable.get()
135/272: keithley.beeper.enable.get_()
135/273: keithley.beeper.enable.set_(0)
135/274: keithley.beeper.enable.set_('ok')
135/275: clear
135/276: np.arra([1,2,3,4,5])
135/277: clear
135/278: test = np.array([1,2,3,4,5])
135/279: test[0]
135/280: test[-1]
135/281: clear
135/282: n_out = 4
135/283:
n_out += (abs(test[-1] - test[0]) >
                               2)
135/284: n_out
135/285: clear
135/286: keithley.beeper.beep(1,12400)
135/287: keithley.beeper.beep.get_()
135/288: clear
135/289: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/290: FUNCTIONS
135/291: clear
135/292: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/293: keithley = MagicClass('keithley')
135/294: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/295: clear
135/296: keithley = MagicClass('keithley')
135/297: keithley.beeper
135/298: keithley.beeper.beep
135/299: keithley.beeper.beep(1,2000)
135/300: result = keithley.beeper.beep(1,2000)
135/301: result
135/302: clear
135/303: keithley.beeper.beep(1,2000)
135/304: keithley.beeper.enable
135/305: keithley.beeper.enable = 1
135/306: del keithley.beeper.enable
135/307: keithley.beeper.enable
135/308: keithley.smua
135/309: keithley.smua.trigger
135/310: keithley.smua.trigger.endpulse
135/311: keithley.smua.trigger.endpulse.stimulus
135/312: clear
135/313: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/314: keithley = MagicClass('keithley')
135/315: keithley.prop
135/316: keithley.prop(test)
135/317: clear
135/318: keithley.prop = 1
135/319: clear
135/320: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/321: clear
135/322: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/323: keithley = MagicClass('keithley')
135/324: keithley.prop
135/325: keithley.prop = 1
135/326: clear
135/327: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/328: keithley = MagicClass('keithley')
135/329: keithley.prop = 1
135/330: keithley.prop
135/331: keithley.prop = 1
135/332: keithley.prop
135/333: clear
135/334: keithley = MagicClass('keithley')
135/335: keithley.prop
135/336: keithley.beeper.enable =1
135/337: keithley.beeper.enable
135/338: clear
135/339: keithley = MagicClass('keithley')
135/340: keithley.beeper.enable
135/341: del keithley
135/342: clear
135/343: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/344: keithley = MagicClass('keithley')
135/345: keithley.beeper.enable
135/346: keithley.beeper.enable = 1
135/347: clear
135/348: None._write()
135/349: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
135/350: clear
135/351: keithley = MagicClass('keithley')
135/352: keithley.beeper
135/353: keithley.beeper.beep = 1
135/354: keithley.beeper.beep
135/355: keithley = MagicClass('keithley')
135/356: keithley.beeper.beep
136/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
136/2: clear
136/3: keithley = MagicClass('keithley')
136/4: keithley.beeper.beep
136/5: keithley.beeper.enable
136/6: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
136/7: clear
136/8: keithley = MagicClass('keithley')
136/9: keithley.beeper
136/10: keithley.beeper.enable
136/11: keithley.beeper.enable =1
136/12: keithley.beeper.enable
136/13: clear
137/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
137/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
137/3: clear
137/4: keithley = MagicClass('keithley')
137/5: keithley.beeper.enable
137/6: keithley.beeper.enable =1
137/7: keithley.beeper.enable
137/8: keithley.smua.enable
137/9: clear
137/10: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
138/1: clear
138/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
138/3: keithley = MagicClass('keithley')
138/4: keithley.beeper.enable
138/5: keithley.beeper.enable
138/6: keithley.beeper.enable =1
138/7: clear
138/8: keithley.smua.enable
138/9: keithley.smua.enable = 1
138/10: clear
138/11: keithley.smua.enable = 1
138/12: keithley.beeper.enable =1
138/13: keithley.beeper.enable =1
138/14: clear
138/15:
setattr(MagicClass, name,
                    property(fget=self.get_prop, fset=self.set_prop))
138/16: clear
138/17: keithley.smua.beeper.enable
138/18: keithley.smua.beeper
138/19: clear
138/20: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
138/21: keithley = MagicClass('keithley')
138/22: clear
138/23: keithley.beeper.enable
138/24: keithley.beeper.enable = 1
138/25: keithley.beeper.enable = 'ON'
138/26: clear
138/27: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
138/28: keithley = MagicClass('keithley')
138/29: keithley.beeper.enable = 'ON'
138/30: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
138/31: keithley = MagicClass('keithley')
138/32: clear
138/33: keithley.beeper.enable
138/34: keithley.beeper.enable = 1
138/35: keithley.beeper.enable
138/36: keithley.beeper.enable
138/37: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
138/38: clear
138/39: keithley.beeper.enable = 'ON'
138/40: keithley = MagicClass('keithley')
138/41: clear
138/42: keithley.beeper.enable
138/43: keithley.beeper.enable
138/44: keithley.beeper.enable
138/45: keithley.beeper.enable
138/46: keithley.beeper.enable
138/47: clear
138/48: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
138/49: keithley = MagicClass('keithley')
138/50: keithley.beeper.enable
138/51: keithley.beeper.enable = 1
138/52: keithley.beeper.enable = 1
138/53: keithley.beeper.enable = 1
138/54: keithley.beeper.enable = 1
138/55: keithley.beeper.enable = 1
138/56: keithley.beeper.enable = 1
138/57: keithley.beeper.enable = 1
138/58: keithley.beeper.enable = 1
138/59: clear
138/60: keithley.beeper.enable
138/61: keithley.beeper.enable = 1
138/62: clear
138/63: r = 'test'
138/64: float(r)
138/65: r = 'test2'
138/66: float(r)
138/67: r = 'test 2'
138/68: float(r)
138/69: clear
139/1: test = 'True'
139/2: bool(test)
139/3: bool('no')
139/4: bool('yes')
139/5: bool('x')
139/6: bool('xoxo')
139/7: bool('False')
139/8: float('xoxo')
139/9: clear
139/10: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/11: keithley = MagicClass('keithley')
139/12: keithley.smua.measure.v(smua.nvbuffer1)
139/13: clear
139/14: keithley.smua.measure.v('smua.nvbuffer1')
139/15: keithley.smua.measure.v
139/16: v in PROPERTIES
139/17: 'v' in PROPERTIES
139/18: 'v' in FUNCTIONS
139/19: clear
139/20: 'r' in FUNCTIONS
139/21: 'r' in PROPERTIES
139/22: 'p' in PROPERTIES
139/23: 'iv' in PROPERTIES
139/24: 'v' in PROPERTIES
139/25: clear
139/26: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/27: keithley = MagicClass('keithley')
139/28: keithley.smua.measure.v('smua.nvbuffer1')
139/29: "'smua.nvbuffer1',".strip(,)
139/30: clear
139/31: "'smua.nvbuffer1',".strip(",")
139/32: "('smua.nvbuffer1',)".strip(",")
139/33: "('smua.nvbuffer1',)".strip("()")
139/34: "('smua.nvbuffer1',)".strip("()").strip(",")
139/35: clear
139/36: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/37:
keithley = MagicClass('keithley')
keithley.smua.measure.v('smua.nvbuffer1')
139/38:
keithley = MagicClass('keithley')
keithley.smua.measure.v(3,2)
139/39: clear
139/40: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/41:
keithley = MagicClass('keithley')
keithley.smua.measure.v('smua.nvbuffer1')
139/42: clear
139/43: keithley.smua.measure
139/44: keithley.smua.measure.v(2)
139/45: clear
139/46: keithley.smua.measure[2]
139/47: keithley.smua.measure[2].v()
139/48: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/49: keithley = MagicClass('keithley')
139/50: clear
139/51: keithley.trigger.blender[2]
139/52: keithley.trigger.blender[2].orenable
139/53: is 'blender' in FUNCTIONS
139/54: 'blender' in FUNCTIONS
139/55: clear
139/56: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/57: keithley = MagicClass('keithley')
139/58: keithley.trigger.blender[2]
139/59: keithley.trigger.blender[2].orenable
139/60: clear
139/61: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/62:

keithley = MagicClass('keithley')
139/63: keithley
139/64: clear
139/65: keithley.CAPACITY
139/66: clear
139/67: keithley.CAPACITY = 1
139/68: keithley.CAPACITY
139/69: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/70: clear
139/71: keithley = MagicClass('keithley')
139/72: keithley.CAPACITY
139/73: clear
139/74: keithley.smua.CAPACITY
139/75: keithley.smua.CAPACITY
139/76: keithley.smua.CAPACITY = 1
139/77: clear
139/78: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/79: keithley = MagicClass('keithley')
139/80: keithley.smua.CAPACITY
139/81: keithley.smua.CAPACITY = 1
139/82: clear
139/83: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/84: clear
139/85: keithley
139/86: keithley.QueryPulseConfig()
139/87: clear
139/88: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/kethley_doc.py')
139/89: clear
139/90: myset = set(SUBCLASSES)
139/91: myset
139/92: clear
139/93: len(myset)
139/94: myset
139/95: clear
139/96: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/kethley_doc.py')
139/97: all_new = [x.strip('.') for x in ALL]
139/98: all_new
139/99: clear
139/100: all_new
139/101: clear
139/102: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/kethley_doc.py')
139/103: all_smu = [x for x in ALL if x.find('smua')]
139/104: x.find('smua')
139/105: 'lan.status.dns.address[N]'.find('smua')
139/106: 'smua.status.dns.address[N]'.find('smua')
139/107: all_smu
139/108: clear
139/109: all_smu = [x for x in ALL if x.find('smua')>=0]
139/110: all_smu
139/111: all_smu = [x.replace('smua', 'smub') for x in all_smu]
139/112: all_smu
139/113: clear
139/114: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/kethley_doc.py')
139/115: AttributeError
139/116: raise AttributeError
139/117: clear
139/118: visa
139/119: visa.bla
139/120: clear
139/121: keithley.QueryPulseConfig
139/122: keithley.smua
139/123: clear
139/124: getattr(keithley,ALL[0])
139/125:
for a in ALL:
    getattr(keithley, a)
139/126: clear
139/127: keithley.bit.bitand
139/128: keithley.trigger.blender[N].orenable
139/129: clear
139/130: keithley.trigger.blender1N].orenable
139/131: keithley.trigger.blender[1].orenable
139/132: clear
139/133: keithley.trigger.blender[1]
139/134: clear
139/135: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/136: clear
139/137: keithley = MagicClass('keithley')
139/138: clear
139/139: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/140: keithley = MagicClass('keithley')
139/141: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/142: keithley = MagicClass('keithley')
139/143: clear
139/144: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/145: keithley = MagicClass('keithley')
139/146: clear
139/147: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/148: keithley = MagicClass('keithley')
139/149: clear
139/150: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/151:
keithley = MagicClass('keithley')
# populate initial attributes from list ALL
for a in ALL:
    getattr(self, a)
139/152: clear
139/153:
for a in ALL:
    getattr(keithley, a)
139/154: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/155: clear
139/156: keithley = MagicClass('keithley')
139/157:
for a in ALL:
    getattr(keithley, a)
139/158: keithley.bit.clear
139/159: keithley.bit.clear
139/160: clear
139/161: keithley.bit.clear
139/162: keithley.digio.trigger.assert
139/163: clear
139/164: keithley.display.getlastkey
139/165: keithley.beeper.beep
139/166: keithley.beeper.enable
139/167: keithley.beeper.enable = 1
139/168: clear
139/169: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/170: keithley = MagicClass('keithley')
139/171: clear
139/172:
for a in ALL:
    setattr(keithley, a)
139/173: clear
139/174: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/175:
for a in ALL:
    setattr(keithley, a)
139/176: clear
139/177: keithley = MagicClass('keithley')
139/178: clear
139/179: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/180: keithley = MagicClass('keithley')
139/181: clear
139/182: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/183: keithley = MagicClass('keithley')
139/184: keithley.dataqueue.CAPACITY
139/185: clear
139/186: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/187: keithley = MagicClass('keithley')
139/188:
for a in ALL:
    setattr(keithley, a)
139/189: clear
139/190:
for a in ALL:
    getattr(keithley, a)
139/191: import operator
139/192: operator.attrgetter("b.c")(keithley)
139/193:
for a in ALL:
    operator.attrgetter(a)(keithley)
139/194: clear
139/195: keithley = MagicClass('keithley')
139/196:
for a in ALL:
    operator.attrgetter(a)(keithley)
139/197: clear
139/198: keithley
139/199: keithley.delay()
139/200: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/201: keithley = MagicClass('keithley')
139/202: clear
139/203:
for a in ALL:
    operator.attrgetter(a)(keithley)
139/204: keithley.execute
139/205: clear
139/206: keithley.add
139/207: clear
139/208: or a in ALL:
139/209:
for a in ALL:
    print(a)
139/210: clear
139/211: clear
139/212: ALL = sorted(ALL)
139/213: ALL
139/214: clear
139/215: all = ALL
139/216: clear
139/217: ALL
139/218: clear
139/219: ALL[0:100]
139/220: clear
139/221: ALL[100:-1]
139/222: clear
139/223: ALL[99:-1]
139/224: clear
139/225: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/kethley_doc.py')
139/226: clea
139/227: clear
139/228: keithley
139/229:
for a in ALL:
    operator.attrgetter(a)(keithley)
139/230:
for a in ALL:
    try:
        operator.attrgetter(a)(keithley)
    except:
        print(a)
139/231: clear
139/232: keithley = MagicClass('keithley')
139/233: operator.attrgetter('beeper.enable')(keithley)
139/234: clear
139/235:
for a in ALL:
    try:
        operator.attrgetter(a)(keithley)
    except:
        print('ERROR setting: %s' % a)
139/236: clear
139/237: keithley.smua.source.delay
139/238: keithley.smua.source
139/239: is 'source' in PROPERTIES
139/240: 'source' in PROPERTIES
139/241: clear
139/242: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/243: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/244: clear
139/245: keithley = MagicClass('keithley')
139/246:
for a in ALL:
    try:
        operator.attrgetter(a)(keithley)
    except:
        print('ERROR setting: %s' % a)
139/247: keithley.node.execute
139/248: keithley.node
139/249: clear
139/250:
WARNING = """
Warning: PROPERTIES, CONSATNTS, FUNCTIONS and SUBCLASSES must be mutually\n
exclusive. A string used for a PROPERTY cannot be used to create a class\n
later, when the property already exists (and vice versa).
"""
139/251: WARNING
139/252: print(WARNING)
139/253: clear
139/254:
WARNING = """
Warning: PROPERTIES, CONSATNTS, FUNCTIONS and SUBCLASSES must be mutually\n\n
exclusive. A string used for a PROPERTY cannot be used to create a class\n\n
later, when the property already exists (and vice versa).
"""
139/255: print(WARNING)
139/256: clear
139/257: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_doc.py')
139/258: bool(properties & functions)
139/259: bool(properties & CLASSES)
139/260: clear
139/261: bool(properties & classes)
139/262: bool(functions & classes)
139/263: clear
139/264: RuntimeError(WARNING)
139/265: clear
139/266: raise RuntimeError(WARNING)
139/267:
WARNING = ('Warning: PROPERTIES, CONSATNTS, FUNCTIONS and SUBCLASSES must be ' +
           'mutually\nexclusive. A string used for a PROPERTY cannot ' +
           'be used to create a class\nlater, when the property already ' +
           'exists (and vice versa).')
139/268: print(WARNING)
139/269: clear
139/270: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_doc.py')
139/271: raise RuntimeError(WARNING)
139/272:
WARNING = ('Warning: PROPERTIES, CONSATNTS, FUNCTIONS must not contain ' +
           'elements \n from and CLASSES. E.g., once a property is created, ' +
           ' it cannot be used as \na class anymore')
139/273: print(WARNING)
139/274:
WARNING = ('Warning: PROPERTIES, CONSATNTS, FUNCTIONS must not contain\n' +
           'elements from and CLASSES. E.g., once a property is created, ' +
           ' it cannot be used as \na class anymore')
139/275: clear
139/276: raise RuntimeError(WARNING)
139/277:
WARNING = ('Warning: PROPERTIES, CONSATNTS, FUNCTIONS must not contain\n' +
           'elements from and CLASSES. E.g., once a property is created, ' +
           ' it cannot be \nused as a class anymore')
139/278: raise RuntimeError(WARNING)
139/279: clear
139/280: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_doc.py')
139/281: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/282:
for a in ALL:
    try:
        operator.attrgetter(a)(keithley)
    except:
        print('ERROR setting: %s' % a)
139/283: clear
139/284: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/285: keithley = MagicClass('keithley')
139/286: clear
139/287: keithley = MagicClass('keithley')
139/288: clear
139/289: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/290: keithley = MagicClass('keithley')
139/291: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/292: keithley = MagicClass('keithley')
139/293: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/294: clear
139/295: keithley = MagicClass('keithley')
139/296: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/297: clear
139/298: keithley = MagicClass('keithley')
139/299: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/300: clear
139/301: keithley = MagicClass('keithley')
139/302: clear
139/303: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/304: keithley = MagicClass('keithley')
139/305: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/306: keithley = MagicClass('keithley')
139/307: clear
139/308: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/309: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/310: keithley = MagicClass('keithley')
139/311: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/312: clear
139/313: keithley = MagicClass('keithley')
139/314: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/315: keithley = MagicClass('keithley')
139/316: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/317: clear
139/318: keithley = MagicClass('keithley')
139/319: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/320: keithley = MagicClass('keithley')
139/321: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/322: clear
139/323: keithley = MagicClass('keithley')
139/324: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/325: keithley = MagicClass('keithley')
139/326: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/327: keithley = MagicClass('keithley')
139/328: clear
139/329: keithley = MagicClass('keithley')
139/330: clear
139/331: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/332: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/333: keithley = MagicClass('keithley')
139/334: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
139/335: keithley = MagicClass('keithley')
139/336: clear
139/337:
# populate attributes
for a in ALL:
    operator.attrgetter(a)(MagicClass)
139/338: clear
139/339:
 # populate attributes
for a in ALL:
    operator.attrgetter(a)(keithley)
139/340: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
140/1: clear
140/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/Keithley/keithley_driver.py')
140/3: keithley = MagicClass('keithley')
140/4:
for a in ALL:
    operator.attrgetter(a)(keithley)
140/5: clea
140/6: clear
140/7: keithley = MagicClass('keithley')
140/8:
for a in ALL:
    setattr(keithley, a)
140/9:
for a in ALL:
    getattr(keithley, a)
140/10: clear
140/11: keithley.__doc__
140/12: help(keithley)
140/13: clear
140/14:
WARNING = """Warning: PROPERTIES, CONSATNTS, FUNCTIONS must not contain
             elements from and CLASSES. E.g., once a property is created,
             it cannot be used as a class anymore"""
140/15: WARNING
140/16: print(WARNING)
140/17:
WARNING = """Warning: PROPERTIES, CONSATNTS, FUNCTIONS must not contain
elements from and CLASSES. E.g., once a property is created,
it cannot be used as a class anymore"""
140/18: print(WARNING)
140/19: clear
140/20:

    BANNER = """'Welcome to CustomXepr %s.

You can access connected instruments as "customXepr", "mercuryFeed" and
"keithley".

Use "%run path_to_file.py" to run a python script such as a measurement cycle.
Execute "goDark()" or "goBright()" to switch the user interface style. Type
"exit" to gracefully exit CustomXepr.

(c) 2016 - 2018, %s.""" % ('1.2.3', 'Sam Schott')
140/21: clear
140/22:
BANNER = """'Welcome to CustomXepr %s.

You can access connected instruments as "customXepr", "mercuryFeed" and
"keithley".

Use "%run path_to_file.py" to run a python script such as a measurement cycle.
Execute "goDark()" or "goBright()" to switch the user interface style. Type
"exit" to gracefully exit CustomXepr.

(c) 2016 - 2018, %s.""" % ('1.2.3', 'Sam Schott')
140/23: clear
140/24:
BANNER = ('Welcome to CustomXepr %s. ' % __version__ +
          'You can access connected instruments as ' +
          '"customXepr", "mercuryFeed" and "keithley".\n\n' +
          'Use "%run path_to_file.py" to run a python script such as a ' +
          'measurement routine.\n'
          'Execute "goDark()" or "goBright()" to switch the user ' +
          'interface style. Type "exit" to gracefully exit ' +
          'CustomXepr.\n\n(c) 2016 - 2018, %s.' % __author__)
140/25: clear
140/26: SMU_LIST = ['smua', 'smub']
140/27: assert 'smua' in SMU_LIST
140/28: assert 'bla' in SMU_LIST
140/29: clear
140/30: smu
140/31: smu = 'smua'
140/32: clear
140/33: smu is 'sma'
140/34: smu is 'smua'
140/35: clear
140/36: "'smu' must be in %s" % SMU_LIST
140/37: clear
140/38: keithley
140/39: keithley.smua
140/40: keithley.smua
140/41: keithley.smua
140/42: keithley.smub
140/43: clear
140/44: keithley.smuc
140/45: keithley.smua
140/46: keithley.smua
140/47: clear
140/48: keithley.smua._name
140/49: keithley.smua
140/50: keithley.smua(2)
140/51: clear
140/52: keithley.smua()
140/53: clear
141/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/3: clear
141/4: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/5: clear
141/6: keithley = MagicClass('keithley')
141/7: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/8: clear
141/9: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/10: keithley = MagicClass('keithley')
141/11: keithley.smua
141/12: keithley.smua._name
141/13: str(keithley.smua)
141/14: clear
141/15: keithley.display
141/16: clear
141/17: keithley.smua
141/18: smu = keithley.smua
141/19: smu
141/20: smu._name
141/21: assert smu._name.split('.')[-1] in self.SMU_LIST
141/22: assert smu._name.split('.')[-1] in SMU_LIST
141/23: SMU_LIST = ['smua', 'smub']
141/24: assert smu._name.split('.')[-1] in SMU_LIST
141/25: smu._name.split('.')[-1]
141/26: clear
141/27: keithley.smua_name
141/28: clear
141/29: keithley.smua._name
141/30: keithley.smua._name.split('.').[-1]
141/31: keithley.smua._name.split('.')[-1]
141/32: clear
141/33: str(True)
141/34: %autorelaod 0
141/35: %autoreload 0
141/36: clear
141/37: str(True)
141/38: 'True'.lowercase()
141/39: dir('True')
141/40: clear
141/41: 'True'.lower()
141/42: value = 'test'
141/43:
if isinstance(value, str):
    value = '"' + value + '"'
141/44: value
141/45: clear
141/46: keithley
141/47: keithley.reset()
141/48: keithley.reset
141/49: clear
141/50:
msg = ('Recording transfer curve with Vg from %sV to %sV, Vd = %s V. '
       % (3, 4, [1,2,3]))
141/51: msg
141/52: clear
141/53: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/54: clear
141/55: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/56: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/57: keithley = Keithley2600()
141/58: clear
141/59: keithley = Keithley2600('172.293.2.33')
141/60: clear
141/61: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/62: keithley = Keithley2600('172.293.2.33')
141/63: clear
141/64: keithley = Keithley2600Base('172.293.2.33')
141/65: clear
141/66: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/67: keithley = Keithley2600Base('172.293.2.33')
141/68: clear
141/69: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/70: keithley = Keithley2600Base('172.293.2.33')
141/71: clear
141/72: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/73: keithley = Keithley2600Base('172.293.2.33')
141/74: clear
141/75: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/76: keithley = Keithley2600Base('172.293.2.33')
141/77: clear
141/78: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/79: keithley = Keithley2600Base('172.293.2.33')
141/80: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/81: clear
141/82: keithley = Keithley2600Base('172.293.2.33')
141/83: keithley.address
141/84: keithley._name
141/85: keithley.address
141/86: clear
141/87: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/88: clear
141/89: keithley = Keithley2600Base('172.293.2.33')
141/90: clear
141/91: Keithley2600Base.__dict__
141/92: clear
141/93: Keithley2600Base
141/94: clear
141/95: keithley = Keithley2600Base('172.293.2.33')
141/96: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/97: keithley = Keithley2600Base('172.293.2.33')
141/98: clear
141/99: keithley
141/100: keithley.address
141/101: clear
141/102: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/103: keithley = Keithley2600Base('172.293.2.33')
141/104: clear
141/105: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/106: keithley = Keithley2600Base('172.293.2.33')
141/107: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/108: clear
141/109: keithley = Keithley2600Base('172.293.2.33')
141/110: keithley.address
141/111: clear
141/112: keithley.beeper.beep()
141/113: keithley.beeper.enable
141/114: keithley.beeper.enable =1
141/115: clear
141/116: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/117: keithley = Keithley2600Base('172.293.2.33')
141/118: keithley
141/119: keithley.beeper.beep()
141/120: clear
141/121: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/122: keithley = Keithley2600Base('172.293.2.33')
141/123: keithley.beeper.beep()
141/124: keithley.beeper.enable =1
141/125: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
141/126: clear
141/127: keithley = Keithley2600Base('172.293.2.33')
141/128: keithley.beeper.beep()
141/129: keithley.beeper.enable =1
141/130: keithley.beeper.enable
141/131: clear
142/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
142/2: clear
142/3: keithley = Keithley2600Base('172.293.2.33')
142/4: keithley.beeper.beep()
142/5: clear
142/6: keithley.beeper.enable =1
142/7: keithley.beeper.enable = True
142/8: clear
142/9: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
142/10: keithley = Keithley2600Base('172.293.2.33')
142/11: keithley.beeper.enable =1
142/12: keithley.beeper.beep()
142/13: keithley.beeper.enable = True
142/14: clear
142/15: keithley.beeper.enable = false
142/16: clear
142/17: keithley.beeper.enable = False
142/18: keithley.beeper.enable = 'test'
142/19: clear
142/20: keithley = Keithley2600('172.293.2.33')
142/21: clear
142/22: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
142/23: keithley = Keithley2600('172.293.2.33')
142/24: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
142/25: keithley = Keithley2600('172.293.2.33')
142/26: clear
142/27: keithley.beeper.beep()
142/28: keithley.beeper.enable
142/29: keithley.beeper.enable()
142/30: clear
142/31: keithley.beeper.enable
142/32: keithley.beeper.enable = 2
142/33: keithley.beeper.beep(0.3, 2400)
142/34: clear
142/35: keithley.applyVoltage(keithley.smua, 10)
142/36: keithley.applyVoltage(keithley.smub, 10)
142/37: smu = keithley.smua
142/38: keithley._check_smu(smu)
142/39: smu.source.output = keithley.OUTPUT_ON
142/40: clear
142/41: smu.source.levelv = 10
142/42: smu.source.levelv
142/43: smu.source
142/44: keithley = Keithley2600('172.293.2.33')
142/45: keithley.smua
142/46: keithley.smua.source
142/47: keithley.smua.source.levelv
143/1: clear
143/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
143/3: keithley = Keithley2600('172.293.2.33')
143/4: keithley.smua.source
143/5: keithley.smua.source.levelv
143/6: clear
143/7: xit
144/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
144/2: clear
144/3: keithley = Keithley2600('172.293.2.33')
144/4: keithley.smua.source.levelv
144/5: clear
144/6: keithley.applyVoltage(keithley.smua,10)
144/7: keithley.applyCurrent(keithley.smua,10)
144/8: keithley.setIntegrationTime(keithley.smua,0.1)
144/9: keithley.localnode.linefreq
144/10: clear
144/11: smu = keithley.smua
144/12: clear
144/13: keithley._check_smu(smu)
144/14: smu.source.output = keithley.OUTPUT_ON
144/15: Vcurr = smu.source.levelv
144/16: keithley.display.smua.measure.func = keithley.MEASURE_DCVOLTS
144/17: smu.source.levelv = 2
144/18: clear
144/19: from Config.main import CONF
144/20: CONF.get('Keithley','VgStart')
144/21: clear
144/22: str(CONF.get('Keithley', 'VdList')).strip('[]')
144/23: clear
144/24: CONF.get('Keithley', 'pulsed')
144/25: clear
144/26: CONF.get('Keithley', 'pulsed')
144/27: CONF.get('Keithley', 'gate')
144/28: clear
144/29: keithley.SMUS
144/30: keithley.SMU_LIST
144/31: clear
144/32: len(keithley.SMU_LIST)
144/33:
comboBoxSmuList = keithley.SMU_LIST
if len(comboBoxSmuList) < 3:
    comboBoxSmuList.append('--')
144/34: comboBoxSmuList
144/35: clear
144/36:
comboBoxSmuList = keithley.SMU_LIST
while len(comboBoxSmuList) < 3:
    comboBoxSmuList.append('--')
144/37: comboBoxSmuList
144/38: clear
144/39: 'smua' in comboBoxSmuList
144/40: cmbList = comboBoxSmuList
144/41: clear
144/42: cmbList.index(CONF.get('Keithley', 'gate'))
144/43: cmbList.index(CONF.get('Keithley', 'drain'))
144/44: cmbList.index(3)
144/45: clear
144/46: smugate = 'smua'
144/47: getattr(keithley, smugate)
144/48: smua = getattr(keithley, smugate)
144/49: smua.__name
144/50: smua._name
144/51: clear
144/52:
msg = ('Keithley cannot be reached at %s. ' % keithley.address
       + 'Please check if address is correct and Keithley is ' +
       'tunrned on')
144/53: msg
144/54: QtWidgets.QMessageBox.information(None, str('error'), msg)
144/55: from qtpy import QtWidgets
144/56: QtWidgets.QMessageBox.information(None, str('error'), msg)
144/57: clear
144/58: keithley.SMU_LIST
144/59: keithley.SMU_LIST
144/60: clear
144/61: keithley.SMU_LIST = ['smua', 'smub']
144/62: clear
144/63: cmbList = keithley.SMU_LIST
144/64: cmbList
144/65:
while len(cmbList) < 3:
    cmbList.append('--')
144/66: cmbList
144/67: keithley.SMU_LIST
144/68: type(keithley.SMU_LIST)
144/69: clear
144/70: x = 3
144/71: a = x
144/72: a
144/73: clear
144/74: a = 4
144/75: x
144/76: keithley.SMU_LIST
144/77: keithley.SMU_LIST = ['smua', 'smub']
144/78: clear
144/79: keithley.SMU_LIST
144/80: keithley.SMU_LIST
144/81: clear
145/1: clear
145/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
145/3: keithley = Keithley2600('noIP')
145/4: keithley.SMU_LIST
145/5: cmbList = keithley.SMU_LIST
145/6: clear
145/7:
cmbList
while len(cmbList) < 3:
    cmbList.append('--')
145/8: cmbList
145/9: keithley.SMU_LIST
145/10: cmbList = ['smua', 'smub']
145/11: keithley.SMU_LIST
145/12: cmbList
145/13: keithley.SMU_LIST = list(cmbList)
145/14: keithley.SMU_LIST
145/15: clear
145/16: clear
146/1: clear
147/1: clear
147/2: from KeithleyDriver.keithley_doc import CONSTANTS, FUNCTIONS, PROPERTIES, ALL
147/3: len(ALL)
147/4: clear
147/5: 'tspnet.excecute()' in ALL
147/6: 'tspnet.excecute' in ALL
147/7: ALL
147/8: clear
147/9: 'tspnet.excecute' in ALL
147/10: 'tspnet.idn' in ALL
147/11: 'SweepILinMeasureV' in ALL
147/12: clear
148/1: clear
148/2: import matplotlib as mpl
148/3: mpl.style
148/4: clear
149/1: clear
149/2: clear
149/3: from Congig.main import CONF
149/4: from Config.main import CONF
149/5: clear
149/6: CONF.set('Keithley', 'gate')
149/7: CONF.get('Keithley', 'gate')
149/8: clear
149/9: clear
155/1: keithleyGUI.cmbList
155/2: keithleyGUI.comboBoxGateSMU.setItemData(['smua','smub'])
155/3: keithleyGUI.comboBoxGateSMU.clear()
149/10: clear
149/11: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/startup.py')
156/1: clear
173/1: clear
173/2: new_name = '.bla.di.bla.di.ba'
173/3: new_name.strip('.')
173/4: new_name
173/5: clear
173/6: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
173/7: keithley = MagicClass('')
173/8: keithley.beeper
173/9: keithley.beeper._name
173/10: keithley.beeper.beep()
173/11: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
173/12: clear
173/13: keithley = MagicClass('')
173/14: keithley.beeper.beep()
173/15: clear
173/16: keithley.beeper.enable
173/17: keithley.beeper.enable = 1
173/18: keithley.beeper.enable = 0
175/1: clear
175/2: keithley
175/3: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
175/4: clear
175/5: keithley = MagicClass('')
175/6: keithley.trigger.blender[1].stimulus[1]
175/7: keithley.trigger.blender[1].stimulus[1] = 46
175/8: clear
175/9: keithley.trigger.blender[1]._name
175/10: clear
175/11: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
175/12: keithley = MagicClass('')
175/13: keithley.trigger.blender[1]._name
175/14: keithley.trigger.blender[1]
175/15: keithley.trigger.blender[2]
175/16: keithley.trigger.blender[1]
175/17: clear
175/18: keithley.trigger.blender[1].stimulus[1]
175/19: keithley.trigger.blender[1]
175/20: keithley.trigger.blender[1]._name
175/21: clear
175/22: keithley.trigger.blender[1].stimulus
175/23: new_name = '%s.%s' % (keithley.trigger.blender[1]._name, 'stimulus')
175/24: new_name
175/25: name = 'stimulus'
175/26: name in FUNCTIONS
175/27: name in PROPERTIES or name in CONSTANTS
175/28: new_name in PROPERTY_LISTS
175/29: clear
175/30: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
175/31: keithley = MagicClass('')
175/32: keithley.trigger.blender[1].stimulus[1]
175/33: keithley.trigger.blender[1].stimulus[2]
175/34: keithley.trigger.blender[1].stimulus[1] = 1
175/35: keithley.trigger.blender[1].stimulus[1] = 2
175/36: clear
175/37: keithley
175/38: keithley._name
175/39: keithley.trigger._name
175/40: keithley.smua.trigger
175/41: keithley.smua.trigger._name
175/42: keithley.smua._name
175/43: clear
175/44: keithley.smua.trigger._parent
175/45: keithley.smua.trigger._parent._name
175/46: clear
175/47: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
176/1: clear
176/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
176/3: keithley = MagicClass('')
176/4: keithley.smua.trigger
176/5: keithley.smua.trigger._name
176/6: keithley.trigger
176/7: keithley.smua.trigger._name
176/8: keithley.smua.trigger
176/9: keithley.smua.trigger._name
176/10: clear
176/11: trigger.
176/12: clear
176/13: handler = MagicClass(new_name, parent=self)
176/14: clear
176/15: keithley.
176/16: clear
176/17: keithley.trigger.smua.trigger.smua.smua.smua.smua
176/18: keithley.trigger.smua.trigger.smua.smua.smua.smua._name
176/19: clear
176/20: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
176/21: keithley = MagicClass('')
176/22: keithley.address
176/23: keithley.address._name
176/24: keithley._name
176/25: clear
176/26: keithley.smua
176/27: keithley.smua._name
176/28: keithley.smua.trigger
176/29: keithley.smua.trigger._name
176/30: keithley.trigger
176/31: keithley.trigger._name
176/32: clear
176/33: keithley.trigger.blender[1].stimulus[1]
176/34: keithley.trigger.blender[1].stimulus[1] = 1
176/35: keithley.smua.trigger
176/36: keithley.smua.trigger._name
176/37: keithley.trigger.blender[1].stimulus[1]
176/38: clear
176/39: keithley.blender._name
176/40: clear
176/41: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
177/1: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
177/2: clear
177/3: keithley = MagicClass('')
177/4: keithley.smua
177/5: keithley.smua
177/6: keithley.smua
177/7: keithley.smua._name
177/8: keithley.trigger.blender[1].stimulus[1] = 1
177/9: keithley.trigger.blender[1].stimulus[1]
177/10: clear
177/11: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
177/12: keithley = MagicClass('')
177/13: keithley.trigger.blender[1].stimulus[1]
177/14: keithley.trigger.blender[1].stimulus
177/15: keithley.trigger.blender[1].stimulus
177/16: clear
177/17: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
177/18: keithley = MagicClass('')
177/19: clear
177/20: keithley.trigger.blender[1].stimulus[1]
177/21: keithley.trigger.blender[1].stimulus
177/22: keithley.trigger.blender[1].stimulus
177/23: keithley.smua
177/24: keithley.smua
177/25: keithley.smua
177/26: keithley.smua
177/27: clear
178/1: clear
178/2: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
178/3: keithley = MagicClass('')
178/4: keithley.trigger.blender[1].stimulus[1]
178/5: keithley.trigger.blender[1].stimulus._name
178/6: clear
178/7: keithley.smua.trigger
178/8: keithley.smua.trigger
178/9: keithley.smua.trigger
178/10: keithley.smua.trigger._name
178/11: keithley.trigger
178/12: keithley.trigger._name
178/13: keithley.trigger
178/14: clear
178/15: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
178/16: runfile('/Users/samschott/Dropbox (Cambridge University)/CustomXepr/KeithleyDriver/keithley_driver_visa.py')
178/17: clear
178/18: keithley = MagicClass('')
178/19: keithley
178/20: keithley.trigger.blender[1].stimulus[1]
178/21: keithley.trigger.blender[1].stimulus._name
178/22: clear
178/23: keithley.smua.trigger
178/24: keithley.smua.trigger
178/25: keithley.smua.trigger
178/26: keithley.smua
178/27: keithley.trigger
178/28: keithley.trigger._name
178/29: clear
178/30: clear
181/1: clear
181/2:
from spyder.widgets.projects.config import (ProjectConfig, CODESTYLE,
                                            CODESTYLE_DEFAULTS,
                                            CODESTYLE_VERSION, WORKSPACE,
                                            WORKSPACE_DEFAULTS,
                                            WORKSPACE_VERSION,
                                            ENCODING, ENCODING_DEFAULTS,
                                            ENCODING_VERSION,
                                            VCS, VCS_DEFAULTS, VCS_VERSION)
181/3: clear
181/4:
CONF[WORKSPACE].get('main', 'recent_files',
                                                default=[])
181/5: clear
184/1: clear
191/1: clear
192/1: clear
197/1: clear
198/1: clear
198/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
198/3: clear
198/4: from . import CustomXepr
198/5: clear
198/6: from __future__ import absolute_import
198/7: from . import CustomXepr
198/8: from CustomXepr import CustomXepr
198/9: clear
198/10: from .XeprTools import CustomXepr
198/11: clear
198/12: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
200/1: runfile('/Users/samschott/Documents/Python/CustomXepr/XeprTools/AboutWindow.py')
200/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
200/3: clear
200/4: from XeprTools.CustomXepr import __version__, __author__, CustomXepr
200/5: clear
200/6: from XeprTools.CustomXepr import __version__, __author__, CustomXepr
200/7: clear
200/8: from .XeprTools.CustomXepr import __version__, __author__, CustomXepr
200/9: clear
200/10: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
200/11: runfile('/Users/samschott/Documents/Python/CustomXepr/KeithleyDriver/keithley_driver.py')
200/12: clear
200/13: keithley = Keithley2600('')
200/14: clear
200/15: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
201/1: clear
201/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
202/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
202/2: import pydoc
202/3: from CustomXepr import CustomXepr
202/4: clear
202/5: from CustomXepr import CustomXepr
202/6: CustomXepr.CustomXepr
202/7: pydoc.render_doc(CustomXepr)
202/8: clear
202/9: print(pydoc.render_doc(CustomXepr.CustomXepr))
202/10: print(pydoc.render_doc(CustomXepr))
202/11: clear
202/12: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
205/1: clear
205/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
208/1: clear
208/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
208/3: clear
209/1: clear
209/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
209/3: clear
210/1: clear
211/1: clear
212/1: clear
212/2: from XeprTools.CustomXepr import CustomXepr
212/3: CustomXepr.CustomXepr
212/4: clear
212/5: from XeprTools.CustomXepr import CustomXepr
212/6: clear
212/7: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
212/8: clear
212/9: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
212/10: go_bright()
212/11: DARK
212/12: DARK = CONF.get('main', 'DARK')
212/13: DARK
213/1: clear
213/2:
import sys
import os
from threading import Event
from qtpy import QtCore
from Queue import Queue
from decorator import decorator
import time
import numpy as np
import logging

# custom imports
from utils.tls_smtp_handler import TlsSMTPHandler
from xeprtools.mode_picture_class import ModePicture
from config.main import CONF
213/3: clear
213/4:
import sys
import os
from threading import Event
from qtpy import QtCore
from Queue import Queue
from decorator import decorator
import time
import numpy as np
import logging

# custom imports
from utils.tls_smtp_handler import TlsSMTPHandler
from xeprtools.mode_picture_class import ModePicture
from config.main import CONF
213/5: clear
213/6: import ipython
213/7: import IPython
213/8: cleaer
213/9: clear
213/10: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/11: clear
213/12: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/13: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/14: clear
213/15: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/16: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/17: clear
213/18: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/19: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/20: ckear
213/21: clear
213/22: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/23: clear
213/24: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/25: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
213/26: clear
213/27: clear
214/1: clear
214/2: clear
214/3: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
215/1: clear
215/2: runfile('/Users/samschott/Documents/Python/Keithley2600-driver/keithley_doc.py')
215/3: clear
217/1: clear
217/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
217/3: clear
217/4: self.gf1_edit.setEnabled(False)
217/5: clear
217/6: mercuryGUI.gf1_edit.setEnabled(False)
217/7: mercuryGUI.gf1_edit.updateText('test')
217/8: clear
217/9: self.gf1_edit.setEnabled(True)
217/10: mercuryGUI.gf1_edit.setEnabled(True)
217/11: clear
218/1: clear
218/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
218/3: self.gf2_checkbox.clicked.connect(self.change_flow_auto)
218/4: clear
218/5: mercuryGUI.gf2_checkbox.clicked.connect(self.change_flow_auto)
218/6: mercuryGUI.gf2_checkbox.clicked.connect(mercuryGUI.change_flow_auto)
218/7:
mercuryGUI.gf1_edit.setReadOnly(True)
mercuryGUI.gf1_edit.setEnabled(False)
218/8: clear
220/1: clear
220/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
220/3: customXeprGUI.setIntialPosition()
220/4: self = customXeprGUI
220/5:
xPos = screen.left()
yPos = screen.top()
width = screen.width()*2/3
height = screen.height()*2/3

self.setGeometry(xPos, yPos, width, height)
220/6: screen = QtWidgets.QDesktopWidget().screenGeometry(self)
220/7:
xPos = screen.left()
yPos = screen.top()
width = screen.width()*2/3
height = screen.height()*2/3

self.setGeometry(xPos, yPos, width, height)

self.splitter.setSizes([width*0.75, width*0.25])
220/8: ckear
220/9: clear
220/10:
self.setStyleSheet('background: transparent')
self.setAttribute(Qt.WA_TranslucentBackground, True)
self.setAutoFillBackground(True)
220/11: from qtpy import QT
220/12: from qtpy import Qt
220/13: clear
220/14:
self.setStyleSheet('background: transparent')
self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
self.setAutoFillBackground(True)
220/15: self.setAutoFillBackground(False)
220/16: self.setStyleSheet('')
220/17: self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
221/1: clear
221/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
221/3: self = customXeprGUI
221/4: clear
221/5: self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
221/6: self.setStyleSheet("background: rgba(0,0,0,80%);")
221/7: self.setStyleSheet("background: rgba(1,1,1,80%);")
223/1: clear
223/2:
('self.mercury.modules[%s].%s'
                           % (3, address))
223/3: clear
223/4:
('self.mercury.modules[%s].%s'
                           % (3, 'address'))
223/5: clear
223/6: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
223/7: clear
225/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
226/1: clear
226/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
226/3: mercuryGUI.mercuryMenu.addAction(self.exitAction)
226/4: mercuryGUI.mercuryMenu.addAction(mercuryGUI.exitAction)
226/5: clear
226/6: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
228/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
229/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
229/2: keithleyGUI.show()
229/3: clear
231/1: clear
232/1: clear
232/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
233/1: %matplotlib
233/2: %matplotlib qt
233/3: %matplotlib qt5
233/4: clear
233/5: %gui qt5
233/6: %gui
233/7: %gui qt5
233/8:
import sys
import os
import logging
from qtpy import QtCore, QtWidgets, QtGui

# local imports
from config.main import CONF
from xeprtools.customxepr import CustomXepr, __version__, __author__
from xeprtools.customxper_ui import JobStatusApp
from mercury_gui.feed import MercuryFeed
from mercury_gui.main import MercuryMonitorApp
from keithley_driver import Keithley2600
from keithley_gui.main import KeithleyGuiApp

from utils import dark_style
from utils.misc import check_dependencies, patch_excepthook
from utils.internal_ipkernel import InternalIPKernel
233/9: clear
233/10: app = QtCore.QCoreApplication.instance()
233/11: app
233/12: app = QtWidgets.QApplication()
233/13: clear
233/14: app = QtWidgets.QApplication([''],)
233/15: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
234/1: clear
234/2:
import matplotlib
gui_env = ['TKAgg','GTKAgg','Qt4Agg','WXAgg']
for gui in gui_env:
    try:
        print "testing", gui
        matplotlib.use(gui,warn=False, force=True)
        from matplotlib import pyplot as plt
        break
    except:
        continue
print "Using:",matplotlib.get_backend()
234/3: clear
234/4:
import matplotlib
gui_env = [i for i in matplotlib.rcsetup.interactive_bk]
non_gui_backends = matplotlib.rcsetup.non_interactive_bk
print ("Non Gui backends are:", non_gui_backends)
print ("Gui backends I will test for", gui_env)
for gui in gui_env:
    print ("testing", gui)
    try:
        matplotlib.use(gui,warn=False, force=True)
        from matplotlib import pyplot as plt
        print ("    ",gui, "Is Available")
        plt.plot([1.5,2.0,2.5])
        fig = plt.gcf()
        fig.suptitle(gui)
        plt.show()
        print ("Using ..... ",matplotlib.get_backend())
    except:
        print ("    ",gui, "Not found")
234/5: clear
234/6: ?%gui
234/7: clear
234/8: import matplotlib
234/9: matplotlib.get_backend()
235/1:
import matplotlib
matplotlib.get_backend()
235/2: import matplotlib
235/3: matplotlib.get_backend()
235/4: matplotlib.backends
235/5: matplotlib.backends()
235/6: matplotlib.backends.backend
235/7: matplotlib.reload('qt5')
235/8: matplotlib.pyplot.get_backend()
235/9: matplotlib.pyplot.switch_backend('qt5')
235/10: matplotlib.pyplot.switch_backend('Qt5Agg')
235/11: clear
235/12: %gui qt
235/13: %gui qt
235/14: %gui qt
235/15: clear
235/16: %gui qt5
236/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
236/2: clear
236/3: created
237/1: from IPython import get_ipython
237/2:
ipython = get_ipython()
ipython.magic('%autoreload 0')
ipython.magic('%gui qt')
237/3:
import sys
import os
import logging
from qtpy import QtCore, QtWidgets, QtGui
237/4: clear
237/5:
created = False
app = QtCore.QCoreApplication.instance()
237/6: app
237/7:
if not app:
    if not args:
        args = ([''],)
    app = QtWidgets.QApplication(*args, **kwargs)
    created = True
237/8: return app, created
237/9: created
237/10: app
237/11: clear
237/12: xit
238/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
238/2: created
238/3: clear
239/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
241/1: clear
241/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
244/1: clear
244/2: %gui qt
244/3: %gui
244/4: %gui inline
244/5: clear
244/6: xit
244/7: clear
245/1: clear
245/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
245/3: created
245/4: CREATED
245/5: clear
246/1: clear
246/2: import time
246/3: time_str = time.strftime('%Y-%m-%d %H:%m')
246/4: time_str
246/5: time_str = time.strftime('%Y-%m-%d %H:%M')
246/6: time_str
246/7: clear
246/8: time_str = time.strftime('%Y-%m-%d %H:%M')
246/9: time_str
247/1: import numpy as np
247/2: from matplotlib.figure import Figure
247/3: import matplotlib.pyplot as plt
247/4: plt.plot(range(0,10),range(0,10),'-',linewidth=0.1)
247/5: clear
247/6:
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 500)
y1 = np.sin(x)
y2 = np.sin(3 * x)

fig, ax = plt.subplots(dpi=244)
ax.fill(x, y1, 'b', x, y2, 'r', alpha=0.3)
plt.show()
247/7: clear
249/1: clear
249/2:
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 500)
y1 = np.sin(x)
y2 = np.sin(3 * x)

fig, ax = plt.subplots(dpi=244)
ax.fill(x, y1, 'b', x, y2, 'r', alpha=0.3)
plt.show()
249/3:
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 500)
y1 = np.sin(x)
y2 = np.sin(3 * x)

fig, ax = plt.subplots()
ax.fill(x, y1, 'b', x, y2, 'r', alpha=0.3)
plt.show()
249/4:
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 500)
y1 = np.sin(x)
y2 = np.sin(3 * x)

fig, ax = plt.subplots()
ax.fill(x, y1, '-b', x, y2, '-r', alpha=0.3)
plt.show()
249/5: ax.fill_betweenx(x, y1, '-b', x, y2, '-r', alpha=0.3)
249/6: ax.fill_betweenx(y,x)
249/7: ax.fill_betweenx(y1,x)
249/8: plt.show()
249/9: clear
249/10:
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 500)
y1 = np.sin(x)
y2 = np.sin(3 * x)

fig, ax = plt.subplots()
ax.plot(x, y1, 'b', x, y2, 'r')
ax.fill_betweenx(y1,x)
plt.show()
249/11:
x = np.linspace(0, 2 * np.pi, 500)
y1 = np.sin(x)
y2 = np.sin(3 * x)

fig, ax = plt.subplots()
ax.plot(x, y1, 'b', x, y2, 'r')
ax.fill_betweenx(y1,x,alpha=0.3)
plt.show()
249/12:
x = np.linspace(0, 2 * np.pi, 500)
y1 = np.sin(x)
y2 = np.sin(3 * x)

fig, ax = plt.subplots()
ax.plot(x, y1, 'b', x, y2, 'r',linewidth = 0.2)
ax.fill_betweenx(y1,x,alpha=0.3)
plt.show()
249/13:
x = np.linspace(0, 2 * np.pi, 500)
y1 = np.sin(x)
y2 = np.sin(3 * x)

fig, ax = plt.subplots()
ax.plot(x, y1, 'b', x, y2, 'r',linewidth = 1)
ax.fill_betweenx(y1,x,alpha=0.3)
plt.show()
249/14:
x = np.linspace(0, 2 * np.pi, 500)
y1 = np.sin(x)
y2 = np.sin(3 * x)

fig, ax = plt.subplots()
ax.plot(x, y1, 'b', x, y2, 'r',linewidth = 0.8)
ax.fill_betweenx(y1,x,alpha=0.3)
plt.show()
250/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
250/2: clc
250/3: clear
251/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
252/1: clear
252/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
252/3: clear
252/4: keithleyGUI.statusBar..setStyleSheet("QStatusBar{padding-left:8px;background:rgba(255,0,0,255);color:black;font-weight:bold;}")
252/5: keithleyGUI.statusBar.setStyleSheet("QStatusBar{padding-left:8px;background:rgba(255,0,0,255);color:black;font-weight:bold;}")
252/6: keithleyGUI.statusBar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255);}")
252/7:
color = QtGui.QPalette().window().color().getRgb()
color = [x/255.0 for x in color]
252/8: color = QtGui.QPalette().window().color().getRgb()
252/9: color
252/10: keithleyGUI.statusBar.setStyleSheet("QStatusBar{background:rgba%s;}" % color)
252/11: "QStatusBar{background:rgba%s;}" % color
252/12: color
252/13: str(color)
252/14: 'QStatusBar{background:rgba%s;}' % color
252/15: '%s' % 3
252/16: '%s' % color
252/17: clear
252/18: 'QStatusBar{background:rgba%s;}' % str(color)
252/19: keithleyGUI.statusBar.setStyleSheet("QStatusBar{background:rgba%s;}" % str(color))
253/1: clear
253/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
253/3: clear
253/4: exitfrom config.main import CONF
253/5: from config.main import CONF
253/6: MERCURY_PORT = CONF.get('MercuryFeed', 'MERCURY_PORT')
253/7: MERCURY_PORT
253/8: clear
253/9: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
254/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
255/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
255/2: clear
255/3: import qdarkstyle
255/4: qdarkstyle.platform
255/5: qdarkstyle.QT_API_VALUES
255/6: qdarkstyle.QT_API_VALUES
255/7: qdarkstyle.PYQTGRAPH_QT_LIB_VALUES
255/8: qdarkstyle.load_stylesheet_pyqt5
255/9: clear
255/10: color = QtGui.QPalette().window().color().getRgb()
255/11: color
255/12: mercuryGUI.show()
256/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
256/2: clear
256/3: QtGui.QPalette()
256/4: p = QtGui.QPalette()
256/5: w =p.window()
256/6: w.style
256/7: w.style()
256/8: p = QtGui.QPalette()
256/9: clear
256/10: keithleyGUI..statusBar.setStyleSheet('QStatusBar{background:rgba%s;}' % str(color))
256/11: keithleyGUI.statusBar.setStyleSheet('QStatusBar{background:transparent;}')
256/12: mercuryGUI.statusBar.setStyleSheet('QStatusBar{background:transparent;}')
256/13: clear
256/14: mercuryGUI.fig
256/15: clear
256/16: mercuryGUI.fig.set_facecolor('transparent')
256/17: [49/255.0, 54/255.0, 59/255.0, 1]
256/18: mercuryGUI.fig.set_facecolor([49/255.0, 54/255.0, 59/255.0, 0])
256/19: mercuryGUI.fig.set_facecolor([1, 1, 1, 0])
256/20: mercuryGUI.fig.set_facecolor([1, 1, 1, 1])
256/21: mercuryGUI.fig.set_facecolor([1, 1, 0.5, 1])
256/22: mercuryGUI.fig.set_facecolor([0.5, 0.5, 0.5, 1])
256/23: mercuryGUI.canvas.draw()
256/24: mercuryGUI.fig.set_facecolor([0.5, 0.5, 0.5, 0])
256/25: mercuryGUI.canvas.draw()
256/26: clear
256/27: mercuryGUI.ax.set_facecolor([0.204, 0.225, 0.246, 1])
256/28: mercuryGUI.ax.set_facecolor([1.5*0.204, 1.5*0.225, 1.5*0.246, 1])
256/29: mercuryGUI.canvas.draw()
256/30: mercuryGUI.ax.set_facecolor([1.1*0.204, 1.1*0.225, 1.1*0.246, 1])
256/31: mercuryGUI.canvas.draw()
256/32: [1.1*0.204, 1.1*0.225, 1.1*0.246, 1]
256/33: clear
256/34: self.xData.append(range(0,100))
256/35: self = mercuryGUI
256/36: self.xData.append(range(0,100))
256/37: clear
256/38: self.yData.append(range(1:100))
256/39: self.yData.append(range(0,100))
256/40: clear
256/41: self._update_slider()
256/42: clear
256/43:
self.xData = self.xData[-86400:]
self.yData = self.yData[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
256/44:
# system imports
import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor
256/45: clear
256/46:
self.xData = self.xData[-86400:]
self.yData = self.yData[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
256/47: np
256/48: clear
256/49: self.xData.append(np.range(0,100))
256/50: self.xData.append(np.arange(0,100))
256/51: self.yData.append(np.arange(0,100))
256/52: clear
256/53:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yData = self.yData[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
256/54: clear
256/55: self.xData = [1,2,3,4,5]
256/56: self.yData = [1,2,3,4,5]
256/57:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yData = self.yData[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
256/58: clear
256/59: self.line1.set(linewidth=1)
256/60: clear
257/1: clear
257/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
257/3: clear
257/4: dark_style.apply_mpl_dark_theme()
257/5: apply_mpl_dark_theme()
257/6: clear
257/7: dark_style.apply_mpl_dark_theme()
257/8: dark_style.apply_mpl_bright_theme()
257/9: dark_style.apply_mpl_dark_theme()
257/10: dark_style.go_dark()
257/11: dark_style.go_bright()
257/12: clear
257/13: mpl.style.use(os.path.join(direct, 'mpl_dark_style.mplstyle'))
257/14: import matplotlib as mpl
257/15: mpl.style.library('mpl_dark_style.mplstyle')
257/16: clear
257/17:
self.xData = [0,1,2,3,4,5]
self.yData = [0,1,2,3,4,5]
257/18: self = mercuryGUI
257/19:
self.xData = [0,1,2,3,4,5]
self.yData = [0,1,2,3,4,5]
257/20: clear
257/21:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yData = self.yData[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
257/22: clear
257/23:
# system imports
import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor
257/24:
self.xData = self.xData[-86400:]
self.yData = self.yData[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
257/25: clear
258/1: clear
258/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
258/3: clea
258/4: clear
258/5: customXepr.wait(20)
258/6: customXepr.pause(20)
258/7: clear
258/8: customXeprGUI.show()
258/9: clear
258/10: import matplotlib as mpl
258/11: mpl.style.use(os.path.join(direct, 'mpl_bright_style.mplstyle'))
258/12: mpl.style.use(os.path.join(direct, 'mpl_bright_style.mplstyle'))
258/13: mpl.style.use('mpl_bright_style.mplstyle')
258/14: clear
258/15: mpl.style.use('mpl_bright_style.mplstyle')
258/16: clear
259/1: clear
259/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
259/3: go_dark()
259/4: go_bright()
259/5: labelColor = [0.8, 0.8, 0.8, 1]
259/6: clear
259/7: set_label_color(keithleyGUI.ax, labelColor)
259/8: runfile('/Users/samschott/Documents/Python/CustomXepr/utils/dark_style.py')
259/9: set_label_color(keithleyGUI.ax, labelColor)
259/10: keithleyGUI.canvas.draw()
259/11: labelColor = [0.2, 0.2, 0.2, 1]
259/12:
set_label_color(keithleyGUI.ax, labelColor)
keithleyGUI.canvas.draw()
259/13: clear
259/14: clear
259/15: xit
260/1: clear
260/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
260/3: clear
261/1: clear
261/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
261/3: clear
261/4: self = mercuryGUI
261/5: clear
261/6: self.fig.subplots(2,sharex=True)
261/7: del self.fig.subplots(2,sharex=True)
261/8: clear
261/9: (ax1, ax2) = self.fig.subplots(2,sharex=True)
261/10: ax1
261/11: ax2
261/12: self.ax1 = ax1
261/13: self.ax2 = ax2
261/14: clear
261/15: self.ax.set_xlabel('Time')
261/16: self.ax2.set_xlabel('Time')
261/17: clear
261/18: self.ax1.set_ylabel('Temperature [K]')
261/19: self.ax2.set_xlabel('Time')
261/20: self.ax2.set_ylabel('%')
261/21: clear
261/22: self.ax2.tick_params(axis='none')
261/23: #  self.ax1.tick_params(axis='y',  which='major')
261/24: self.ax1.tick_params(axis='y',  which='major')
261/25: clear
261/26: self.xLim, self.yLim = [-1, 1.0/60], [0, 300]
261/27: self.ax1.axis(self.xLim + self.yLim)
261/28: self.xLim + self.yLim
261/29: self.ax2.axis(self.xLim + [-0.02, 1])
261/30: clear
261/31: self.line1, = self.ax1.plot(0, 295, '-', linewidth=1)
261/32: self.canvas = FigureCanvas(self.fig)
261/33: clear
261/34:
import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor

# custom imports
from mercury_gui.feed import MercuryFeed
from mercury_gui.main_ui import Ui_MainWindow
from mercury_gui.address_dialog import AddressDialog

if QtCore.PYQT_VERSION_STR[0] == '5':
    from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg
                                                    as FigureCanvas)
elif QtCore.PYQT_VERSION_STR[0] == '4':
    from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg
                                                    as FigureCanvas)
261/35: clear
261/36: self.canvas = FigureCanvas(self.fig)
261/37: self.mplvl.addWidget(self.canvas)
261/38: self.canvas.draw()
261/39: self.mplvl.removeWidget(self.canvas)
261/40: self.mplvl.removeWidget(self.canvas)
261/41: self.mplvl.widget
261/42: clear
262/1: clear
262/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
262/3: clear
262/4: self = mercuryGUI
262/5: self.fig.subplots_adjust(hspace=0)
262/6: self.canvas.draw()
262/7: self.ax1.set_xticks([])
262/8: self.canvas.draw()
262/9: self.ax1.set_xticks('automatic)
262/10: self.ax1.set_xticks('automatic')
262/11: clear
262/12: self.ax1.set_xticks()
262/13: clear
262/14: self.ax1.set_autoscaley_on(True)
262/15: self.ax1.set_autoscaley_on(False)
262/16: self.ax2.set_yticks([])
262/17: self.canvas.draw()
262/18: self.ax2.set_yticks([0,1])
262/19: self.canvas.draw()
262/20: self.ax2.axis(self.xLim + [-0.05, 1.05])
262/21: self.canvas.draw()
262/22: self.fig.set_tight_layout('tight')
262/23: clear
262/24: self.canvas.draw()
262/25: self.canvas.draw()
262/26: self.fig.subplots_adjust(hspace=0)
262/27: self.canvas.draw()
262/28: self.fig.subplots_adjust(wspace=0,hspace=0)
262/29: self.canvas.draw()
262/30: clear
262/31: self.ax1.get_aspect()
262/32: self.ax1.set_aspect([1,2])
262/33: clear
262/34: self.ax1.set_aspect(2)
262/35: self.canvas.draw()
262/36: self.ax1.set_aspect(0.1)
262/37: self.canvas.draw()
262/38: self.ax1.set_aspect('auto')
262/39: self.canvas.draw()
262/40: grid = self.fig.GridSpec(hspace=0)
262/41: self.fig.autolayout
262/42: clear
262/43: self.fig.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
262/44: self.canvas.draw()
262/45: self.canvas.draw()
262/46: self.fig.set_tight_layout('auto')
262/47: self.canvas.draw()
262/48: self.fig.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
262/49: self.canvas.draw()
263/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
263/2: clear
263/3: self = mercuryGUI
263/4: clear
263/5: self.label.setText(_translate("MainWindow", "Show 60 min"))
263/6: clear
263/7: self.label.setText("Show 60 min")
263/8: self.label.setText("Show last 60 min")
263/9: clear
263/10: self.ax2.set_yticks([])
263/11: self.ax2.tick_params(axis='y', which='none')
263/12: self.ax2.set_yticks([0,1])
263/13: self.canvas.draw()
263/14: self.ax2.tick_params(axis='y', which='none')
263/15: self.canvas.draw()
263/16: self.ax2.set_yticks([])
263/17: self.canvas.draw()
263/18: clear
263/19: self.fig.set_tight_layout('tight')
263/20: self.canvas.draw()
263/21: clear
263/22: clear
263/23: xit
264/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
264/2: clear
264/3: self = mercuryGUI
264/4: clear
264/5: clear
265/1: clear
265/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
265/3: clear
266/1: clear
266/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
266/3: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
266/4: clear
266/5: self = mercuryGUI
266/6:
self.ax1.set_ylabel('Temperature [K]', fontsize=9)
self.ax2.set_xlabel('Time', fontsize=9)
self.ax2.set_ylabel('%', fontsize=9)
self.ax1.tick_params(axis='y', which='major', labelsize=9)
266/7: self.canvas.draw()
266/8: clea
266/9: clear
266/10: self.ax1.set_ylabel('Temperature [K]', fontsize=9)
266/11: self.ax2.set_xlabel('Time', fontsize=9)
266/12: self.ax1.tick_params(axis='y', which='major', labelsize=9)
266/13: self.ax2.set_yticks([])
266/14: self.canvas.draw()
266/15: clear
267/1: clear
267/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
267/3: clear
268/1: clear
268/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
268/3: clear
268/4: self.ax2.set_ylabel('Heater / gasflow', fontsize=9)
268/5: self = mercuryGUI
268/6: clear
268/7: self = monitor
268/8: clear
268/9: self.ax2.set_ylabel('Heater / gasflow', fontsize=9)
268/10: self.canvas.draw()
268/11: self.ax2.set_ylabel('', fontsize=9)
268/12: self.canvas.draw()
268/13: clear
268/14:
self.ax1.spines['bottom'].set_color([0.3, 0.3, 0.3, 1])
self.ax1.spines['top'].set_color([0.3, 0.3, 0.3, 1])
self.ax1.spines['left'].set_color([0.3, 0.3, 0.3, 1])
self.ax1.spines['right'].set_color([0.3, 0.3, 0.3, 1])
268/15: self.canvas.draw()
268/16: self.ax1.tick_params(axis='both', colors=[0.3, 0.3, 0.3, 1])
268/17: self.canvas.draw()
268/18: self.ax2.spines['top'].set_color([0.5, 0.5, 0.5, 1])
268/19: self.canvas.draw()
268/20: ax.tick_params(axis='both', colors='black')
268/21: self.ax1.tick_params(axis='both', colors='black')
268/22: clear
268/23: self.canvas.draw()
268/24: self.ax1.spines['bottom'].set_color([0.5, 0.5, 0.5, 1])
268/25: self.canvas.draw()
268/26: sb =self.ax1.spines['bottom']
268/27: sb.set_linewidth(1)
268/28: self.canvas.draw()
268/29: clear
268/30: self.xData = range(0, 10000)
268/31: self.yData = range(0, 10000)
268/32: clear
268/33:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yData = self.yData[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataMinZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
268/34: clear
268/35: self.lines = []
268/36: self.lines[0] = self.ax1.plot(0, 295, '-', linewidth=1)
268/37: self.lines.append(self.ax1.plot(0, 295, '-', linewidth=1))
268/38: clear
268/39: self.ax1.plot(0, 295, '-', linewidth=1)
268/40: re = self.ax1.plot(0, 295, '-', linewidth=1)
268/41: re
268/42: clear
268/43: self.yDataG = [0.5] * 10000
268/44: self.yDataH = [0.2] * 10000
268/45: clear
268/46:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
268/47: clear
269/1: clear
269/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
269/3: self = mercuryGUI
269/4: self.xData = range(0, 10000)
269/5:
self.yDataG = [295] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000
269/6: clear
269/7:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
269/8: min(self.CurrentYDataT)
269/9: self.CurrentYDataT
269/10: clear
269/11:
numberDP = sum(abs(x) < self.horizontalSlider.value()
               for x in self.xDataZero) + 5
269/12: numberDP
269/13: self.ax2.set_ylabel('', fontsize=9)
269/14: numberDP
269/15: clear
269/16: self.horizontalSlider.value()
269/17: self.horizontalSlider.value()
269/18:
numberDP = sum(abs(x) < self.horizontalSlider.value()
               for x in self.xDataZero) + 5
269/19: numberDP
269/20: clear
269/21: self.CurrentXData
269/22: clear
269/23:
# select data to be plotted
self.CurrentXData = self.xDataZero[-numberDP:]
self.CurrentYDataT = self.yDataT[-numberDP:]
self.CurrentYDataG = self.yDataG[-numberDP:]
self.CurrentYDataH = self.yDataH[-numberDP:]
269/24: min(self.CurrentYDataT))
269/25: min(self.CurrentYDataT)
269/26: clear
269/27: self.yDataT[-numberDP:]
269/28: numberDP
269/29: self.yDataT
269/30:
self.xData = range(0, 10000)
self.yDataT = [295] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000
269/31: self.yDataT
269/32: clear
269/33:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
269/34: self.yDataT = [297.3] * 10000
269/35: clear
269/36:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
269/37: clear
269/38: self.ax2.fill_between(self.xData, self.yDataH)
269/39: fill1 = self.ax2.fill_between(self.xData, self.yDataH)
269/40: self.canvas.draw()
269/41: fill1 = self.ax2.fill_betweenx(self.yDataH, self.xData)
269/42: self.canvas.draw()
269/43: fill1 = self.ax2.fill_between(self.xData, self.yDataH,0)
269/44: self.canvas.draw()
269/45: clear
269/46: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataH,0)
269/47: self.canvas.draw()
269/48: clear
269/49: fill2 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG,0)
269/50: self.canvas.draw()
269/51: clear
269/52: self.ax2.fill_between(self.CurrentXData, self.CurrentYDataH,0,alpha=0.5)
269/53: self.canvas.draw()
269/54: clear
270/1: clear
270/2:
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro', animated=True)

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()
270/3: clear
270/4:
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro', animated=True)

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()
270/5: clear
270/6: clear
271/1: clear
271/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
271/3: self=mercuryGUI
271/4: clear
271/5:
self.xData = range(0, 10000)
self.yDataT = [295] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000
271/6:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
271/7: self.yDataT = [297.5] * 10000
271/8: clear
271/9:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_slider()
271/10: clear
271/11: fill2 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataH, 0, alpha=0.5)
271/12: self.canvas.draw()
271/13: fill2.set_alpha(0.8)
271/14: self.canvas.draw()
271/15: fill2.set_alpha(0.2)
271/16: self.canvas.draw()
271/17: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, alpha=0.2)
271/18: self.canvas.draw()
271/19: fill11 = self.ax1.fill_between(self.CurrentXData, self.CurrentYDataT, 0, alpha=0.2)
271/20: self.canvas.draw()
271/21: clear
271/22: self.ax2.collections.clear()
271/23: self.ax2.collections.remove(fill2)
271/24: self.ax2.collections.remove(fill1)
271/25: self.canvas.draw()
271/26: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, alpha=0.2)
271/27: fill2 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataH, 0, alpha=0.2)
271/28: self.canvas.draw()
271/29: self.ax2.collections.remove(fill1)
271/30: self.ax2.collections.remove(fill2)
271/31: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, facecolor='blue', alpha=0.2)
271/32: self.canvas.draw()
271/33: self.ax2.collections.remove(fill1)
271/34: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, alpha=1)
271/35: self.canvas.draw()
271/36: clear
271/37: self.ax2.collections.remove(fill1)
271/38: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, facecolor=[85, 134, 1288], alpha=0.2)
271/39: clear
271/40: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, facecolor=[85, 134, 188]/.255, alpha=0.2)
271/41: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, facecolor=[85/.255, 134/.255, 188/.255], alpha=0.2)
271/42: clear
271/43: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, facecolor=[85/.255, 134/.255, 188/.255, 0.2])
271/44: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, facecolor=[85/255, 134/255, 188/255, 0.2])
271/45: self.canvas.draw()
271/46: clear
271/47: self.ax2.collections.pop()
271/48: self.ax2.collections.pop()
271/49: clear
271/50: self.canvas.draw()
271/51: fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, facecolor=[85/255.0, 134/255.0, 188/255.0, 0.2])
271/52: self.canvas.draw()
271/53: self.ax2.collections.pop()
271/54: self.canvas.draw()
271/55: clear
271/56:
self.color1 = [85/255.0, 134/255.0, 188/255.0, 0.2]
self.color2 = [229/255.0, 137/255.0, 36/255.0, 0.2]
271/57: self.fill1 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataG, 0, facecolor=self.color1)
271/58: self.fill2 = self.ax2.fill_between(self.CurrentXData, self.CurrentYDataH, 0, facecolor=self.color2)
271/59: self.canvas.draw()
271/60: clear
271/61: clear
271/62: clear
272/1: clear
272/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
272/3: clear
272/4: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
272/5: clear
272/6: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
272/7: clear
272/8: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
272/9: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
272/10: clear
272/11: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
272/12: clear
272/13:
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000
272/14: self = mercuryGUI
272/15:
self.xData = range(0, 10000)
self.yDataT = [295] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000
272/16: clear
272/17:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))
272/18: self._update_plot()
272/19: clear
272/20: self
272/21: clear
273/1: clear
273/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
273/3:
self = mercuryGUI
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000
273/4: clear
273/5:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_plot()
273/6: clear
274/1: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
274/2:
self = mercuryGUI
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000
274/3: clear
274/4:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_plot()
274/5: clear
274/6: self.mplwindow.setContentsMargins(0, 0, 0, 0)
274/7: self.ax2.axis(self.xLim + [0, 1.05])
274/8: self.canvas.draw()
274/9: clear
274/10: self.fig.set_facecolor('white')
274/11: self.canvas.draw()
274/12: self.ax2.set_xlabel('', fontsize=9)
274/13: self.canvas.draw()
274/14: self.ax2.set_xlabel('Time', fontsize=9)
274/15: self.canvas.draw()
274/16: clear
274/17: self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
274/18: self.canvas.draw()
274/19: self.fig.subplots_adjust(left=10, bottom=10, right=10, top=10, wspace=0, hspace=0)
274/20: clear
274/21: self.fig.subplots_adjust(left=0, bottom=0, right=10, top=10, wspace=0, hspace=0)
274/22: self.canvas.draw()
274/23: self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
274/24: self.canvas.draw()
274/25: self.fig.subplots_adjust(left=0, bottom=0, right=0.9, top=0.9, wspace=0, hspace=0)
274/26: self.canvas.draw()
274/27: self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0, hspace=0)
274/28: self.canvas.draw()
274/29: clear
274/30: self.fig.subplots_adjust(left=0.2, bottom=0.2, right=0.9, top=0.9, wspace=0, hspace=0)
274/31: self.canvas.draw()
274/32: self.ax2.set_xticks([])
274/33: self.canvas.draw()
274/34: clear
274/35:
self.ax2.set_xlabel('', fontsize=9)
self.ax2.set_ylabel('', fontsize=9)
274/36: self.canvas.draw()
274/37: self.fig.subplots_adjust(left=0.1, bottom=0, right=0.9, top=0.9, wspace=0, hspace=0)
274/38: self.canvas.draw()
274/39: self.fig.subplots_adjust(left=0.1, bottom=001, right=0.9, top=0.9, wspace=0, hspace=0)
274/40: clear
274/41: self.fig.subplots_adjust(left=0.1, bottom=0.01, right=0.99, top=0.9, wspace=0, hspace=0)
274/42: self.canvas.draw()
274/43: self.fig.subplots_adjust(left=0.1, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0)
274/44: self.canvas.draw()
274/45:
color = QtGui.QPalette().window().color().getRgb()
color = [x/255.0 for x in color]
274/46: self.fig.set_facecolor(color)
274/47: self.canvas.draw()
274/48: clear
274/49: self.fig.subplots_adjust(left=0.2, bottom=0.01, right=0.9, top=0.99, wspace=0, hspace=0)
274/50: self.canvas.draw()
274/51: clear
274/52: clear
274/53:
self.ax1.tick_params(axis='both', which='major', direction='in',
                     pad=-20, labelsize=9)
274/54: self.canvas.draw()
274/55:
self.ax1.tick_params(axis='both', which='major', direction='in',
                     pad=-50, labelsize=9)
274/56: self.canvas.draw()
274/57:
self.ax1.tick_params(axis='both', which='major', direction='in',
                     pad=-40, labelsize=9)
274/58: self.canvas.draw()
274/59:
self.ax1.tick_params(axis='both', which='major', direction='in',
                  labelsize=9)
274/60: self.canvas.draw()
274/61:
self.ax1.tick_params(axis='both', which='major', direction='in',
                     pad=0, labelsize=9)
274/62: self.canvas.draw()
274/63:
self.ax1.tick_params(axis='both', which='major', direction='in',
                     pad=10, labelsize=9)
274/64: self.canvas.draw()
274/65:
self.ax1.tick_params(axis='both', which='major', direction='in',
                     pad=4, labelsize=9)
274/66: self.canvas.draw()
274/67: clear
274/68: clear
274/69: direct = os.path.dirname(os.path.realpath('utils'))
274/70: direct
274/71: direct = os.path.dirname(os.path.realpath('utils'))
274/72: os.path.join(direct, 'utils','mpl_bright_style.mplstyle')
274/73: clear
274/74: clear
275/1: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
275/2: clear
275/3: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
275/4: clear
276/1: clear
276/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
276/3: clear
276/4: self = mercuryGUI
276/5: self.ax1.xaxis.label.set_color([0.5,0.5,0.5,1])
276/6: self.canvas.draw()
276/7: self.ax1.yaxis.label.set_color([0.5,0.5,0.5,1])
276/8: self.canvas.draw()
276/9: self.ax1.yaxis.label.set_color([0,0,0,1])
276/10: self.canvas.draw()
276/11: self.ax1.spines['bottom'].set_color([0.5,0.5,0.5,1])
276/12: self.canvas.draw()
276/13: self.ax1.spines['top'].set_color([0.5,0.5,0.5,1])
276/14: self.canvas.draw()
276/15: self.ax1.axhline(linewidth=1)
276/16: self.ax1.axvline(linewidth=1)
276/17: self.canvas.draw()
276/18: clear
277/1: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
277/2: clear
278/1: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
278/2: clear
278/3: exig
279/1: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
280/1: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
280/2: exi
281/1: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
281/2: self.fig.subplots_adjust(left=0.15, right=0.1)
281/3: clear
281/4: self=mercuryGUI
281/5: self.fig.subplots_adjust(left=0.15, right=0.1)
281/6: clear
281/7: self.fig.subplots_adjust(left=0.15, right=0.85)
281/8: self.canvas.draw()
281/9: self.fig.subplots_adjust(left=0.1, right=0.9)
281/10: self.canvas.draw()
281/11: self.fig.subplots_adjust(left=0.1, right=0.95)
281/12: self.canvas.draw()
281/13: self.fig.subplots_adjust(left=0.08, right=0.95)
281/14: self.canvas.draw()
281/15: self.fig.subplots_adjust(left=0.09, right=0.95)
281/16: self.canvas.draw()
281/17: self.fig.subplots_adjust(left=0.08, right=0.95)
281/18: self.canvas.draw()
281/19: self.fig.subplots_adjust(left=0.08, right=0.92)
281/20: self.canvas.draw()
281/21: self.fig.subplots_adjust(left=0.08, right=0.93)
281/22: self.canvas.draw()
281/23: self.fig.subplots_adjust(left=0.1, right=0.93)
281/24: self.canvas.draw()
281/25: self.fig.subplots_adjust(left=0.1, right=0.92)
281/26: self.canvas.draw()
281/27: self.fig.subplots_adjust(left=0.1, right=0.93)
281/28: self.canvas.draw()
281/29: clear
281/30: self.fig.subplots_adjust(hspace=0, bottom=0.03, top=0.97, left=0.1, right=0.93)
281/31: self.canvas.draw()
281/32: self.fig.subplots_adjust(hspace=0, bottom=0.03, top=0.97, left=0.1, right=0.93)
281/33: clear
282/1: clear
282/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
282/3:
self = mercuryGUI
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000
282/4: clear
282/5:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_plot()
282/6: clear
282/7: self.fig.subplots_adjust(hspace=0, bottom=0.03, top=0.97, left=0.1, right=0.93)
282/8: self.canvas.draw()
282/9: self.fig.subplots_adjust(hspace=0, bottom=0.03, top=0.97, left=0.15, right=0.90)
282/10: self.canvas.draw()
282/11: self.fig.subplots_adjust(hspace=0, bottom=0.03, top=0.97, left=0.11, right=0.93)
282/12: self.canvas.draw()
282/13: self.fig.subplots_adjust(hspace=0, bottom=0.03, top=0.97, left=0.1, right=0.92)
282/14: self.canvas.draw()
282/15: self.fig.subplots_adjust(hspace=0, bottom=0.03, top=0.97, left=0.11, right=0.92)
282/16: self.canvas.draw()
282/17: self.fig.subplots_adjust(hspace=0, bottom=0.03, top=0.97, left=0.11, right=0.91)
282/18: self.canvas.draw()
282/19: self.fig.subplots_adjust(hspace=0, bottom=0.03, top=0.97, left=0.11, right=0.93)
282/20: self.canvas.draw()
282/21: clear
283/1: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
283/2:
self = mercuryGUI
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000
283/3:
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_plot()
285/1: clear
285/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
285/3: clear
285/4:
keithleyGUI.ax1.tick_params(axis='both', which='major', direction='in',
                     colors='black', color=[0.5, 0.5, 0.5, 1],
                     labelsize=9)
285/5:
keithleyGUI.ax.tick_params(axis='both', which='major', direction='in',
                     colors='black', color=[0.5, 0.5, 0.5, 1],
                     labelsize=9)
285/6: clear
285/7: keithleyGUI.canvas.draw()
285/8: clear
285/9: clear
285/10: clear
286/1: clear
286/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
286/3: clear
287/1: clear
287/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
287/3: clear
287/4:
INFO:qdarkstyle:Found QT_API='pyqt5'
INFO:qdarkstyle:Using Qt wrapper = PyQt5 
clear
287/5: clear
287/6: goDark()
287/7: clear
287/8: go_drak()
287/9: go_dark()
287/10: go_bright()
288/1: clear
288/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
288/3: clear
288/4: clear
288/5: clear
289/1: clear
289/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
289/3: clear
289/4: rand(1)
289/5: clear
289/6:
self = mercuryGUI
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = [0.5] * 10000
self.yDataH = [0.2] * 10000

self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]
289/7: clear
289/8:
# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_plot()
289/9:
# system imports
import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor
289/10: clear
289/11:
# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_plot()
289/12:
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = range(0, 10000/10000, 1/10000)
self.yDataH = range(10000/10000, 0, 1/10000)
289/13:
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = range(0, 10000/10000.0, 1/10000.0)
self.yDataH = range(10000/10000.0, 0, 1/10000.0)
289/14: clear
289/15: self.xData = range(0, 10000,100)
289/16: self.xData
289/17: len(self.xData)
289/18: clear
289/19: self.xData = range(0, 10000,1000)
289/20: clear
289/21: len(self.xData)
289/22: clear
289/23: self.yDataT = [297.5] * 10
289/24:
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]
289/25: len(self.yDataG)
289/26: len(self.yDataH)
289/27: clear
289/28:
# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_plot()
289/29: clear
289/30: self.yDataH = [0, 0.1,1, 0.9, 0.1, 0.1, 0, 0, 0, 0]
289/31: clear
289/32:
# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                             [60.0] * len(xDataZero)))

self._update_plot()
289/33: clear
289/34: self
289/35: self.line_t
289/36: self.line_t.set_color('lime')
289/37: self.canvas.draw()
289/38: self.line_t.set_color('lightgreen')
289/39: self.canvas.draw()
289/40: self.line_t.set_color('green')
289/41: self.canvas.draw()
289/42: self.line_t.set_color([174/255.0, 229/255.0, 131/255.0, 255/255.0])
289/43: self.canvas.draw()
289/44: [174/255.0, 229/255.0, 131/255.0, 255/255.0]
289/45: self.canvas.draw()
289/46: self.line_t.set_color([0.7,0.9,0.5,1])
289/47: self.canvas.draw()
289/48: self.line_t.set_color([0.7,0.8,0.4,1])
289/49: self.canvas.draw()
289/50: self.line_t.set_color([0.8,0.8,0.4,1])
289/51: self.canvas.draw()
289/52: self.line_t.set_color([0.6,0.8,0.6,1])
289/53: self.canvas.draw()
289/54: self.line_t.set_linewidth(1.0)
289/55: self.canvas.draw()
289/56: self.line_t.set_linewidth(12)
289/57: self.line_t.set_linewidth(2)
289/58: self.canvas.draw()
289/59: self.line_t.set_linewidth(1.5)
289/60: self.canvas.draw()
289/61: self.line_t.set_linewidth(1.1)
289/62: self.canvas.draw()
289/63: clear
289/64: self.line_t.set_color('lime')
289/65: self.canvas.draw()
289/66: self.line_t.set_color('green')
289/67: self.canvas.draw()
289/68: self.line_t.set_color([0,0.8,0.6,1])
289/69: self.canvas.draw()
289/70: self.line_t.set_color([0,1,0.6,1])
289/71: self.canvas.draw()
289/72: self.line_t.set_color([0,0.8,0.6,1])
289/73: self.canvas.draw()
289/74: clear
289/75: clear
290/1: clear
291/1: clear
291/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
291/3: self = mercuryGUI
291/4:
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = range(0, 10000/10000, 1/10000)
self.yDataH = range(10000/10000, 0, 1/10000)

self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = range(0, 10000/10000.0, 1/10000.0)
self.yDataH = range(10000/10000.0, 0, 1/10000.0)
291/5: clear
291/6:
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = range(0, 10000/10000.0, 1/10000.0)
self.yDataH = range(10000/10000.0, 0, 1/10000.0)
291/7:
self.xData = range(0, 10000)
self.yDataT = [297.5] * 10000
self.yDataG = range(0, 10000/10000, 1/10000.0)
self.yDataH = range(10000/10000, 0, 1/10000.0)
291/8: clear
291/9:
self.xData = range(0, 10000,1000)
clear
len(self.xData)
clear
self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]
291/10:
self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]
291/11: clear
291/12:
import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor
291/13: clear
291/14:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                          [60.0] * len(xDataZero)))
291/15: self._update_plot()
291/16: clear
291/17: self.yDataG = - self.yDataG
291/18: self.yDataG = [-x for x in self.yDataG]
291/19: clear
292/1: clear
292/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
292/3: self = mercuryGUI
292/4:
self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]

self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]
292/5:
import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor
292/6: self.yDataG = [-x for x in self.yDataG]
292/7: clear
292/8:
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                          [60.0] * len(xDataZero)))

self._update_plot()
292/9: self.xData]
292/10: self.xData
292/11: self.xData = range(0, 10000,1000)
292/12: clear
292/13:
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                          [60.0] * len(xDataZero)))

self._update_plot()
292/14: clear
293/1: clear
293/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
293/3:
self = mercuryGUI
self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]

self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]

import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor
293/4: self.xData = range(0, 10000,1000)
293/5:
self.xDataZero = list(map(operator.div, xDataZero,
                          [60.0] * len(xDataZero)))

self._update_plot()
293/6: clear
293/7:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                          [60.0] * len(xDataZero)))

self._update_plot()
293/8: clear
294/1: clear
294/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
294/3: clear
294/4: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
294/5:
self = mercuryGUI
self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]

self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]

import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor

self.xData = range(0, 10000,1000)
294/6: self.yDataG = [-x for x in self.yDataG]
294/7:
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                          [60.0] * len(xDataZero)))

self._update_plot()
294/8:
self.fc2 = [221/255.0, 61/255.0, 53/255.0, 0.3]
self.fc3 = [100/255.0, 171/255.0, 246/255.0, 0.3]
294/9:
self.fc2 = [221/255.0, 61/255.0, 53/255.0, 0.2]
self.fc3 = [100/255.0, 171/255.0, 246/255.0, 0.2]
294/10: clear
294/11: cleafr
294/12: clear
295/1: clear
295/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
295/3:
self = mercuryGUI
self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]

self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]

import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor

self.xData = range(0, 10000,1000)

self.yDataG = [-x for x in self.yDataG]
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                          [60.0] * len(xDataZero)))

self._update_plot()
295/4: clear
296/1: clear
296/2: runfile('/Users/samschott/Documents/Python/CustomXepr/mercury_gui/main.py')
296/3:
self = mercuryGUI
self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]

self.yDataT = [297.5] * 10
self.yDataG = [0, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.5, 0.3, 0]
self.yDataH = [0, 0.1, 0.8, 0.9, 0.7, 0.1, 0, 0, 0, 0]

import sys
import os
import platform
import subprocess
import time
from qtpy import QtGui, QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.figure import Figure
import operator
import numpy as np
import logging
from math import ceil, floor

self.xData = range(0, 10000,1000)

self.yDataG = [-x for x in self.yDataG]
# prevent data vector from exceeding 86400 entries
self.xData = self.xData[-86400:]
self.yDataT = self.yDataT[-86400:]
self.yDataG = self.yDataG[-86400:]
self.yDataH = self.yDataH[-86400:]

# convert yData to minutes and set current time to t = 0
xDataZero = list(map(operator.sub, self.xData,
                     [max(self.xData)] * len(self.xData)))
self.xDataZero = list(map(operator.div, xDataZero,
                          [60.0] * len(xDataZero)))

self._update_plot()
297/1: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
299/1: clear
299/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
299/3: clear
299/4: os.path.realpath('utils')
299/5: clear
299/6: os.path.realpath('utils')
299/7: os.path.basename()
299/8: os.path.basename('utils')
299/9: os.path.curdir()
299/10: os.path.curdir
299/11: clear
299/12: os.path.basename('utils')
299/13: os.path.realpath('utils)
299/14: clear
299/15: os.path.realpath('utils')
299/16: from untils import mpl_bright_style.mplstyle
299/17: from untils import mpl_bright_style
299/18: from utils import mpl_bright_style
299/19: clear
299/20: from utils import BRIGHT_STYLE_PATH, DARK_STYLE_PATH
299/21: clear
299/22: from utils.dark_style import BRIGHT_STYLE_PATH
299/23: clear
299/24: from utils.dark_style import BRIGHT_STYLE_PATH
299/25: import utils.dark_style
299/26: utils.dark_style.BRIGHT_STYLE_PATH
299/27: utils.dark_style.direct
299/28: os.path.join(utils.dark_style.direct, 'mpl_bright_style.mplstyle')
299/29: clear
299/30: runfile('/Users/samschott/Documents/Python/CustomXepr/utils/dark_style.py')
299/31: BRIGHT_STYLE_PATH
299/32: DARK_STYLE_PATH
300/1: clear
300/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
300/3: clear
300/4: self = mercuryGUI
300/5: self.gf1_edit.setStyleSheet('color:rgb(100,171,246)')
300/6: self.h1_edit.setStyleSheet('color:rgb(221,61,53)')
300/7: self.t1_reading.setStyleSheet('color:rgb(0,204,153)')
300/8: self.t1_reading.setStyleSheet('color:rgb(0,0,0)')
300/9: 'color:rgb(%s)' % self.lc1
300/10: 'color:rgb(%s)' % self.lc1*255
300/11: clear
300/12: 'color:rgb(%s)' % *self.lc1
300/13: 'color:rgb(%s)' % (*self.lc1)
300/14: clear
300/15: 'color:rgb(%s,%s,%s)' % (*self.lc1)
300/16: 'color:rgb(%s,%s,%s)' % self.lc1
300/17: 'color:rgb(%s,%s,%s)' % (self.lc1[0],self.lc1[1],self.lc1[2])
300/18: 'color:rgb(%s,%s,%s)' % (self.lc1[0]*255,self.lc1[1]*255,self.lc1[2]*255)
300/19: clear
300/20: self.gf1_edit.setStyleSheet('color:rgb(%s,%s,%s)' % (self.lc1[0]*255,self.lc1[1]*255,self.lc1[2]*255))
300/21: self.h1_edit.setStyleSheet('color:rgb(%s,%s,%s)' % (self.lc1[0]*255,self.lc1[1]*255,self.lc1[2]*255))
300/22: clear
300/23:
self.gf1_edit.setStyleSheet('color:rgb(%s,%s,%s)' % (self.lc1[0]*255,self.lc1[1]*255,self.lc1[2]*255))
self.h1_edit.setStyleSheet('color:rgb(%s,%s,%s)' % (self.lc2[0]*255,self.lc2[1]*255,self.lc2[2]*255))
300/24: self.gf1_edit.setStyleSheet('color:rgb(100,171,246)')
300/25: self.gf1_edit.setStyleSheet('color:rgb(100,171,246)')
300/26: self.t1_reading.setStyleSheet('color:rgb(0,204,153)')
300/27: self.gf1_edit.setStyleSheet('color:rgb(100,171,246)')
300/28: self.t1_reading.setStyleSheet('color:rgb(0,0,0)')
300/29: clear
300/30: self.gf1_edit.setStyleSheet('color:rgb(100,171,246)' % (self.lc1[0]*255,self.lc1[1]*255,self.lc1[2]*255))
300/31: self.gf1_edit.setStyleSheet('color:rgb(%s,%s,%s)' % (self.lc1[0]*255,self.lc1[1]*255,self.lc1[2]*255))
300/32: self.gf1_edit.setStyleSheet('color:rgb(%s)' % self.lc1)
300/33: 'color:rgb(%s)' % self.lc1
300/34: 'color:rgb(%s)' % *self.lc1
300/35: clear
300/36: QtGui.QColor(self.lc0)
300/37: clear
300/38: self.gf1_edit.setTextColor(self.lc1)
300/39: [i * 255 for i in self.lc1]
300/40: 'color:rgb(%s,%s,%s)' % tuple([i * 255 for i in self.lc1])
300/41: clc
300/42: clear
300/43: clear
300/44:
self.gf1_edit.setStyleSheet('color:rgb(%s,%s,%s)' % tuple([i * 255 for i in self.lc1]))
self.h1_edit.setStyleSheet('color:rgb(%s,%s,%s)' % tuple([i * 255 for i in self.lc2]))
300/45:
self.gf1_unit.setStyleSheet('color:rgb(%s,%s,%s)' % tuple([i * 255 for i in self.lc1]))
self.h1_unit.setStyleSheet('color:rgb(%s,%s,%s)' % tuple([i * 255 for i in self.lc2]))
301/1: clear
301/2: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
302/1: clear
303/1: clear
305/1: clear
305/2: libname = 'libxeprapi_32.so' if ctypes.sizeof(ctypes.c_void_p) * 8 == 32 else 'libxeprapi.so'
305/3:
__author__ = 'Bruker BioSpin'
__version__ = 0.59
_msgprefix = 'Xepr API: '
import types, sys
if sys.version_info[0] != 2 or not sys.version_info[1] in [5, 6, 7]:
    raise ImportError('%sNeed Python V2.5.x, V2.6.x or V2.7.x to use XeprAPI' % _msgprefix)
import os, tempfile, re, ctypes
from ctypes import byref
from sys import stderr
from pipes import quote
from exceptions import Exception
try:
    import numpy as NP
    _tmp = [ int(x) for x in NP.__version__.strip().split('.') ]
    if _tmp[0] < 1 or _tmp[0] == 1 and _tmp[1] < 2:
        raise Exception
    if _tmp[0] == 1 and _tmp[1] == 2 and len(_tmp) == 3 and _tmp[2] < 1:
        raise Exception
except:
    raise ImportError('%sNeed recent (>= V1.2.1) Numpy package for Python' % _msgprefix)

try:
    import multiprocessing as MP
except:
    import Queue

try:
    import Tkinter as tk
except:
    pass

try:
    ctypes.c_bool
except:
    ctypes.c_bool = ctypes.c_byte
305/4: clear
305/5: libname = 'libxeprapi_32.so' if ctypes.sizeof(ctypes.c_void_p) * 8 == 32 else 'libxeprapi.so'
305/6: libname
305/7: clear
307/1: clear
   1: clear
   2: from queue import Queue
   3: clear
   4: runfile('/Users/samschott/Documents/Python/CustomXepr/startup.py')
   5: clear
   6: history
   7: %history -g
   8: %hist -o -g -f ipython_history.md
