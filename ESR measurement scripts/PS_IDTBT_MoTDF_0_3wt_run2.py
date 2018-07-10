Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 45, 10: 35, 20: 30, 30: 30, 50: 30, 80: 25, 110: 25, 140: 25, 170: 22, 200: 20, 230: 22, 260: 25, 290: 25}
modAmp = {5: 1.8, 10: 1.5, 20: 1.5, 30: 1.3, 50: 1.2, 80: 1.1, 110: 1.1, 140: 1.1, 170: 1, 200: 1.2, 230: 1.2, 260: 1.2, 290: 1.5}
nbScans = {5: 10, 10: 10, 20: 12, 30: 12, 50: 12, 80: 12, 110: 12, 140: 12, 170: 12, 200: 14, 230: 15, 260: 18, 290: 20}


folder = '/home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_Mo(TFD-COCF)3_0_3wt_2nd_run/'
title = 'PS_IDTBT_MoTFD_0_3wt_run2'


for T in [170, 140, 110, 80, 50, 30, 20, 10, 5]:

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
