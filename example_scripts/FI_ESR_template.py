from customxepr import run
customxepr, xepr, _ = run()


def sign(x):
    return (1, -1)[x < 0]


exp = xepr.XeprExperiment('Experiment')
pwrst = xepr.XeprExperiment('PowerSat')

atten = {5: 50, 10: 40, 20: 36, 30: 35, 50: 30, 80: 20, 110: 20, 140: 20, 170: 20, 200: 20, 230: 20, 260: 15, 290: 15}
modAmp = {5: 1.5, 10: 1.3, 20: 1, 30: 0.8, 50: 0.5, 80: 0.4, 110: 0.3, 140: 0.2, 170: 0.3, 200: 0.4, 230: 0.7, 260: 0.9, 290: 1}
sweepWidth = {5: 23, 10: 20, 20: 20, 30: 18, 50: 15, 80: 15, 110: 15, 140: 15, 170: 15, 200: 15, 230: 15, 260: 18, 290: 20}
nbScans = {5: 16, 10: 16, 20: 16, 30: 16, 50: 12, 80: 12, 110: 12, 140: 12, 170: 12, 200: 14, 230: 16, 260: 18, 290: 20}

# number of scans for different gate voltages
multiplierVg = {0: 2.5, -10: 2.5, -20: 2.5, -30: 2, -40: 2, -50: 1.5, -60: 1, -70: 1}

Vg = -70

directory = '/home/ss2151/Dropbox/ESR_data_upload/my_sample'
filename = 'my_sample'

for T in [290, 260, 230, 200, 170, 140, 110, 80, 50, 30, 20, 10, 5]:

    # ====================================================================================
    # Prepare temperature
    # ====================================================================================
    customxepr.setTemperature(T)
    customxepr.sendEmail('Temperature stable at %sK.' % T)
    customxepr.customtune()
    customxepr.customtune()
    customxepr.getQValueCalc(directory, T)

    # ====================================================================================
    # Perform FET measurements
    # ====================================================================================
    path1 = "{0}/{1}_{2:03d}K_transfer.txt".format(directory, filename, T)
    path2 = "{0}/{1}_{2:03d}K_output.txt".format(directory, filename, T)

    customxepr.transferMeasurement(path=path1)
    customxepr.outputMeasurement(path=path2)

    # ====================================================================================
    # Perform ESR measurements at Vg and background scan at 0V
    # ====================================================================================

    for v in [0, Vg]:
        path3 = "{0}/{1}_{2:03d}K_Vg_{3:03d}".format(directory, filename, T, v)

        customxepr.setGateVoltage(v)
        customxepr.runXeprExperiment(exp, path=path3,
                                    ModAmp=modAmp[T], PowerAtten=atten[T],
                                    SweepWidth=sweepWidth[T], NbScansToDo=nbScans[T])
        customxepr.setGateVoltage(0)

    # ====================================================================================
    # Perform PowerSat measurements at certain steps
    # ====================================================================================
    if T in [5, 20, 50, 80, 140, 200, 260]:

        customxepr.customtune()

        path4 = "{0}/{1}_PowerSat_{2:03d}K_Vg_{3:03d}".format(directory, filename, T, Vg)

        customxepr.setGateVoltage(Vg)
        customxepr.runXeprExperiment(pwrst, path=path4,
                                     ModAmp=modAmp[T], PowerAtten=atten[T],
                                     SweepWidth=sweepWidth[T])
        customxepr.setGateVoltage(0)

    # ====================================================================================
    # Gate voltage dependence
    # ====================================================================================

    if T in [5, 50, 110, 170, 230, 290]:

        customxepr.customtune()

        for v in [-10, -20, -30, -40, -50, -60]:

            nscans = int(round(multiplierVg[v] * nbScans[T]))
            path5 = "{0}/{1}_{2:03d}K_Vg_{3:03d}".format(directory, filename, T, v)

            customxepr.setGateVoltage(v)
            customxepr.runXeprExperiment(
                    exp, path=path5,
                    ModAmp=modAmp[T], PowerAtten=atten[T],
                    SweepWidth=sweepWidth[T], NbScansToDo=nscans)
            customxepr.setGateVoltage(0)

    customxepr.sendEmail('Measurements at %sK completed.' % T)
