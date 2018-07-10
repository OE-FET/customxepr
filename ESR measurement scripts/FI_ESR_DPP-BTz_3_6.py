Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 47, 10: 40, 20: 37, 30: 35, 50: 35, 80: 32, 110: 30, 140: 25, 170: 23, 200: 23, 230: 20, 260: 15, 290: 15}
modAmp = {5: 0.5, 10: 0.5, 20: 0.45, 30: 0.4, 50: 0.3, 80: 0.3, 110: 0.3, 140: 0.35, 170: 0.47, 200: 0.6, 230: 0.7, 260: 0.9, 290: 1}
sweepWidth = {5: 23, 10: 20, 20: 20, 30: 18, 50: 15, 80: 15, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}
nbScans = {5: 16, 10: 14, 20: 14, 30: 12, 50: 10, 80: 7, 110: 8, 140: 9, 170: 12, 200: 14, 230: 16, 260: 18, 290: 20}

# number of scans for different gate voltages
multiplierVg = {0: 2.5, -10: 2.5, -20: 2.5, -30: 2, -40: 2, -50: 1.5, -60: 1, -70: 1}

folder = '/home/ss2151/xeprFiles/Data/ss2151/FI_ESR_DPP_BTz/FET3_6/'
title = 'FET3_6_DPP_BTz'

# gate voltage dependence at: 5, 50, 110, 170, 230, 290

for T in [80, 50, 30]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()

    # =========================================================================
    # Perform FET measurements
    # =========================================================================
    transferFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_transfer.txt'
    outputFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_output.txt'

    customXepr.transferMeasurement(transferFile)
    customXepr.outputMeasurement(outputFile)

    # =========================================================================
    # Perform ESR measurements (Vg = -70 and background)
    # =========================================================================
    customXepr.getQValue(T, folder)

    for Vg in [-70, 0]:

        customXepr.biasGate(Vg)
        customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])
        customXepr.biasGate(0)

        esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Gate voltage dependance
    # =========================================================================

    if T in [5, 50, 110, 170, 230, 290]:

        customXepr.customtune()

        for Vg in [-20, -30, -40, -50, -60]:

            nscans = int(round(multiplierVg[Vg] * nbScans[T]))

            customXepr.biasGate(Vg)
            customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nscans)
            customXepr.biasGate(0)

            esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
            customXepr.saveCurrentData(esrDataFile)

Vg = -70
customXepr.biasGate(Vg)

for T in [5]:

    if T < 70:
        customXepr.setTempRamp(0.4)
    elif T < 110:
        customXepr.setTempRamp(0.7)
    elif T < 200:
        customXepr.setTempRamp(1)
    else:
        customXepr.setTempRamp(1.5)

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()

    # =========================================================================
    # Perform ESR measurements (gate voltage and background)
    # =========================================================================
    customXepr.getQValue(T, folder)

    customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])

    esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
    customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurement
    # =========================================================================

    customXepr.customtune()

    customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T])

    esrDataFile = folder + '/' + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
    customXepr.saveCurrentData(esrDataFile)

T = 5

for Vg in [-60, -50, -40, -30, 0]:

    customXepr.biasGate(Vg)

    customXepr.setTemperature(T)

    customXepr.customtune()

    customXepr.getQValue(T, folder)

    nscans = int(round(multiplierVg[Vg] * nbScans[5]))
    customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nscans)

    esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
    customXepr.saveCurrentData(esrDataFile)

Vg = 0
T = 5

customXepr.biasGate(Vg)

customXepr.customtune()

customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T])

esrDataFile = folder + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_real_' + str(abs(Vg))
customXepr.saveCurrentData(esrDataFile)


customXepr.setStandby()
customXepr.setTemperature(290)
