"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""

import sys
from qtpy import QtCore, QtWidgets


class ReadingsOverview(QtWidgets.QDialog):
    def __init__(self, mercury):
        super(self.__class__, self).__init__()
        self.mercury = mercury
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName('ITC Readings Overview')
        Form.resize(500, 142)
        self.masterGrid = QtWidgets.QGridLayout(Form)
        self.masterGrid.setObjectName('gridLayout')

        # create main tab widget
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName('tabWidget')

        # get number of modules
        self.ntabs = len(self.mercury.modules)
        self.tab = [None]*self.ntabs
        self.gridLayout = [None]*self.ntabs
        self.comboBox = [None]*self.ntabs
        self.lineEdit = [None]*self.ntabs
        self.label = [None]*self.ntabs

        # create a tab for each module
        for i in range(0, self.ntabs):
            self.tab[i] = QtWidgets.QWidget()
            self.tab[i].setObjectName('tab_%s' % str(i))

            self.gridLayout[i] = QtWidgets.QGridLayout(self.tab[i])
            self.gridLayout[i].setContentsMargins(0, 0, 0, 0)
            self.gridLayout[i].setObjectName('gridLayout_%s' % str(i))

            self.label[i] = QtWidgets.QLabel(self.tab[i])
            self.label[i].setObjectName('label_%s' % str(i))
            self.gridLayout[i].addWidget(self.label[i], 0, 0, 1, 2)

            self.comboBox[i] = QtWidgets.QComboBox(self.tab[i])
            self.comboBox[i].setObjectName('comboBox_%s' % str(i))
            self.gridLayout[i].addWidget(self.comboBox[i], 1, 0, 1, 1)

            self.lineEdit[i] = QtWidgets.QLineEdit(self.tab[i])
            self.lineEdit[i].setObjectName('lineEdit_%s' % str(i))
            self.gridLayout[i].addWidget(self.lineEdit[i], 1, 1, 1, 1)

            self.tabWidget.addTab(self.tab[i], self.mercury.modules[i].nick)

        # fill combobox with information
        for i in range(0, self.ntabs):
            attr = dir(self.mercury.modules[i])
            EXEPT = ['read', 'write', 'query', 'CAL_INT', 'EXCT_TYPES',
                     'TYPES', 'clear_cache']
            readings = [x for x in attr if not (x.startswith('_') or x in EXEPT)]
            self.comboBox[i].addItems(readings)
            self._get_Reading(module_index=i)
            self.comboBox[i].currentIndexChanged.connect(self._get_Reading)

        # add tab widget to main grid
        self.masterGrid.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # get readings and alarms
        for i in range(0, self.ntabs):
            self._get_Reading(module_index=i)
            self._get_Alarms(module_index=i)

    def _get_Reading(self, select_index=None, module_index=None):

        i = module_index
        if i is None:
            self.activeBox = self.focusWidget()
            boxName = str(self.activeBox.objectName())
            i = int(boxName[-1])

        self.getreading = 'self.mercury.modules[%s].' % str(i) + str(self.comboBox[i].currentText())
        reading = eval(self.getreading)
        if type(reading) == tuple:
            reading = ''.join(map(str, reading))
        reading = str(reading)
        self.lineEdit[i].setText(reading)

    def _get_Alarms(self, module_index):

        # get alarms for all modules
        i = module_index
        address = self.mercury.modules[i].address.split(':')
        short_address = address[1]
        if self.mercury.modules[i].nick == 'LOOP':
            short_address = short_address.split('.')
            short_address = short_address[0] + '.loop1'
        try:
            alarm = self.mercury.alarms[short_address]
        except KeyError:
            alarm = '--'

        self.label[i].setText('Alarms: %s' % alarm)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('ITC Readings Overview',
                                       'ITC Readings Overview'))
