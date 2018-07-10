Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

folder = '/home/ss2151/xeprFiles/Data/mjc222/'
title = 'Cu_ii'

# gate voltage dependence at: 5, 50, 110, 170, 230, 290

for T in [12, 14, 16, 18, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 290]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.pause(2*60)
    customXepr.customtune()
    customXepr.customtune()

    # =========================================================================
    # Perform ESR measurements
    # =========================================================================
    customXepr.getQValue(T, folder)

    customXepr.runExperiment(Exp)

    esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K'
    customXepr.saveCurrentData(esrDataFile)

    customXepr.runExperiment(Pwrst)

    esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_PowerSat'
    customXepr.saveCurrentData(esrDataFile)
