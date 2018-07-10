Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')
Pwrst2 = xepr.XeprExperiment('PowerSat2')

atten = {5: 45, 10: 43, 20: 40, 30: 40, 50: 37, 80: 30, 110: 25, 140: 20, 170: 17, 200: 15, 230: 15, 260: 10, 290: 5}
modAmp = {5: 2, 10: 1.5, 20: 1.2, 30: 1, 50: 0.8, 80: 0.5, 110: 0.6, 140: 0.8, 170: 1.2, 200: 2.5, 230: 3, 260: 3.5, 290: 4}
nbScans = {5: 5, 10: 4, 20: 4, 30: 3, 50: 3, 80: 3, 110: 3, 140: 2, 170: 2, 200: 2, 230: 3, 260: 5, 290: 5}
sweepWidth = {5: 40, 10: 40, 20: 40, 30: 40, 50: 44, 80: 48, 110: 48, 140: 48, 170: 48, 200: 48, 230: 48, 260: 48, 290: 48}

# number of scans for different gate voltages
multiplierVg = {0: 2.5, 10: 2.5, 20: 2, 30: 2, 40: 1.5, 50: 1.5, 60: 1, 70: 1}

folder = '/home/ss2151/Dropbox/ESR_data_upload/FI_ESR_N2200/Device1_4_2nd/'
title = 'FET1_4'


for T in [30, 20, 10, 5]: # 290, 260, 230, 200, 170, 140, 80, 50,

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
    if T >= 50:
        transferFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_transfer.txt'
        outputFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_output.txt'

        customXepr.transferMeasurement(transferFile, VgStart=-10,VgStop=60, VgStep=1, Vd=(5, 60))
        customXepr.outputMeasurement(outputFile, VdStart=0, VdStop=60, VdStep=1, Vg=(0, 20, 40, 60))

    # =========================================================================
    # Perform ESR measurements
    # =========================================================================

    for Vg in [70, 0]:

        nscans = int(round(multiplierVg[Vg] * nbScans[T]))

        customXepr.biasGate(Vg)
        customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], NbScansToDo=nscans, SweepWidth=sweepWidth[T])
        customXepr.biasGate(0)

        esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg)).zfill(2)
        customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 20, 50, 80, 140, 200, 260, 290]:

        for Vg in [70, 0]:
            customXepr.customtune()

            customXepr.biasGate(Vg)
            if T > 110:
                customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], NbScansToDo=nbScans[T], SweepWidth=sweepWidth[T])
            elif T < 110:
                customXepr.runExperiment(Pwrst2, ModAmp=modAmp[T], NbScansToDo=nbScans[T], SweepWidth=sweepWidth[T])
            customXepr.biasGate(0)

            esrDataFile = folder + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg)).zfill(2)
            customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Gate voltage dependance
    # =========================================================================

    if T in [5, 50, 110, 170, 230, 290]:

        customXepr.customtune()

        for Vg in [10, 20, 30, 40, 50, 60]:

            nscans = int(round(multiplierVg[Vg] * nbScans[T]))

            customXepr.biasGate(Vg)
            customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], NbScansToDo=nscans, SweepWidth=sweepWidth[T])

            esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg)).zfill(2)
            customXepr.saveCurrentData(esrDataFile)

        customXepr.biasGate(0)

customXepr.setTemperature(290)
