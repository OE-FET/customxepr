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

EXTENTIONS = ('.DSC', '.DTA', '.YGF', '.ZSC')


class TestXeprData(unittest.TestCase):

    PATH_ORIGINAL_2D = DIR + '/cw_epr_complex'
    PATH_NEW_2D = DIR + '/cw_epr_power_sat_new'

    PATH_ORIGINAL_CPLX = DIR + '/cw_epr_complex'
    PATH_NEW_CPLX = DIR + '/cw_epr_complex_new'

    def test_load_save_2d(self):
        """
        Test loading and saving BES3T 2D data files. Assert that the saved files have the
        same content as the original files. This test will fail in Python 2 since the
        order of sections will not be maintained.
        """

        # test loading and saving in the correct file format

        dset = XeprData(self.PATH_ORIGINAL_2D + '.DSC')
        dset.save(self.PATH_NEW_2D + '.DSC')

        for ext in EXTENTIONS:
            if os.path.isfile(self.PATH_ORIGINAL_2D + ext):
                self.assertTrue(filecmp.cmp(self.PATH_ORIGINAL_2D + ext,
                                            self.PATH_NEW_2D + ext))

    def test_modify_ordinate(self):
        """
        Tests getter and setter methods for ordinate data by verifying that the data does
        not change in a get / set cycle.
        """

        # test loading and saving in the correct file format

        dset = XeprData(self.PATH_ORIGINAL_2D + '.DSC')
        dset.o = dset.o  # should not change the actual content
        dset.save(self.PATH_NEW_2D + '.DSC')

        for ext in EXTENTIONS:
            if os.path.isfile(self.PATH_ORIGINAL_2D + ext):
                self.assertTrue(filecmp.cmp(self.PATH_ORIGINAL_2D + ext,
                                            self.PATH_NEW_2D + ext))

    def test_load_save_complex(self):
        """
        Test loading and saving BES3T data files with complex data. Assert that the saved
        files have the same content as the original files. This test will fail in Python 2
        since the order of sections will not be maintained.
        """

        # test loading and saving in the correct file format

        dset = XeprData(self.PATH_ORIGINAL_CPLX + '.DSC')
        dset.save(self.PATH_NEW_CPLX + '.DSC')

        for ext in EXTENTIONS:
            if os.path.isfile(self.PATH_ORIGINAL_CPLX + ext):
                self.assertTrue(filecmp.cmp(self.PATH_ORIGINAL_CPLX + ext,
                                            self.PATH_NEW_CPLX + ext))

    def test_remove_param(self):
        """
        Test removing a parameter from :attr:`XeprData.pars`. Assert that the parameter is
        indeed gone.
        """

        PATH_ORIGINAL = DIR + '/cw_epr_complex'

        dset = XeprData(self.PATH_ORIGINAL_2D + '.DSC')
        del dset.pars['MWFQ']

        with self.assertRaises(KeyError):
            dset.pars['MWFQ']

    def test_add_param(self):
        """
        Test adding a new parameter to :attr:`XeprData.pars`. Assert that the parameter is
        saved to the appropriate location in the DSC file.
        """

        dset = XeprData(self.PATH_ORIGINAL_2D + '.DSC')
        dset.pars['NewParam1'] = 1234
        dset.pars['NewParam2'] = XeprParam(1234, 'K/sec')
        dset.save(self.PATH_NEW_2D + '.DSC')

        dset.load(self.PATH_NEW_2D + '.DSC')

        self.assertEqual(dset.pars['NewParam1'].value, 1234)
        self.assertEqual(dset.pars['NewParam2'].value, 1234)

        self.assertEqual(dset.dsl.groups['customXepr'].pars['NewParam1'].value, 1234)
        self.assertEqual(dset.dsl.groups['customXepr'].pars['NewParam2'].value, 1234)

    def tearDown(self):

        new_files = [os.path.join(DIR, f) for f in os.listdir(DIR) if 'new' in f]

        for f in new_files:
            os.remove(f)

if __name__ == '__main__':
    unittest.main()
