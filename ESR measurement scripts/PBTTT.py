Pwrst = xepr.XeprExperiment('PowerSat')

folder = '/home/ss2151/Dropbox/ESR_data_upload/pBTTT_F4TCNQ_Oct_2017/Annealed4/'
title = 'pBTTT_F4TCNQ_Annealed4'


for T in [230, 200, 170, 110, 80, 50, 30, 20, 10, 5]: #

    # =========================================================================
    # Prepare temperature
    # =========================================================================

    customXepr.setTemperature(T)

    customXepr.customtune()
    customXepr.customtune()

    customXepr.getQValueCalc(folder, T)

    # =========================================================================
    # Perform PowerSat measurements at all steps
    # =========================================================================

    customXepr.runExperiment(Pwrst)
    esrDataFile = folder + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K'
    name = title + '_PowerSat_' + str(int(T)).zfill(3) + 'K'
    customXepr.saveCurrentData(esrDataFile, name)

customXepr.setStandby()
customXepr.setTemperature(294)
