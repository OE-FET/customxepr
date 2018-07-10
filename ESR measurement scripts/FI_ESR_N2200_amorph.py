Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 45, 10: 43, 20: 40, 30: 40, 50: 37, 80: 35, 110: 30, 140: 30, 170: 30, 200: 25, 230: 25, 260: 25, 290: 25}
modAmp = {5: 2.2, 10: 1.9, 20: 1.6, 30: 1.3, 50: 1, 80: 0.6, 110: 0.5, 140: 0.3, 170: 0.2, 200: 0.2, 230: 0.3, 260: 0.4, 290: 0.45}
nbScans = {5: 3, 10: 2, 20: 2, 30: 2, 50: 2, 80: 2, 110: 2, 140: 2, 170: 1, 200: 2, 230: 2, 260: 2, 290: 2, 296: 2}
sweepWidth = {5: 35, 10: 30, 20: 25, 30: 20, 50: 20, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 20, 290: 20}

# number of scans for different gate voltages
multiplierVg = {0: 3, 10: 3, 20: 3, 30: 2, 40: 2, 50: 2, 60: 1.5, 70: 1, 80: 1, 90: 1, 100: 1}

folder = '/home/ss2151/Dropbox/ESR_data_upload/FI_ESR_N2200/Device2_2/'
title = 'FET2_2'

for T in [290, 260, 230, 200, 170, 140, 110, 80, 50, 30, 20, 10, 5]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()
    customXepr.getQValueCalc(folder, T)

    # =========================================================================
    # Perform FET measurements
    # =========================================================================
    if T > 50:
        transferFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_transfer.txt'
        outputFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_output.txt'

        customXepr.transferMeasurement(transferFile, VgStart=-10,VgStop=70, VgStep=1, Vd=(5, 70))
        customXepr.outputMeasurement(outputFile, VdStart=0, VdStop=60, VdStep=1, Vg=(0,20,40,60))

    # =========================================================================
    # Perform ESR measurements
    # =========================================================================

#    for Vg in [70, 0]:
#        customXepr.biasGate(Vg)
#        customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], NbScansToDo=nbScans[T], SweepWidth=sweepWidth[T])
#        customXepr.biasGate(0)
#
#        esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
#        customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
#    if T in [5, 20, 50, 80, 140, 200, 260, 290]:
#
#        for Vg in [70, 0]:
#            customXepr.customtune()
#
#            customXepr.biasGate(Vg)
#            customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], NbScansToDo=nbScans[T], SweepWidth=sweepWidth[T])
#            customXepr.biasGate(0)
#
#            esrDataFile = folder + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
#            customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Gate voltage dependance
    # =========================================================================

    if T in [5, 50, 110, 170, 230, 290]:

        customXepr.customtune()

        for Vg in [0, 10, 20, 30, 40, 50, 60, 70]:

            nscans = int(round(multiplierVg[Vg] * nbScans[T]))

            customXepr.biasGate(Vg)
            customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], NbScansToDo=nscans, SweepWidth=sweepWidth[T])

            esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
            customXepr.saveCurrentData(esrDataFile)

        customXepr.biasGate(0)
