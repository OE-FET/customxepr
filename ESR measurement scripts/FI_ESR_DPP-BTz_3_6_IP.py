Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 47, 10: 40, 20: 37, 30: 35, 50: 35, 80: 32, 110: 30, 140: 25, 170: 23, 200: 23, 230: 20, 260: 15, 290: 15}
modAmp = {5: 0.5, 10: 0.5, 20: 0.45, 30: 0.4, 50: 0.3, 80: 0.3, 110: 0.3, 140: 0.35, 170: 0.47, 200: 0.6, 230: 0.7, 260: 0.9, 290: 1}
sweepWidth = {5: 42, 10: 35, 20: 35, 30: 35, 50: 28, 80: 28, 110: 28, 140: 28, 170: 28, 200: 28, 230: 28, 260: 35, 290: 35}
nbScans = {5: 5, 10: 4, 20: 4, 30: 3, 50: 2, 80: 2, 110: 2, 140: 2, 170: 2, 200: 3, 230: 3, 260: 4, 290: 4}

# number of scans for different gate voltages
multiplierVg = {0: 2, -10: 2, -20: 2, -30: 1.5, -40: 1.5, -50: 1, -60: 1, -70: 1}

folder = '/home/ss2151/xeprFiles/Data/ss2151/FI_ESR_DPP_BTz/FET3_5_IP/'
title = 'FET3_5_DPP_BTz_IP'

# gate voltage dependence at: 5, 50, 110, 170, 230, 290

for T in [290, 260, 230, 200, 170, 140, 110, 80, 50, 30, 20, 10, 5]:

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

        esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(Vg)
        customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Gate voltage dependance
    # =========================================================================

    if T in [290, 230, 170, 110, 50, 5]:

        customXepr.customtune()

        for Vg in [-20, -30, -40, -50, -60]:

            nscans = int(round(multiplierVg[Vg] * nbScans[T]))

            customXepr.biasGate(Vg)
            customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nscans)
            customXepr.biasGate(0)

            esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(Vg)
            customXepr.saveCurrentData(esrDataFile)



for T in [5, 10, 20, 30, 50, 80, 110, 140, 170, 200, 230, 260, 290]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()

    # =========================================================================
    # Perform ESR measurements (Vg = -70 and background)
    # =========================================================================
    customXepr.getQValue(T, folder)

    for Vg in [20]:

        customXepr.biasGate(Vg)
        customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])
        customXepr.biasGate(0)

        esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(Vg)
        customXepr.saveCurrentData(esrDataFile)

customXepr.setStandby()

