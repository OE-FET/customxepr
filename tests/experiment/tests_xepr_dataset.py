# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
import os
import unittest
import filecmp


from customxepr.experiment.xepr_dataset import XeprData, XeprParam

DIR = os.path.dirname(os.path.realpath(__file__))
EXTENTIONS = (".DSC", ".DTA", ".YGF", ".ZSC")

TEST_FILES = (
    "cw_epr_angle_dep",
    "cw_epr_complex",
    "cw_epr_power_sat",
    "pulsed_edmr_rabi",
)


class TestXeprData(unittest.TestCase):
    def test_load_save(self):
        """
        Test loading and saving BES3T data files. Assert that the saved files have the
        same content as the original files. This test will fail in Python 2 since the
        order of sections will not be maintained.
        """

        # test loading and saving in the correct file format

        for file in TEST_FILES:
            old_path = os.path.join(DIR, file)
            new_path = os.path.join(DIR, file) + "_new"

            dset = XeprData(old_path + ".DSC")
            dset.save(new_path + ".DSC")

            for ext in EXTENTIONS:
                if os.path.isfile(old_path + ext):
                    self.assertTrue(
                        filecmp.cmp(old_path + ext, new_path + ext),
                        "different contents for {}".format(file + ext),
                    )

    def test_modify_ordinate(self):
        """
        Tests getter and setter methods for ordinate data by verifying that the data does
        not change in a get / set cycle.
        """

        # test loading and saving in the correct file format

        for file in TEST_FILES:
            old_path = os.path.join(DIR, file)
            new_path = os.path.join(DIR, file) + "_new"

            dset = XeprData(old_path + ".DSC")
            dset.o = dset.o  # should not change the actual content
            dset.save(new_path + ".DSC")

            for ext in EXTENTIONS:
                if os.path.isfile(old_path + ext):
                    self.assertTrue(
                        filecmp.cmp(old_path + ext, new_path + ext),
                        "different contents for {}".format(file + ext),
                    )

    def test_remove_param(self):
        """
        Test removing a parameter from :attr:`XeprData.pars`. Assert that the parameter is
        indeed gone.
        """

        PATH_ORIGINAL = os.path.join(DIR, TEST_FILES[1])

        dset = XeprData(PATH_ORIGINAL + ".DSC")
        del dset.pars["MWFQ"]

        with self.assertRaises(KeyError):
            dset.pars["MWFQ"]

    def test_add_param(self):
        """
        Test adding a new parameter to :attr:`XeprData.pars`. Assert that the parameter is
        saved to the appropriate location in the DSC file.
        """

        PATH_ORIGINAL = os.path.join(DIR, TEST_FILES[1])

        dset = XeprData(PATH_ORIGINAL + ".DSC")
        dset.pars["NewParam1"] = 1234
        dset.pars["NewParam2"] = XeprParam(1234, "K/sec")
        dset.save(PATH_ORIGINAL + "_new.DSC")

        dset.load(PATH_ORIGINAL + "_new.DSC")

        self.assertEqual(dset.pars["NewParam1"].value, 1234)
        self.assertEqual(dset.pars["NewParam2"].value, 1234)

        self.assertEqual(dset.dsl.groups["customXepr"].pars["NewParam1"].value, 1234)
        self.assertEqual(dset.dsl.groups["customXepr"].pars["NewParam2"].value, 1234)

    def tearDown(self):

        new_files = [os.path.join(DIR, f) for f in os.listdir(DIR) if "new" in f]

        for f in new_files:
            os.remove(f)


if __name__ == "__main__":
    unittest.main()
