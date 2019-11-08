# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
import math
import numpy as np
import time

from lmfit import Model
from lmfit.models import PolynomialModel


def lorentz_peak(x, x0, w, a):
    """
    Lorentzian with area `a`, full-width-at-half-maximum `w`, and center `x0`.
    """

    numerator = 2/math.pi * w
    denominator = 4*(x - x0)**2 + w**2
    return a * numerator / denominator


class ModePicture(object):
    """
    Class to store mode pictures. It provides methods to calculate Q-values,
    and save and load mode picture data from and to .txt files.

    If several mode pictures with different zoom factors are given,
    :class:`ModePicture` will rescale and combine the data into a single mode
    picture.

    :param dict mode_pic_data: Dict with zoom factors as keys and respective mode picture
        data sets as values.
    :param filepath: Path to file with saved mode picture data.
    :param float freq: Cavity resonance frequency in GHz as float.

    :ivar x_data_mhz: Numpy array with x-axis data of mode picture in MHz.
    :ivar x_data_points: Numpy array with x-axis data of mode picture in pts.
    :ivar y_data: Mode picture y-axis data (absorption of cavity).
    :ivar freq0: Center frequency of cavity resonance.
    :ivar qvalue: Fitted Q-Value.
    :ivar qvalue_stderr: Standard error of Q-Value from fitting.
    """

    def __init__(self, mode_pic_data=None, filepath=None, freq=9.385):

        if not (filepath or mode_pic_data) or (filepath and mode_pic_data):
            raise ValueError('You must either give mode picture data or a file path.')

        if mode_pic_data is None:
            self.x_data_mhz, self.x_data_points, self.y_data, self.freq0 = self.load(filepath)
        else:
            if not isinstance(mode_pic_data, dict):
                raise TypeError('"mode_pic_data" must be a dictionary containing ' +
                                'mode pictures for with different zoom factors.')

            self.mode_pic_data = mode_pic_data
            self.freq0 = freq

            self.zoom_factors = list(mode_pic_data.keys())
            self.x_data_mhz, self.x_data_points, self.y_data = self.combine_data(mode_pic_data)

        self.qvalue, self.fit_result = self.fit_qvalue(self.x_data_points, self.y_data)
        self.qvalue_stderr = self.get_qvalue_stderr()

    @staticmethod
    def _points_to_mhz(n_points, zf, x0):
        """
        Converts an x-axis from points to MHz according to the mode picture's zoom factor.

        :param int n_points: Number of data points in mode picture.
        :param int zf: Zoom factor, i.e., scaling factor of x-axis. Typically is 1, 2, 4,
            or 8.
        :param int x0: Center of axis corresponding to `freq0`.
        :returns: X-axis of mode picture in MHz.
        :rtype: np.array
        """
        x_axis_points = np.arange(0, n_points)
        x_axis_mhz = 1e-3 / (2 * zf) * (x_axis_points - x0)

        return x_axis_mhz

    def combine_data(self, mode_pic_data):
        """
        Rescales mode pictures from different zoom factors and combines them to one.

        :param dict mode_pic_data: Dict with zoom factors as keys and
            respective mode picture curves as values.
        :returns: `(x_axis_mhz_comb, x_axis_points_comb, mode_pic_comb)` where
            `x_axis_mhz_comb` and `x_axis_points_comb` are the combined x-axis
            values of all mode pictures in mhz and points, respectively, and
            `mode_pic_comb` is the combines y-axis data in a.u..
        """
        n_points = len(next(iter(mode_pic_data.values())))
        x_axis_points = np.arange(0, n_points)

        x_axis_mhz = {}

        # rescale x-axes according to zoom factor
        for zf in mode_pic_data.keys():
            q_value, fit_rslt = self.fit_qvalue(x_axis_points, mode_pic_data[zf], zf)
            x_axis_mhz[zf] = self._points_to_mhz(n_points, zf, fit_rslt.best_values['x0'])

        # combine data from all zoom factors
        x_axis_mhz_comb = np.concatenate(list(x_axis_mhz.values()))
        mode_pic_comb = np.concatenate(list(mode_pic_data.values()))

        # sort arrays in order of ascending frequency
        indices = np.argsort(x_axis_mhz_comb)
        x_axis_mhz_comb = x_axis_mhz_comb[indices]
        mode_pic_comb = mode_pic_comb[indices]
        x_axis_points_comb = 2 / 1e-3 * x_axis_mhz_comb

        return x_axis_mhz_comb, x_axis_points_comb, mode_pic_comb

    @staticmethod
    def _get_fit_starting_points(x_data, y_data):
        """
        Returns plausible starting points for least square Lorentzian fit.
        """
        # find center dip
        peak_center = x_data[np.argmin(y_data)]

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

        return peak_center, fwhm, peak_area

    def fit_qvalue(self, x_data, y_data, zoom_factor=1):
        """
        Least square fit of Lorentzian and polynomial background to mode picture.

        :param x_data: Iterable containing x-data of mode picture in points.
        :param y_data: Iterable containing y-data of mode picture in a.u..
        :param zoom_factor: Zoom factor (scaling factor of x-axis).
        :returns: (q_value, fit_result) where `fit_result` is a
        """
        # get first guess parameters for Lorentzian fit
        peak_center, fwhm, peak_area = self._get_fit_starting_points(x_data, y_data)

        # set up fit models for polynomial background and Lorentzian dip
        pmod = PolynomialModel(degree=7)
        lmodel = Model(lorentz_peak)

        mode_picture_model = pmod - lmodel

        # isolate back ground area from resonance dip
        idx1 = sum((x_data < (peak_center - 3 * fwhm)))
        idx2 = sum((x_data > (peak_center + 3 * fwhm)))

        x_bg = np.concatenate((x_data[0:idx1], x_data[-idx2:-1]))
        y_bg = np.concatenate((y_data[0:idx1], y_data[-idx2:-1]))

        # get first guess parameters for background
        pars = pmod.guess(y_bg, x=x_bg)

        # add fit parameters for Lorentzian resonance dip
        pars.add_many(('x0', peak_center, True, None, None, None, None),
                      ('w', fwhm, True, None, None, None, None),
                      ('a', peak_area, True, None, None, None, None))

        # perform full fit
        fit_result = mode_picture_model.fit(y_data, pars, x=x_data)

        # calculate Q-value from resonance width
        delta_freq = fit_result.best_values['w'] * 1e-3 / (2 * zoom_factor)
        q_value = round(self.freq0 / delta_freq, 1)

        return q_value, fit_result

    def get_qvalue_stderr(self):
        """
        Determines 1 sigma confidence bounds for Q-value.

        :returns: Standard error of Q-value from fitting.
        :rtype: float
        """

        delta_freq = self.fit_result.params['w'].value * 1e-3 / 2
        delta_freq_stderr = self.fit_result.params['w'].stderr * 1e-3 / 2

        qvalue_stderr = round(self.freq0 / delta_freq**2 * delta_freq_stderr, 1)

        return qvalue_stderr

    def plot(self):
        """
        Plots mode picture and the least squares fit used to determine the Q-value.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError('matplotlib is required for plotting.')

        comps = self.fit_result.eval_components(x=self.x_data_points)
        offset = self.fit_result.best_values['c0']

        yfit = self.fit_result.best_fit
        lz = offset - comps['lorentz_peak']

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.x_data_mhz, self.y_data, '.', color='#2980B9', label='Mode picture')
        ax.plot(self.x_data_mhz, lz, '--', color='#000000', label='Cavity dip')
        ax.plot(self.x_data_mhz, yfit, '-', color='#C70039', label='Total fit')

        ax.legend()
        ax.set_xlabel('Microwave frequency [MHz]')
        ax.set_ylabel('Microwave absorption [a.u.]')

        fig.show()

    def save(self, filepath):
        """
        Saves mode picture data as a text file with headers. If no file path
        is given, the user is prompted to select a location and name through a
        user interface.

        :param str filepath: Absolute file path.
        """
        # create header and title for file
        time_str = time.strftime('%H:%M, %d/%m/%Y')
        title = ['Cavity mode picture, recorded at {}'.format(time_str),
                 'Center frequency = {:0.3f} GHz'.format(self.freq0)]
        title = '\n'.join(title)

        header = ['freq [MHz]', 'MW abs. [a.u.]']
        header = '\t'.join(header)

        data_matrix = np.concatenate(([self.x_data_mhz], [self.y_data]), axis=0)

        # noinspection PyTypeChecker
        np.savetxt(filepath, data_matrix.T, fmt='%.9E', delimiter='\t', header=title+header)

    @staticmethod
    def load(filepath):
        """
        Loads mode picture data from text file.

        :param str filepath: Absolute path to file.
        :returns: `(x_axis_mhz_comb, x_axis_points_comb, mode_pic_comb, freq0)`
            where `x_axis_mhz_comb` and `x_axis_points_comb` are the combined
            x-axis values of all mode pictures in mhz and points, respectively,
            `mode_pic_comb` is the combines y-axis data in a.u. and `freq0` is
            the center resonance frequency.
        """

        data_matrix = np.loadtxt(filepath)
        x_axis_mhz_comb = data_matrix[:, 0]
        mode_pic_comb = data_matrix[:, 1]

        x_axis_points_comb = 2 / 1e-3 * x_axis_mhz_comb

        freq = None
        with open(filepath, 'r') as fh:
            for line in fh:
                if 'GHz' in line:
                    freq = list(filter(lambda x: x in '0123456789.', line))
                    freq = ''.join(freq)
                    break

        if freq is None:
            raise RuntimeError('Could not find frequency information.')

        freq0 = float(freq[0])

        return x_axis_mhz_comb, x_axis_points_comb, mode_pic_comb, freq0


    def __repr__(self):
        return '<{0}(QValue = {1}+/-{2}, freq = {3}GHz)>'.format(
            self.__class__.__name__, self.qvalue, self.qvalue_stderr, round(self.freq0, 4))
