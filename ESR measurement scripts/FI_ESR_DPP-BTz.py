Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 50, 10: 40, 20: 36, 30: 35, 50: 30, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 15, 290: 15}
modAmp = {5: 1.5, 10: 1.3, 20: 1, 30: 1, 50: 1, 80: 0.9, 110: 0.7, 140: 0.5, 170: 0.7, 200: 0.7, 230: 0.7, 260: 0.9, 290: 1}
sweepWidth = {5: 23, 10: 20, 20: 20, 30: 18, 50: 15, 80: 15, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}
nbScans = {5: 16, 10: 16, 20: 16, 30: 16, 50: 12, 80: 12, 110: 12, 140: 12, 170: 12, 200: 14, 230: 16, 260: 18, 290: 20}

folder = '/home/ss2151/xeprFiles/Data/ss2151/FI_ESR_DPP_BTz/FET3_8/'
title = 'FET3_8_DPP_BTz'

# gate voltage dependence at: 5, 50, 110, 170, 230, 290

for T in [110, 80, 50]:

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
    # Perform FET measurements
    # =========================================================================
    transferFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_transfer.txt'
    outputFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_output.txt'

    customXepr.transferMeasurement(transferFile, VgStart=10, VgStop=-70, VgStep=1, Vd=(-5, -70))
    customXepr.outputMeasurement(outputFile)

    # =========================================================================
    # Perform ESR measurements (gate voltage and background)
    # =========================================================================
    customXepr.getQValue(T, folder)

    for Vg in [-70, 0]:

        customXepr.biasGate(Vg)
        customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])
        customXepr.biasGate(0)

        esrDataFile = folder + '/' + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 50, 110, 140, 200, 260, 290]:

        for Vg in [-70, 0]:

            customXepr.customtune()

            customXepr.biasGate(Vg)
            customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T])
            customXepr.biasGate(0)

            esrDataFile = folder + '/' + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
            customXepr.saveCurrentData(esrDataFile)

Vg = -70
customXepr.biasGate(Vg)

for T in [30, 20, 10, 5]:

    if T < 70:
        customXepr.setTempRamp(0.5)
    elif T < 110:
        customXepr.setTempRamp(1)
    else:
        customXepr.setTempRamp(2)

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

    esrDataFile = folder + '/' + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
    customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 50, 110, 140, 200, 260, 290]:

        customXepr.customtune()

        customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T])

        esrDataFile = folder + '/' + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        customXepr.saveCurrentData(esrDataFile)

Vg = 0
customXepr.biasGate(Vg)

for T in [5, 10, 20, 30]:

    if T < 70:
        customXepr.setTempRamp(0.5)
    elif T < 110:
        customXepr.setTempRamp(1)
    else:
        customXepr.setTempRamp(2)

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

    esrDataFile = folder + '/' + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
    customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 50, 110, 140, 200, 260, 290]:

        customXepr.customtune()

        customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T])

        esrDataFile = folder + '/' + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        customXepr.saveCurrentData(esrDataFile)

customXepr.setStandby()
customXepr.setTemperature(290)
