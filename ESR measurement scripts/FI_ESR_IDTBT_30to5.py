Exp = Xepr.XeprExperiment('Experiment')
Pwrst2 = Xepr.XeprExperiment('PowerSat2')

atten = {5: 50, 10: 40, 20: 36, 30: 35, 50: 30, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 15, 290: 15}
modAmp = {5: 1.5, 10: 1.3, 20: 1, 30: 0.8, 50: 0.5, 80: 0.4, 110: 0.3, 140: 0.2, 170: 0.3, 200: 0.4, 230: 0.7, 260: 1.3, 290: 1.5}
sweepWidth = {5: 23, 10: 20, 20: 20, 30: 18, 50: 15, 80: 15, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}
nbScans = {5: 18, 10: 16, 20: 16, 30: 16, 50: 12, 80: 12, 110: 12, 140: 12, 170: 12, 200: 14, 230: 16, 260: 18, 290: 20}

CustomXepr.setTemperature(100)

CustomXepr.setTempRamp(3)

CustomXepr.setTemperature(40)

Vg = -70
CustomXepr.biasGate(Vg)

folder = '/home/ss2151/xeprFiles/Data/ss2151/FI_ESR_Data/FI_ESR_3_2/'
title = 'FI_ESR_device4'

CustomXepr.setTempRamp(0.5)


for T in [20, 10, 5]:

#==============================================================================
# Prepare temperature
#==============================================================================
    CustomXepr.setTemperature(T)
    CustomXepr.customtune()
    CustomXepr.customtune()

#==============================================================================
# Perform ESR measurements
#==============================================================================

    if T is not 20:
        CustomXepr.getQValue(T, folder)

        CustomXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])

        esrDataFile = title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        CustomXepr.saveCurrentData(folder, esrDataFile)

#==============================================================================
# Perform PowerSat measurements at certain steps
#==============================================================================
    if T in [5, 20]:

        CustomXepr.customtune()

        CustomXepr.runExperiment(Pwrst2, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T])

        esrDataFile = title + '_PowerSat_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        CustomXepr.saveCurrentData(folder, esrDataFile)

CustomXepr.biasGate(0)