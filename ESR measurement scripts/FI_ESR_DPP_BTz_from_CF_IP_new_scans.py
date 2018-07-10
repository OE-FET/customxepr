Exp = xepr.XeprExperiment('Experiment')
Pwrst = xepr.XeprExperiment('PowerSat')
Pwrst2 = xepr.XeprExperiment('PowerSat2')

atten = {5: 45, 10: 40, 20: 35, 30: 33, 50: 32, 80: 30, 110: 30, 140: 25, 170: 23, 200: 15, 230: 14, 260: 12, 290: 10}
modAmp = {5: 2.3, 10: 1.8, 20: 1, 30: 0.8, 50: 0.6, 80: 0.35, 110: 0.3, 140: 0.32, 170: 0.42, 200: 0.65, 230: 0.80, 260: 1, 290: 1.2}
sweepWidth = {5: 25, 10: 23, 20: 20, 30: 18, 50: 15, 80: 15, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}
nbScans = {5: 8, 10: 8, 20: 8, 30: 8, 50: 6, 80: 6, 110: 6, 140: 8, 170: 10, 200: 10, 230: 12, 260: 12, 290: 12, 296: 12}

# number of scans for different gate voltages
multiplierVg = {0: 2, -10: 2, -20: 2, -30: 2, -40: 1.5, -50: 1, -60: 1, -70: 1}

folder = '/home/ss2151/Dropbox/ESR_data_upload/FI_ESR_DPP_BTz_fromCF/FET1_2_IP_2nd_run/'
title = 'FET1_2_IP'

# I am aleardy happy with the PowerSat data from 290K, 260K, 200K, 140K.
# 80K is a bit noisy, most likely also 50K, 20K and 5K.
# => double number of scans to planned, increase ModAmp if possible
# also scedule gate voltage dependence, now that we have the time!

for T in [5, 10, 20, 30, 50, 80, 110, 140, 170, 200, 230, 260, 290]:

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()
    customXepr.getQValueCalc(folder, T)

    # =========================================================================
    # Perform FET measurements
    # =========================================================================
    tString = str(int(T)).zfill(3)
    transferFile = folder + title + '_' + tString + 'K_transfer.txt'
    outputFile = folder + title + '_' + tString + 'K_output.txt'

    customXepr.transferMeasurement(transferFile, VgStart=10, VgStop=-60, VgStep=1, Vd=(-5, -60))
    customXepr.outputMeasurement(outputFile, VdStart=0, VdStop=-60, VdStep=1, Vg=(0,-20,-40,-60))

    # =========================================================================
    # Perform ESR measurements
    # =========================================================================
    
    for Vg in [-70, 0]:
        customXepr.biasGate(Vg)
        customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])
        customXepr.biasGate(0)
    
        esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
        customXepr.saveCurrentData(esrDataFile)

    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
#     if T in [140, 200, 260, 290]:
#    
#         for Vg in [-70, 0]:
#    
#             customXepr.customtune()
#    
#             customXepr.biasGate(Vg)
#             customXepr.runExperiment(Pwrst, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])
#             customXepr.biasGate(0)
#    
#             esrDataFile = folder + title + '_PowerSat_' + tString + 'K_Vg_' + str(abs(Vg))
#             customXepr.saveCurrentData(esrDataFile)
            
    # =========================================================================
    # Perform PowerSat measurements at certain steps
    # =========================================================================
    if T in [5, 80]:
        
        for Vg in [-70, 0]:

            customXepr.customtune()
    
            customXepr.biasGate(Vg)
            customXepr.runExperiment(Pwrst2, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])
            customXepr.biasGate(0)
    
            esrDataFile = folder + title + '_PowerSat_' + tString + 'K_Vg_' + str(abs(Vg))
            customXepr.saveCurrentData(esrDataFile)
# =============================================================================
# Gate voltage dependance
# =============================================================================

    if T in [50, 110, 230, 290]:

        customXepr.customtune()

        for Vg in [-20, -30, -40, -50, -60]:

            nscans = int(round(multiplierVg[Vg] * nbScans[T]))

            customXepr.biasGate(Vg)
            customXepr.runExperiment(Exp, ModAmp=modAmp[T], PowerAtten=atten[T], SweepWidth=sweepWidth[T], NbScansToDo=nscans)
            customXepr.biasGate(0)

            esrDataFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_Vg_' + str(abs(Vg))
            customXepr.saveCurrentData(esrDataFile)
