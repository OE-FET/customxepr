Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 50, 10: 40, 20: 36, 30: 35, 50: 30, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 15, 290: 15}
modAmp = {5: 1.5, 10: 1.3, 20: 1, 30: 0.8, 50: 0.5, 80: 0.4, 110: 0.3, 140: 0.2, 170: 0.3, 200: 0.4, 230: 0.7, 260: 0.9, 290: 1}
sweepWidth = {5: 23, 10: 20, 20: 20, 30: 18, 50: 15, 80: 15, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}
nbScans = {5: 8, 10: 8, 20: 8, 30: 8, 50: 6, 80: 6, 110: 6, 140: 6, 170: 6, 200: 7, 230: 8, 260: 9, 290: 10}


folder = '/home/ss2151/Dropbox/ESR_data_upload/PS_IDTBT/PS_IDTBT_5wt/'
title = 'PS_IDTBT_5wt'


for T in [290, 260, 230, 200, 170, 140, 110, 80, 50, 30, 20, 10, 5]:

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

    esrDataFile = folder + '/' + title + '_' + tString + 'K'
    customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 20, 50, 80, 140, 200, 260, 290]:

        customXepr.customtune()

        customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T])

        esrDataFile = folder + title + '_PowerSat_' + tString + 'K'
        customXepr.saveCurrentData(esrDataFile)
