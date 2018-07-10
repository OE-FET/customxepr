# gate voltage dependence at: 5, 50, 110, 170, 230, 290

for T in [290, 260, 230, 200]:

    if T < 70:
        customXepr.setTempRamp(0.4)
    elif T < 110:
        customXepr.setTempRamp(0.7)
    elif T < 200:
        customXepr.setTempRamp(1)
    else:
        customXepr.setTempRamp(1.5)

    customXepr.setTemperature(T)
    customXepr.customtune()
    customXepr.customtune()

    # =========================================================================
    # Perform FET measurements
    # =========================================================================
    transferFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_transfer.txt'
    outputFile = folder + title + '_' + str(int(T)).zfill(3) + 'K_output.txt'

    customXepr.transferMeasurement(transferFile, VgStart=10, VgStop=-70, VgStep=1, Vd=(-5, -70))
    customXepr.outputMeasurement(outputFile)
