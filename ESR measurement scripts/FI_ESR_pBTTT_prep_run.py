Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 50, 10: 40, 20: 36, 30: 35, 50: 30, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 15, 290: 15}
modAmp = {5: 2.3, 10: 1.8, 20: 1, 30: 0.8, 50: 0.6, 80: 0.35, 110: 0.3, 140: 0.32, 170: 0.42, 200: 0.65, 230: 0.80, 260: 1, 290: 1.2}
sweepWidth = {5: 25, 10: 23, 20: 20, 30: 18, 50: 15, 80: 15, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}
nbScans = {5: 8, 10: 8, 20: 8, 30: 8, 50: 6, 80: 6, 110: 6, 140: 8, 170: 10, 200: 10, 230: 12, 260: 12, 290: 12}

# number of scans for different gate voltages
multiplierVg = {0: 2.5, -10: 2.5, -20: 2.5, -30: 2, -40: 2, -50: 1.5, -60: 1, -70: 1}

Vg = -60

folder = '/home/ss2151/Dropbox/ESR_data_upload/FI_ESR_pBTTT/'
title = 'FI_ESR_pBTTT_1_1'

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
    if T > 20:
        tString = str(int(T)).zfill(3)
        transferFile1 = folder + title + '_' + tString + 'K_transfer.txt'
        transferFile2 = folder + title + '_' + tString + 'K_transfer_trailing.txt'
        outputFile = folder + title + '_' + tString + 'K_output.txt'

        customXepr.transferMeasurement(transferFile1, VgStart=3, VgStop=-60)
        customXepr.transferMeasurement(transferFile2, VgStart=3, VgStop=-60, Vd=[-5,'trailing'])
        customXepr.outputMeasurement(outputFile)

    # =========================================================================
    # Perform ESR measurements at Vg and background scan at 0V
    # =========================================================================

    for volt in [0, Vg]:
        customXepr.biasGate(volt)
        customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])
        customXepr.biasGate(0)

        esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(volt)
        customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================  
    if T in [5, 20, 50, 80, 140, 200, 260]:
        for volt in [0, Vg]:  
            customXepr.customtune()
    
            customXepr.biasGate(volt)
            customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T])
            customXepr.biasGate(0)
    
            esrDataFile = folder + title + '_PowerSat_' + tString + 'K_Vg_' + str(volt)
            customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Gate voltage dependance
    # =========================================================================

#    if T in [5, 50, 110, 170, 230, 290]:
#
#        customXepr.customtune()
#
#        for Vg in [-20, -30, -40, -50, -60]:
#
#            nscans = int(round(multiplierVg[Vg] * nbScans[T]))
#
#            customXepr.biasGate(Vg)
#            customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nscans)
#            customXepr.biasGate(0)
#
#            esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
#            customXepr.saveCurrentData(esrDataFile)
