Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {30: 50, 50: 45, 70: 45, 90: 45, 120: 45, 150: 40, 170: 35, 200: 35, 230: 30, 260: 30, 290: 30}

folder = '/home/ss2151/xeprFiles/Data/ss2151/Solution_ESR_Data/IDTBT/'
title = 'IDTBT_AlCl3_new'

for T in [260, 230, 200, 170, 150, 120, 90, 70, 50, 30]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()

    # =========================================================================
    # Perform ESR measurements
    # =========================================================================
    customXepr.getQValue(T, folder)

    customXepr.runExperiment(Exp, PowerAtten=atten[T])

    esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K'
    name = title + '_' + str(int(T)).zfill(3) + 'K'
    customXepr.saveCurrentData(esrDataFile, name)

    # =========================================================================
    # Perform PowerSat measurements
    # =========================================================================

    customXepr.customtune()

    customXepr.runExperiment(Pwrst, PowerAtten=atten[T])

    esrDataFile = folder + title + '_PowerSat_' + str(int(T)).zfill(3) + 'K'
    name = title + '_PowerSat_' + str(int(T)).zfill(3) + 'K'

    customXepr.saveCurrentData(esrDataFile, name)
