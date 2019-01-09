#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 14:03:29 2017

@author: SamSchott
"""
from __future__ import division, absolute_import
import math
import re
import numpy as np
from lmfit import Model
from lmfit.models import PolynomialModel
import matplotlib.pyplot as plt
import time


def lorentz_peak(x, x0, w, A):
    """
    Lorentzian with area A and fwhm w centered around x0.
    """

    numerator = 2/math.pi * w
    denominator = 4*(x - x0)**2 + w**2
    return A * numerator / denominator


class ModePicture(object):
    """
    Class to store mode pictures, calculate QValues and save the mode
    picture data as a .txt file.
    """

    def __init__(self, mode_pic_data=None, freq=9.385):
        """
        :param dict mode_pic_data: Dict with zoom factors as keys and respective mode picture curves as values.
        :param float freq: Cavity resonance frequency in GHz as float.
        """
        if mode_pic_data is None:
            self.x_axis_mhz_comb, self.x_axis_points_comb, self.mode_pic_comb, self.freq0 = self.load()
        else:

            if not isinstance(mode_pic_data, dict):
                raise TypeError('"mode_pic_data" must be a dictionary containing ' +
                                'mode pictures for with different zoom factors.')

            self.mode_pic_data = mode_pic_data
            self.freq0 = freq

            self.zoomFactors = mode_pic_data.keys()
            self.x_axis_mhz_comb, self.x_axis_points_comb, self.mode_pic_comb = self.combine_data(mode_pic_data)

        self.qvalue, self.fit_result = self.fit_qvalue(self.x_axis_points_comb, self.mode_pic_comb)

    def _points_to_mhz(self, n_points, zf, x0):
        """
        Converts an x-axis from points to MHz according to the mode picture's zoom factor.

        :param int n_points: Number of data points in mode picture.
        :param int zf: Zoom factor (1, 2, 4, 8).
        :param int x0: Center of axis correspoding to `freq0`.
        :return: X-axis of mode picture in MHz.
        :rtype: np.array
        """
        x_axis_points = np.arange(0, n_points)
        x_axis_mhz = 1e-3 / (2 * zf) * (x_axis_points - x0)

        return x_axis_mhz

    def combine_data(self, mode_pic_data):
        """
        Rescales mode pictures from different zoom factors and combines them to one.

        :param dict mode_pic_data: Dict with zoom factors as keys and respective mode picture curves as values.
        """
        n_points = len(mode_pic_data.values()[0])
        x_axis_points = np.arange(0, n_points)

        x_axis_mhz = {}

        # rescale x-axes according to zoom factor
        for zooom_fact in mode_pic_data.keys():
            rlst = self.fit_qvalue(x_axis_points, mode_pic_data[zooom_fact], zooom_fact)
            x_axis_mhz[zooom_fact] = self._points_to_mhz(n_points, zooom_fact, rlst.best_values['x0'])

        # combine data from all zoom factors
        x_axis_mhz_comb = np.concatenate(x_axis_mhz.values())
        mode_pic_comb = np.concatenate(mode_pic_data.values())

        # sort arrays in order of ascending frequency
        indices = np.argsort(x_axis_mhz_comb)
        x_axis_mhz_comb = x_axis_mhz_comb[indices]
        mode_pic_comb = mode_pic_comb[indices]
        x_axis_points_comb = 2 / 1e-3 * x_axis_mhz_comb

        return x_axis_mhz_comb, x_axis_points_comb, mode_pic_comb

    def _get_fit_starting_points(self, x_data, y_data):
        """
        Return plausible starting points for least square Lorentzian fit.
        """
        # find center dip
        peakCenter = x_data[np.argmin(y_data)]

        # find baseline height
        interval = 0.25
        n_points = len(x_data)
        bs1 = np.mean(y_data[0:int(n_points * interval)])
        bs2 = np.mean(y_data[-int(n_points * interval):-1])
        baseline = np.mean([bs1, bs2])

        # find peak area
        peak_height = baseline - np.min(y_data)
        peak_index = (y_data < peak_height / 2 + np.min(y_data))
        fwhm = max(np.max(x_data[peak_index]) - np.min(x_data[peak_index]), 1)
        peak_area = peak_height * fwhm * math.pi / 2

        return peakCenter, fwhm, peak_area

    def fit_qvalue(self, x_data, y_data, zoom_factor=1):
        """
        Least square fit of Lorentzian and polynomial background
        to mode picture.
        """
        peak_center, fwhm, peak_area = self._get_fit_starting_points(x_data, y_data)

        # perform peak fit
        pmod = PolynomialModel(degree=7)
        lmodel = Model(lorentz_peak)

        mode_picture_model = pmod - lmodel

        idx1 = sum((x_data < (peak_center - 3 * fwhm)))
        idx2 = sum((x_data > (peak_center + 3 * fwhm)))

        x_bg = np.concatenate((x_data[0:idx1], x_data[-idx2:-1]))
        y_bg = np.concatenate((y_data[0:idx1], y_data[-idx2:-1]))

        pars = pmod.guess(y_bg, x=x_bg)

        pars.add_many(('x0', peak_center, True, None, None, None, None),
                      ('w', fwhm, True, None, None, None, None),
                      ('A', peak_area, True, None, None, None, None))

        result = mode_picture_model.fit(y_data, pars, x=x_data)

        delta_freq = result.best_values['w'] * 1e-3 / (2 * zoom_factor)

        return round(self.freq0 / delta_freq, 1), result

    def plot(self):
        """
        Plot mode picture and least squares fit.
        """
        comps = self.fit_result.eval_components(x=self.x_axis_points_comb)
        offset = self.fit_result.best_values['c0']

        yfit = self.fit_result.best_fit
        lz = offset - comps['lorentz_peak']

        plt.plot(self.x_axis_mhz_comb, self.mode_pic_comb, '.', color='#2980B9')
        plt.plot(self.x_axis_mhz_comb, lz, 'k--')
        plt.plot(self.x_axis_mhz_comb, yfit, '-', color='#C70039')

        plt.legend(['Mode picture', 'Cavity dip', 'Total fit'])
        plt.xlabel('Microwave frequency [MHz]')
        plt.ylabel('Microwave absorption [a.u.]')

    def save(self, filepath=None):
        """
        Saves mode picture data as a text file with headers. If no filepath
        is given, the user is promted to select a location and name through a
        user interface.

        :param str filepath: Absolute filepath.
        """
        # create header and title for file
        time_str = time.strftime('%H:%M, %d/%m/%Y')
        title = ('# Cavity mode picture, recorded at %s\n'
                 '# Center frequency =  %0.3f GHz\n' % (time_str, self.freq0))

        header = ['freq [MHz]', 'MW abs. [a.u.]']
        header = '\t'.join(header)

        data_matrix = [self.x_axis_mhz_comb, self.mode_pic_comb]
        data_matrix = zip(*data_matrix)

        # save to file
        if filepath is None:
            from qtpy import QtWidgets
            prompt = 'Save as file'
            filename = 'untitled.txt'
            formats = 'Text file (*.txt)'
            filepath = QtWidgets.QFileDialog.getSaveFileName(None, prompt,
                                                             filename, formats)
            filepath = filepath[0]

        if len(filepath) > 4:
            np.savetxt(filepath, data_matrix, fmt='%.9E', delimiter='\t',
                       newline='\n', header=header, comments=title)

        return filepath

    def load(self, filepath=None):
        """
        Loads mode picture data from text file. If no filepath is given, the
        user is promted to select a location and name through a user interface.

        :param str filepath: Absolute filepath.
        """
        if filepath is None:
            from qtpy import QtWidgets
            prompt = 'Select mode picture file'
            filepath = QtWidgets.QFileDialog.getOpenFileName(None, prompt)
            filepath = filepath[0]

        if len(filepath) > 4:
            data_matrix = np.loadtxt(filepath, skiprows=3)
            x_axis_mhz_comb = data_matrix[:, 0]
            mode_pic_comb = data_matrix[:, 1]

            x_axis_points_comb = 2 / 1e-3 * x_axis_mhz_comb

            linestring = None
            with open(filepath, 'r') as fh:
                for line in fh:
                    if 'GHz' in line:
                        linestring = line
            if linestring:
                freq = re.findall("\d+\.\d+", linestring)
            else:
                raise RuntimeError('Could not find frequency information.')

            freq0 = float(freq[0])

            return x_axis_mhz_comb, x_axis_points_comb, mode_pic_comb, freq0
