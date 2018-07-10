Exp = xepr.XeprExperiment('Experiment')

folder = '/home/ss2151/xeprFiles/Data/ss2151/SHE_samples/pBTTT_curr/'
title = 'pBTTT_device1'

T = 295

customXepr.customtune()
customXepr.customtune()

customXepr.getQValue(T, folder)


for T in [290, 260, 230, 200, 170, 140, 110, 80, 50, 30, 20, 10, 5]:
    # =========================================================================
    # Perform FET measurements
    # =========================================================================

    outputFile = folder + title + '_' + str(int(Vg)).zfill(3) + 'V_IV_curve.txt'

    customXepr.outputMeasurement(outputFile, VdStart=-Vg, VdStop=Vg, VdStep=Vg/50.0, Vg=(0, ))

    # =========================================================================
    # Perform ESR measurements
    # =========================================================================

    # set SMUA voltage

    customXepr.biasGate(Vg)

    customXepr.runExperiment(Exp, PowerAtten = 20)
    esrDataFile = folder + title + '_' + str(int(Vg)).zfill(3) + 'V'
    name = title + '_' + str(int(Vg)).zfill(3) + 'V'
    customXepr.saveCurrentData(esrDataFile, name)

    customXepr.biasGate(0)
