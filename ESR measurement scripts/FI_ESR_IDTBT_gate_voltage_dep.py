Exp = Xepr.XeprExperiment('Experiment')
Pwrst = Xepr.XeprExperiment('PowerSat')
# measurement parameters for different temperatures
atten = {5: 50, 10: 40, 20: 36, 30: 35, 50: 30, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 15, 290: 15}
modAmp = {5: 1.5, 10: 1.3, 20: 1, 30: 0.8, 50: 0.5, 80: 0.4, 110: 0.3, 140: 0.2, 170: 0.3, 200: 0.4, 230: 0.7, 260: 0.9, 290: 1}
sweepWidth = {5: 23, 10: 20, 20: 20, 30: 18, 50: 15, 80: 15, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}

# number of scans for different gate voltages
nbScans = {0: 32, -40: 32, -50: 25, -60: 21, -70: 18, -80: 16, -90: 14, -100: 13}

folder = '/home/ss2151/xeprFiles/Data/ss2151/FI_ESR_Data/FI_ESR_3_2_5K_gate_voltage/'
title = 'FI_ESR_device4'

# create dictionary for output and transfer data
outputData = {}
transferData = {}

for T in [5]:

#==============================================================================
# Perform ESR measurements
#==============================================================================

    for Vg in range(-10,-50,-10):
        CustomXepr.biasGate(keithley, Vg)
        CustomXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[Vg])

        esrDataFile = title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        CustomXepr.saveCurrentData(folder, esrDataFile)
        
        time.sleep(0.1)

    CustomXepr.biasGate(keithley, 0)


for T in [80, 110]:

#==============================================================================
# Prepare temperature
#==============================================================================
    CustomXepr.setTemperature(feed, T)
    CustomXepr.customtune()
    CustomXepr.customtune()
    CustomXepr.getQValue(T, folder)

#==============================================================================
# Perform FET measurements
#==============================================================================

    transferFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_transfer_Vg100_pulsed.txt'
    outputFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_output_Vg100_pulsed.txt'

    transferData[T] = CustomXepr.transferMeasurement(keithley, transferFile, VgStart=10, VgStop=-100, VgStep=1, Vd=(-10, -100), pulsed=True)
    outputData[T] = CustomXepr.outputMeasurement(keithley, outputFile, VdStart=0, VdStop=-100, VdStep=1, Vg=(0, -20, -40, -60, -80, -100), pulsed=True)

#==============================================================================
# Perform ESR measurements
#==============================================================================

    for Vg in range(0,-110,-10):
        CustomXepr.biasGate(keithley, Vg)
        CustomXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[Vg])

        esrDataFile = title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        CustomXepr.saveCurrentData(folder, esrDataFile)
        
        time.sleep(0.1)

    CustomXepr.biasGate(keithley, 0)
