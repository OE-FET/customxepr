#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 14:03:29 2017

@author: SamSchott
"""
from __future__ import division, unicode_literals, absolute_import
import math
import re
import numpy as np
from lmfit import Model
from lmfit.models import PolynomialModel
import matplotlib.pyplot as plt
import time
from qtpy import QtWidgets


def lorentz_peak(x, x0, w, A):
    """
    Lorentzian with area A and fwhm w centered around x0.
    """

    numerator = 2/math.pi * w
    denominator = 4*(x - x0)**2 + w**2
    return A * numerator / denominator


class ModePicture(object):

    def __init__(self, modePicData={}, freq=9.385):
        """
        Class to store mode pictures, calculate QValues and save the mode
        picture data as a .txt file.
        """

        if not isinstance(modePicData, dict):
            raise TypeError('"modePicData" must be a dictionary containing ' +
                            'mode pictures for with different zoom factors.')

        if modePicData == {}:
            self.load()
        else:
            self.modePicData = modePicData
            self.freq0 = freq

            self.zoomFactors = modePicData.keys()
            self.nPoints = len(modePicData.values()[0])
            self.xPoints = np.arange(0, self.nPoints)

            self.combineData()
        self.result = self.fitQValue(self.xPointsTot, self.modePicTot)

    def combineData(self):
        """
        Rescale mode pictures from different zoom factors and combine.
        """
        self.xMHz = {}

        for zf in self.zoomFactors:
            rlst = self.fitQValue(self.xPoints, self.modePicData[zf], zf)
            self.xMHz[zf] = 1e-3/(2*zf)*(self.xPoints - rlst.best_values['x0'])

        self.xMHzTot = np.concatenate(self.xMHz.values())
        self.modePicTot = np.concatenate(self.modePicData.values())

        indices = np.argsort(self.xMHzTot)
        self.xMHzTot = self.xMHzTot[indices]
        self.modePicTot = self.modePicTot[indices]
        self.xPointsTot = 2/1e-3 * self.xMHzTot

    def _getStartingPoints(self, xData, yData):
        """
        Get plausible starting points for least square fit.
        """
        # find center dip
        peakCenter = xData[np.argmin(yData)]
        # find baseline height
        interval = 0.25
        bs1 = np.mean(yData[0:int(self.nPoints*interval)])
        bs2 = np.mean(yData[-int(self.nPoints*interval):-1])
        baseline = np.mean([bs1, bs2])
        # find peak area
        peakHeight = baseline - np.min(yData)
        peakIndex = (yData < peakHeight/2 + np.min(yData))
        fwhm = max(np.max(xData[peakIndex]) - np.min(xData[peakIndex]), 1)
        peakArea = peakHeight * fwhm * math.pi / 2

        return peakCenter, fwhm, peakArea

    def fitQValue(self, xData, yData, modeZoom=1):
        """
        Least square fit of Lorentzian and polynomial background
        to mode picture.
        """
        peakCenter, fwhm, peakArea = self._getStartingPoints(xData, yData)

        # perform peak fit
        pmod = PolynomialModel(degree=7)
        lmodel = Model(lorentz_peak)

        modePictureModel = pmod - lmodel

        idx1 = sum((xData < (peakCenter - 3*fwhm)))
        idx2 = sum((xData > (peakCenter + 3*fwhm)))

        x_bg = np.concatenate((xData[0:idx1], xData[-idx2:-1]))
        y_bg = np.concatenate((yData[0:idx1], yData[-idx2:-1]))

        pars = pmod.guess(y_bg, x=x_bg)

        pars.add_many(('x0', peakCenter, True, None, None, None, None),
                      ('w', fwhm, True, None, None, None, None),
                      ('A', peakArea, True, None, None, None, None))

        result = modePictureModel.fit(yData, pars, x=xData)

        deltaFreq = result.best_values['w'] * 1e-3 / (2*modeZoom)

        self.QValue = round(self.freq0 / deltaFreq, 1)

        return result

    def plot(self):
        """
        Plot mode picture and least squares fit.
        """
        comps = self.result.eval_components(x=self.xPointsTot)
        offset = self.result.best_values['c0']

        self.yfit = self.result.best_fit
        self.lz = offset - comps['lorentz_peak']

        plt.plot(self.xMHzTot, self.modePicTot, '.', color='#2980B9')
        plt.plot(self.xMHzTot, self.lz, 'k--')
        plt.plot(self.xMHzTot, self.yfit, '-', color='#C70039')

        plt.legend(['Mode picture', 'Cavity dip', 'Total fit'])
        plt.xlabel('Microwave frequency [MHz]')
        plt.ylabel('Microwave absorption [a.u.]')

    def save(self, filepath=None):
        """
        Saves mode picture data as a text file with headers. If no filepath
        is given, the user is promted to select a location and name through a
        user interface.
        """
        # create header and title for file

        time_str = time.strftime('%H:%M, %d/%m/%Y')
        title = ('# Cavity mode picture, recorded at %s\n'
                 '# Center frequency =  %0.3f GHz\n' % (time_str, self.freq0))

        header = ['freq [MHz]', 'MW abs. [a.u.]']
        header = '\t'.join(header)

        data_matrix = [self.xMHzTot, self.modePicTot]
        data_matrix = zip(*data_matrix)

        # save to file
        if filepath is None:
            text = 'Please select file to save mode picture:'
            filepath = QtWidgets.QFileDialog.getSaveFileName(caption=text)
            filepath = filepath[0]

        if len(filepath) > 4:
            np.savetxt(filepath, data_matrix, fmt='%.9E', delimiter='\t',
                       newline='\n', header=header, comments=title)

        return filepath

    def load(self, filepath=None):

        if filepath is None:
            text = 'Please select file with mode picture data:'
            filepath = QtWidgets.QFileDialog.getOpenFileName(caption=text)
            filepath = filepath[0]

        if len(filepath) > 4:
            data_matrix = np.loadtxt(filepath, skiprows=3)
            self.xMHzTot = data_matrix[:, 0]
            self.modePicTot = data_matrix[:, 1]

            self.xPointsTot = 2/1e-3 * self.xMHzTot
            self.nPoints = len(self.xPointsTot)
            with open(filepath, 'r') as myfile:
                for line in myfile:
                    if 'GHz' in line:
                        linestring = line
            freq = re.findall("\d+\.\d+", linestring)
            self.freq0 = float(freq[0])
