Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

# number of scans for different gate voltages

folder = '/home/ss2151/Dropbox/ESR_data_upload/IDTBT_for_John/IDTBT_photoexcitation'
title = 'IDTBT_pre_PE'

for T in [110, 80, 50, 30, 20, 10, 5]:

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

    customXepr.runExperiment(Exp)

    esrDataFile = folder + '/' + title + '_' + str(int(T)).zfill(3) + 'K'
    customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Microwave power dependance
    # =========================================================================

    if T in [290, 260, 230, 200, 170, 140, 110, 80, 50, 30, 20, 10, 5]:

        customXepr.customtune()

        customXepr.runExperiment(Pwrst)
        esrDataFile = folder + '/' + title + '_' + str(int(T)).zfill(3) + 'K_PowerSat'
        customXepr.saveCurrentData(esrDataFile)


customXepr.setTemperature(290)
customXepr.setStandby()
