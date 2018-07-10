folder = '/home/ss2151/xeprFiles/Data/ss2151/WireBond_test/'
title = 'WireBond_test'

# gate voltage dependence at: 5, 50, 110, 170, 230, 290

for T in [100, 50, 5]:

    if T < 70:
        customXepr.setTempRamp(1)
    elif T < 110:
        customXepr.setTempRamp(2)
    elif T < 200:
        customXepr.setTempRamp(3)
    else:
        customXepr.setTempRamp(4)

    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune_lossy()
    customXepr.customtune_lossy()
    
    customXepr.getQValue(T, folder)

    # =========================================================================
    # Perform FET measurements
    # =========================================================================
    
    fileName = folder + title + '_' + str(int(T)).zfill(3) + 'K_IVcurve.txt' 

    customXepr.outputMeasurement(fileName, VdStart=-2, VdStop=2, VdStep=0.1, Vg=(0,))
    
for T in [50, 100, 150, 200, 290]:


    # =========================================================================
    # Prepare temperature
    # =========================================================================
    customXepr.setTemperature(T)
    customXepr.customtune_lossy()
    customXepr.customtune_lossy()
    
    customXepr.getQValue(T, folder)

    # =========================================================================
    # Perform FET measurements
    # =========================================================================
    
    fileName = folder + title + '_' + str(int(T)).zfill(3) + 'K_IVcurve_warmup.txt' 

    customXepr.outputMeasurement(fileName, VdStart=-2, VdStop=2, VdStep=0.1, Vg=(0,))