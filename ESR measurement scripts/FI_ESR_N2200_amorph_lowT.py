Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 47, 10: 40, 20: 37, 30: 35, 50: 35, 80: 32, 110: 30, 140: 20, 170: 18, 200: 15, 230: 15, 260: 12, 290: 10, 296: 10}
modAmp = {5: 2.2, 10: 1.9, 20: 1.6, 30: 1.3, 50: 1, 80: 0.6, 110: 0.5, 140: 0.3, 170: 0.2, 200: 0.2, 230: 0.3, 260: 0.4, 290: 0.45, 296: 1}
nbScans = {5: 3, 10: 2, 20: 2, 30: 2, 50: 2, 80: 2, 110: 2, 140: 2, 170: 1, 200: 2, 230: 2, 260: 1, 290: 2, 296: 2}
sweepWidth = {5: 35, 10: 30, 20: 25, 30: 20, 50: 20, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 20, 290: 20}

# number of scans for different gate voltages
multiplierVg = {0: 2, 10: 2, 20: 2, 30: 1.5, 40: 1.5, 50: 1, 60: 1, 70: 1, 80: 1, 90: 1, 100: 1}

folder = '/home/ss2151/Dropbox/ESR_data_upload/FI_ESR_N2200/Device2_7/'
title = 'FET2_7'

customXepr.setTemperature(80)
customXepr.customtune()
customXepr.customtune()
customXepr.getQValueCalc(folder, 80)

Vg = 70
customXepr.biasGate(Vg)

for T in [5]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()
    customXepr.getQValueCalc(folder, T)

    # =========================================================================
    # Perform ESR measurements
    # =========================================================================
    customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], NbScansToDo=nbScans[T], SweepWidth=sweepWidth[T])

    esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
    customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 20, 50, 80, 140, 200, 260, 290, 296]:

        customXepr.customtune()

        customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], SweepWidth=sweepWidth[T])

        esrDataFile = folder + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        customXepr.saveCurrentData(esrDataFile)

Vg = 0
customXepr.biasGate(Vg)

for T in [5, 10, 20, 30, 50]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()

    # =========================================================================
    # Perform ESR measurements
    # =========================================================================

    customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], NbScansToDo=nbScans[T], SweepWidth=sweepWidth[T])

    esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
    customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 20, 50, 80, 140, 200, 260, 290, 296]:

        customXepr.customtune()

        customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], SweepWidth=sweepWidth[T])

        esrDataFile = folder + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        customXepr.saveCurrentData(esrDataFile)
