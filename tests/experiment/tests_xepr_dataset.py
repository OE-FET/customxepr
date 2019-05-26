# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import, unicode_literals
import os
import unittest
import filecmp

from customxepr import XeprData, XeprParam

DIR = os.path.dirname(os.path.realpath(__file__))

PATH_ORIGINAL = DIR + '/cw_epr_power_sat'
PATH_NEW = DIR + '/cw_epr_power_sat_new'
EXTENTIONS = ('.DSC', '.DTA', '.YGF', '.ZSC')


class TestXeprData(unittest.TestCase):

    def test_load_save(self):
        """
        Test loading and saving BES3T data files form Xepr. Assert that the saved files
        have the same content as the original files. This test will fail in Python 2 since
        the order of sections will not be maintained.
        """

        # test loading and saving in the correct file format

        dset = XeprData(PATH_ORIGINAL + '.DSC')
        dset.save(PATH_NEW + '.DSC')

        for ext in EXTENTIONS:
            if os.path.isfile(PATH_ORIGINAL + ext):
                self.assertTrue(filecmp.cmp(PATH_ORIGINAL + ext, PATH_NEW + ext))

    def test_remove_param(self):
        """
        Test removing a parameter from :attr:`XeprData.pars`. Assert that the parameter is
        indeed gone.
        """
        dset = XeprData(PATH_ORIGINAL + '.DSC')
        del dset.pars['MWFQ']

        with self.assertRaises(KeyError):
            dset.pars['MWFQ']

    def test_add_param(self):
        """
        Test adding a new parameter to :attr:`XeprData.pars`. Assert that the parameter is
        saved to the appropriate location in the DSC file.
        """
        dset = XeprData(PATH_ORIGINAL + '.DSC')
        dset.pars['NewParam1'] = 1234
        dset.pars['NewParam2'] = XeprParam(1234, 'K/sec')
        dset.save(PATH_NEW + '.DSC')

        dset.load(PATH_NEW + '.DSC')

        self.assertEqual(dset.pars['NewParam1'].value, 1234)
        self.assertEqual(dset.pars['NewParam2'].value, 1234)

        self.assertEqual(dset.dsl.groups['customXepr'].pars['NewParam1'].value, 1234)
        self.assertEqual(dset.dsl.groups['customXepr'].pars['NewParam2'].value, 1234)

    def tearDown(self):
        """
        Delete created file.
        """
        for ext in EXTENTIONS:
            if os.path.isfile(PATH_NEW + ext):
                os.remove(PATH_NEW + ext)

if __name__ == '__main__':
    unittest.main()
