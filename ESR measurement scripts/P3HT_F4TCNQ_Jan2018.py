Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 50, 10: 48, 20: 46, 30: 44, 50: 42, 80: 40, 110: 38, 140: 36, 170: 34, 200: 32, 230: 30, 260: 28, 290: 25}

# number of scans for different gate voltages

folder = '/home/ss2151/Dropbox/ESR_data_upload/P3HT_F4TCNQ_Jan_2018/Stage0_Dedoping'
title = 'P3HT_F4TCNQ_Jan_2018'

for T in [290, 260, 230, 200, 170, 140, 110, 80, 50, 30, 20, 10, 5]:

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
    if T > 150:
        modAmp = 1
    else:
        modAmp = 0.5
        
    customXepr.runExperiment(Exp, PowerAtten=atten[T], ModAmp=modAmp)

    esrDataFile = folder + '/' + title + '_' + str(int(T)).zfill(3) + 'K'
    customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Microwave power dependance
    # =========================================================================

    if T in [290, 260, 230, 200, 170, 140, 110, 80, 50, 30, 20, 10, 5]:

        customXepr.customtune()

        customXepr.runExperiment(Pwrst, ModAmp=modAmp)
        esrDataFile = folder + '/' + title + '_' + str(int(T)).zfill(3) + 'K_PowerSat'
        customXepr.saveCurrentData(esrDataFile)


customXepr.setTemperature(290)
customXepr.setStandby()
