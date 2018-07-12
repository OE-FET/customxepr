# CustomXepr

A Python instrument controller and GUI for Bruker E500 ESR spectrometers, MercuryiTC temperature controllers and Keithley 2600 series source measurement units.

## Overview

*CustomXepr* for Linux and macOS X enables the interaction with all instruments involved in electron spin resonance (ESR) measurements: the Bruker E500 spectrometer, through Bruker's Xepr Python API, the Oxford Instruments MercuryiTC temperature controller, and the Keithley 2600 series of source measurement units (SMUs).

The aim of CustomXepr is twofold: First and foremost, it enables the user to automate and schedule full measurement plans which may run for weeks without user input. Second, it complements the functionality of Bruker's Xepr control software. This includes for instance powerful logging capabilities for all key events, a more accurate determination of the cavity's Q-value from its frequency response, more reliable tuning of the cavity, the ability to re-tune the cavity during long-running measurements, logging of the cryostat temperature during measurements, and many more. On the other hand, low level functionality and communication with the spectrometer remains with Xepr.

![Screenshot of CustomXepr GUI](/Screenshots/Screenshot_all_dark.png)

## Job-scheduling

CustomXepr's core consists of functions for preconfigured tasks, such as changing the cryostat temperature, recording a transfer curve, performing a preconfigured ESR measurement.
For instance, `customXepr.setTemperature(110)` tells the MercuryiTC to change its temperature set-point to 110 K and waits until the latter is reached and maintained with the desired stability (default: ±0.1 K for 120 sec). It also adjust the helium flow if necessary and will warn the user if the target temperature cannot be reached within the expected time.
`customXepr.runExperiment(PowerSat)` will run the preconfigured ESR measurement "PowerSat" while tuning the cavity between scans and monitoring the temperature stability during the measurement.

Such built in jobs are not performed immediately but are queued and executed in the background after the successful completion of the previous jobs. Any data returned by a job, such as a transfer curve or a cavity mode picture, will be kept in a result queue and saved to a specified file if requested. CustomXepr functions that are expected to run for longer than 1 sec can gracefully abort upon user request without leaving the setup in an inconsistent state.

In addition, the queuing system can be used to manually schedule any user-specified function, related or unrelated to the ESR setup and its ancillary equipment.

## Logging and error handling

All CustomXper functions release logging messages during their execution which may have the levels "status", "info", "warning", and "error". Status notifications will only be shown in the user interface and typically contain information about the progress of a job (number of completed scans in an ESR measurement, countdown until the temperature is stable, etc). Info notifications typically contain information about the  beginning or completion of a job (e.g., "Waiting for temperature to stabilize.", "All scans complete."), and potentially useful information about how the job was completed (e.g., "Temperature stable at 120.01±0.02 K during scans.").

Warning notifications are only logged when CustomXepr believes that there may be a problem which requires user intervention, for instance if a job is taking significantly longer than expected, or if the gas flow required to maintain a certain temperature is unusually high. Finally, error messages are only released if CustomXepr is unable to proceed with a job, in which case it will abort and pause all pending jobs. Such errors may include loss of communication with an instrument, repeated strong temperature fluctuations during an ESR measurement, etc.

By default, all messages of level "info" and higher are saved to a log file in the user's home directory and messages of level "warning" and higher are sent as an email to the specified address. In addition, temperature readings are saved to a log file every 5 min, allowing the user to retrospectively confirm the temperature stability during measurements.

The detection and escalation of possible problems is key to enabling unattended measurements. Otherwise the user may come back after two days expecting a completed measurement cycle, only to see that the helium dewar was emptied a day ago or that the program got stuck asking the user if it should really override a data file.

## Example code

CustomXepr has a user interface which displays all jobs waiting in the queue, all results returned from previous jobs, and all logging messages. Common tasks such as pausing, aborting and clearing jobs, plotting and saving returned data, and setting temperature stability tolerances can be performed through the interface itself. However, apart from tuning the cavity and reading a Q factor, all jobs  must be scheduled programmatically through the console. For example, a measurement script which cycles through different temperatures and records ESR spectra and transfer curves at each step reads as follows:

```python
# get preconfigured experiment from Xepr
Exp = xepr.XeprExperiment('Experiment')
# set-up modulation amplitudes in Gauss for different temperatures
modAmp = {5: 3, 50: 2, 100: 1, 150: 1, 200: 1, 250: 1.5, 300: 2}

# specify folder to save data
folder = '/path/to/folder/'
title = 'my_sample'
	
for T in [5, 50, 100, 150, 200, 250, 300]:
	# =================================================================
	# Prepare temperature
	# =================================================================
	customXepr.setTemperature(T)        # set desired temperature 
	customXepr.customtune()             # tune the cavity
	customXepr.getQValueCalc(folder, T) # measure and save the Q factor
	
	# =================================================================
	# Perform FET measurements
	# =================================================================
	# generate file name for transfer curve
	transferFile = folder + title + '_' + str(T) + 'K_transfer.txt'
	# record default transfer curve and save to file
	customXepr.transferMeasurement(transferFile)
	
	# =================================================================
	# Perform ESR measurements at Vg = -70V and Vg = 0V
	# =================================================================
	for Vg in [0, -70]:
	  	customXepr.biasGate(Vg)  # bias gate
		# perform preconfigured ESR measurement
		customXepr.runExperiment(Exp, ModAmp=modAmp[T])
		customXepr.biasGate(0)  # set gate voltage to zero
        
    	# save ESR spectrum to file
		esrDataFile = folder + title + '_' + str(T) + 'K_Vg_' + str(Vg)
		customXepr.saveCurrentData(esrDataFile)
       
customXepr.setStandby()  # ramp down field and set MW bridge to standby	
```

In this code, all functions belonging to CustomXepr will be added to the job queue and will be carried out successively such that, for instance, ESR measurements will not start while the temperature is still being ramped.

## Mercury controls
CustomXepr includes a Python driver for the MercuryiTC temperature controller and a higher-level worker thread which regularly queries the MercuryiTC for its sensor readings and provides a live stream of this data to other parts of the software. This prevents individual functions from querying the MercuryiTC directly and causing unnecessary overhead.

The user interface for the cryostat plots historic temperature readings going back up to 24\,h and provides access to relevant temperature control settings such as gas flow, heater power, and ramping speed while lower-level configurations such as calibration tables must be changed programatically.
## Keithley controls
As with the cryostat, CustomXepr includes a Python driver for the Keithley 2600 series and a high-level user interface which allows the user to configure, record and save voltage sweeps such as transfer and output measurements. Since there typically is no need to provide a live stream of readings from the Keithley, the data from an IV-curve is buffered locally on the instrument and only transferred to CustomXepr after completion of a measurement.

## System requirements
*Required*:

-Linux or macOSX
-Python 2.7
-NI-VISA
-PyQT4 or PyQt5 (PyQt 5 preferred)
-Python dependencies

*Optional*:

-Bruker Xepr software (ESR related functions will not work without Xepr)
-fping   - command line tool for pings with millisecond timeout
-Postfix - mail transfer agent for macOSX and Linux, required for email
          notifications. 
	  
*Python modules*:

-matplotlib
-decorator
-pyvisa
-qtpy
-lmfit
-numpy
-yagmail
-pyqtgraph
qdarkstyle
jupyter_qtconsole_colorschemes
