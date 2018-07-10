Exp = xepr.XeprExperiment('Experiment')

# measurement parameters for different temperatures
atten = {5: 50, 10: 40, 20: 36, 30: 35, 50: 30, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 15, 290: 15}
modAmp = {5: 1.5, 10: 1.3, 20: 1, 30: 0.8, 50: 0.5, 80: 0.4, 110: 0.3, 140: 0.2, 170: 0.3, 200: 0.4, 230: 0.7, 260: 0.9, 290: 1}
sweepWidth = {5: 23, 10: 20, 20: 20, 30: 18, 50: 15, 80: 15, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}

# number of scans for different gate voltages
nbScans = {0: 32, -40: 32, -50: 25, -60: 21, -70: 18, -80: 17, -90: 16, -100: 16}

folder = '/home/ss2151/xeprFiles/Data/ss2151/FI_ESR_Data/FI_ESR_3_2_5K_gate_voltage/'
title = 'FI_ESR_device4'

T = 5

#customXepr.setTemperature(80)
#
#customXepr.customtune()
#customXepr.customtune()
#
#customXepr.setTempRamp(2)
#customXepr.setTemperature(40)
#
#customXepr.customtune()

#==============================================================================
# Perform ESR measurements
#==============================================================================

for Vg in [-90, -80, -70, -60, -50, -40, 0]:

#    customXepr.setTempRamp(0.5)
#    customXepr.setTemperature(40)
#    customXepr.biasGate(Vg)

    customXepr.biasGate(Vg)
    customXepr.setTemperature(T)

    customXepr.customtune()
    customXepr.customtune()

    customXepr.getQValue(T, folder)

    customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[Vg])
    
    fileName = title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
    filePath = folder + fileName
    customXepr.saveCurrentData(filePath, fileName)


customXepr.setTemperature(40)
customXepr.setTempRamp(2)
customXepr.setTemperature(80)
customXepr.setTempRamp(4)
customXepr.setTemperature(290)
