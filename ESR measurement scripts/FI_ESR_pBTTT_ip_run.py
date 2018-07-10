Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 50, 10: 40, 20: 36, 30: 35, 50: 33, 80: 30, 110: 25, 140: 25, 170: 25, 200: 25, 230: 24, 260: 22, 290: 20}
modAmp = {5: 2, 10: 2, 20: 2, 30: 1.7, 50: 1.5, 80: 1.2, 110: 1, 140: 0.6, 170: 0.42, 200: 0.4, 230: 0.3, 260: 0.4, 290: 0.6}
sweepWidth = {5: 30, 10: 30, 20: 30, 30: 25, 50: 25, 80: 20, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}
nbScansExp = {5: 12, 10: 11, 20: 9, 30: 8, 50: 6, 80: 6, 110: 5, 140: 5, 170: 5, 200: 5, 230: 6, 260: 6, 290: 6}
nbScansPwrst = {5: 12, 10: 11, 20: 9, 30: 8, 50: 6, 80: 6, 110: 5, 140: 5, 170: 5, 200: 5, 230: 5, 260: 5, 290: 5}

# number of scans for different gate voltages
multiplierVg = {0: 2.5, -10: 2.5, -20: 2.5, -30: 2, -40: 2, -50: 1.5, -60: 1, -70: 1}

Vg = -60

folder = '/home/ss2151/Dropbox/ESR_data_upload/FI_ESR_pBTTT/IP/'
title = 'FI_ESR_pBTTT_1_6'

for T in [290, 260, 230, 200, 170, 140, 110, 80, 50, 30, 20, 10, 5]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()
    customXepr.getQValueCalc(folder, T)
    customXepr.customtune()

    # =========================================================================
    # Perform FET measurements
    # =========================================================================

    tString = str(int(T)).zfill(3)

    if T > 80:
        transferFile1 = folder + title + '_' + tString + 'K_transfer.txt'
        transferFile2 = folder + title + '_' + tString + 'K_transfer_trailing.txt'
        outputFile = folder + title + '_' + tString + 'K_output.txt'

        customXepr.transferMeasurement(transferFile1, VgStart=2, VgStop=-60)
        customXepr.transferMeasurement(transferFile2, VgStart=2, VgStop=-60, Vd=[-5,'trailing'])
        customXepr.outputMeasurement(outputFile)

    # =========================================================================
    # Perform ESR measurements at Vg and background scan at 0V
    # =========================================================================

#    for volt in [0, Vg]:
#        customXepr.biasGate(volt)
#        # allow time for charge injection at low T
#        if T <= 80:
#            customXepr.pause(3*60)
#
#        customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScansExp[T])
#        customXepr.biasGate(0)
#
#        esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(volt)
#        customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 20, 50, 80, 140, 200, 260, 290]:
        for volt in [0, Vg]:
            customXepr.customtune()

            customXepr.biasGate(volt)
            # allow time for charge injection at low T
            if T <= 80:
                customXepr.pause(3*60)
            customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=1.5*sweepWidth[T], NbScansToDo=nbScansPwrst[T])
            customXepr.biasGate(0)

            esrDataFile = folder + title + '_PowerSat_' + tString + 'K_Vg_' + str(volt)
            customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Gate voltage dependance
    # =========================================================================

    if T in [5, 50, 110, 170, 230, 290]:

        customXepr.customtune()

        for Vg in [-20, -30, -40, -50]:

            nscans = int(round(multiplierVg[Vg] * nbScansExp[T]))

            customXepr.biasGate(Vg)
            # allow time for charge injection at low T
            if T <= 80:
                customXepr.pause(3*60)

            customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=1.5*sweepWidth[T], NbScansToDo=nscans)
            customXepr.biasGate(0)

            esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(Vg)
            customXepr.saveCurrentData(esrDataFile)

customXepr.setTemperature(290)
