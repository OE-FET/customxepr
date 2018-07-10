Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 50, 10: 40, 20: 36, 30: 35, 50: 30, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 15, 290: 15}
modAmp = {5: 1.8, 10: 1.5, 20: 1.5, 30: 1.3, 50: 1.2, 80: 1.1, 110: 1, 140: 1, 170: 1, 200: 1, 230: 1, 260: 1, 290: 1}
nbScans = {5: 8, 10: 8, 20: 8, 30: 8, 50: 6, 80: 6, 110: 6, 140: 6, 170: 6, 200: 7, 230: 8, 260: 9, 290: 10}

folder = '/home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG/'
title = 'PS_IDTBT_Mo(TFD-COCF)3_0_3wt_BG'

for T in [20, 30, 50, 80, 110, 140, 170, 200, 230, 260, 290]:

    tString = str(int(T)).zfill(3)

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()
    customXepr.getQValueCalc(folder, T)

    # =========================================================================
    # Perform ESR measurements at Vg and background scan at 0V
    # =========================================================================

    customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], NbScansToDo=nbScans[T])

    esrDataFile = folder + title + '_' + tString + 'K'
    customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 20, 50, 80, 140, 200, 260, 290]:

        customXepr.customtune()

        customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T])

        esrDataFile = folder + title + '_PowerSat_' + tString + 'K'
        customXepr.saveCurrentData(esrDataFile)
