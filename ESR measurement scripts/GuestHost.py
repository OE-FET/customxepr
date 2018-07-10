Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')
nbScans = {5: 5, 50: 6, 100: 8, 150: 6, 200: 8, 250: 10, 290: 12}
modAmp = {5: 1, 50: 1, 100: 1, 150: 0.6, 200: 0.8, 250: 1, 290: 1}


folder = '/home/ss2151/Dropbox/ESR_data_upload/Guest_Host/Sample2_F4-TCNQ/'
title = 'Sample2_F4-TCNQ'
# gate voltage dependence at: 5, 50, 110, 170, 230, 290

for T in [250, 290]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()
    customXepr.getQValue(T, folder)

    # =========================================================================
    # Perform ESR measurements
    # =========================================================================

    customXepr.runExperiment(Pwrst, NbScansToDo=nbScans[T], ModAmp=modAmp[T])

    esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_PowerSat'
    customXepr.saveCurrentData(esrDataFile)

customXepr.setStandby()

