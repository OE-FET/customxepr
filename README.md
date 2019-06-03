[![Documentation Status](https://readthedocs.org/projects/customxepr/badge/?version=latest)](https://customxepr.readthedocs.io/en/latest/?badge=latest)

# CustomXepr

A Python instrument controller and GUI for Bruker E500 EPR spectrometers, MercuryiTC
temperature controllers and Keithley 2600 series source measurement units. CustomXepr
relies on the python drivers [keithley2600](https://github.com/OE-FET/keithley2600) and
[mercuryitc](https://github.com/OE-FET/mercuryitc) and the respective user interfaces
[keithleygui](https://github.com/OE-FET/keithleygui) and
[mercurygui](https://github.com/OE-FET/mercurygui) for functionality regarding the
Keithley 2600 and MercuryiTC instruments.

![Screenshot of CustomXepr GUI](/screenshots/CustomXepr_all.png)

## Overview

CustomXepr for Linux and macOS enables the interaction with all instruments involved in
field induced electron spin resonance (FI-EPR) measurements: the Bruker E500 spectrometer,
through Bruker's Xepr Python API, the Oxford Instruments MercuryiTC temperature
controller, and the Keithley 2600 series of source measurement units (SMUs). The program
suite is structured into drivers and user interfaces for individual instruments (external
packages), CustomXepr's main class which provides higher level functions that often
combine functionality from multiple instruments, and a manager which handles the
scheduling of experiments.

The aim of CustomXepr is twofold: First and foremost, it enables the user to automate and
schedule full measurement plans which may run for weeks without user input. Second, it
complements the functionality of Bruker's Xepr control software. This includes for
instance powerful logging capabilities, a more accurate determination of the cavity's
Q-value from its frequency response, more reliable tuning of the cavity, the ability to
re-tune the cavity during long-running measurements, logging of the cryostat temperature
during measurements, and many more. Low level functionality and communication with the
spectrometer remains with Xepr.

![CustomXepr structure](/screenshots/CustomXepr_structure.png)

## Installation
Make sure that you have PyQt or PySide installed on your system (all other dependencies
will be installed automatically). Then install CustomXepr by running in a terminal:
```
$ pip install git+https://github.com/OE-FET/customxepr
```
CustomXepr depends on its own version of [pyqtgraph](http://www.pyqtgraph.org) which
includes some important bug fixes. If you previously did not have pyqtgraph installed, the
correct version will automatically be downloaded and installed for you. Otherwise, please
uninstall pyqtgraph and then reinstall it form [http://www.github.com/OE-
FET/pyqtgraph](http://www.github.com/OE-FET/pyqtgraph) by running:
```
$ pip install git+https://github.com/OE-FET/pyqtgraph
```
This should not break any other packages which also depend on pyqtgraph.

## Instrument communication
CustomXepr communicates with with the Keithley and MercuryiTC through NI-VISA or pyvisa-py
and is therefore independent of the actual interface, e.g., Ethernet, USB, or GPIB.
Connections to the EPR spectrometer are handled through Bruker's Xepr Python API.

## Usage

CustomXepr can be run interactively from a Jupyter console, or as a standalone program. In
the latter case, it will create its own internal Jupyter console for the user to run
commands.

You can start CustomXepr from a Python command prompt as follows:
```python
>>> from customxepr import run
>>> customXepr, xepr, mercury, mercury_feed, keithley, ui = run()
```
If executed from an Jupyter console, this will automatically start the integrated Qt event
loop and run in interactive mode. To start CustomXepr from the console / terminal, run
`CustomXepr`.

CustomXepr has a user interface which displays all jobs waiting in the queue, all results
returned from previous jobs, and all logging messages. Common tasks such as pausing,
aborting and clearing jobs, plotting and saving returned data, and setting temperature
stability tolerances can be performed through the interface itself. However, apart from
tuning the cavity and reading a Q-factor, all jobs  must be scheduled programmatically
through the provided Jupyter console.

## Job-scheduling

CustomXepr's core consists of functions for preconfigured tasks, such as changing the
cryostat temperature, recording a transfer curve, performing a preconfigured EPR
measurement. For instance, `customXepr.setTemperature(110)` tells the MercuryiTC to change
its temperature set-point to 110 K and waits until the latter is reached and maintained
with the desired stability (default: ±0.1 K for 120 sec). It also adjusts the helium flow
if necessary and warns the user if the target temperature cannot be reached within the
expected time. `customXepr.runExperiment(powersat)` will run the preconfigured EPR
measurement "powersat" while tuning the cavity between scans and monitoring the
temperature stability during the measurement.

Such built in jobs are not performed immediately but are queued and run after the
successful completion of the previous jobs. Any data returned by a job, such as a transfer
curve or a cavity mode picture, will be kept in a result queue and saved to a specified
file if requested. If the returned object has `save` and `plot` methods implemented, one
can right-click on its entry in the GUI to plot the data or save it to the hard drive.

CustomXepr functions that are expected to run for longer than 1 sec can gracefully abort
upon user request without leaving the setup in an inconsistent state.

![Screenshot of CustomXepr GUI](/screenshots/CustomXepr_jobs.png)

In addition, the queuing system can be used to manually schedule any user-specified jobs,
related or unrelated to the EPR setup and its ancillary equipment. This can be done with
the `queued_exec` decorator from `customxepr.manager`:

```python
    >>> import time
    >>> from customxepr.manager import Manager, queued_exec
    >>> manager = Manager()
    >>> # create test function
    >>> @queued_exec(manager.job_queue)
    ... def test_func(*args):
    ...     # do something
    ...     for i in range(0, 10):
    ...         time.sleep(1)
    ...		    # check for requested aborts
    ...         if manager.abort.is_set()
    ...             break
    ...     return args  # return input arguments
    >>> # run the function: this will return immediately
    >>> test_func('test succeeded')
```

The result returned by `test_func` can be retrieved from the result queue as follows:

```python
    >>> result = manager.result_queue.get()  # blocks until result is available
    >>> print(result)
	test succeeded
```

More information regarding the manual scheduling of experiments can be found
[here](https://customxepr.readthedocs.io/en/latest/api/manager.html#manager.Manager).

## Logging and error handling

The detection and escalation of possible problems is key to enabling unattended
measurements. Otherwise the user may come back after two days expecting a completed
measurement cycle, only to see that the helium dewar was emptied a day ago or that the
program got stuck asking the user if it should really override a data file. CustomXepr
therefore includes logging capabilities to track the progress of jobs and notify the user
of potential problems.

All CustomXper methods release logging messages during their execution which may have the
levels "status", "info", "warning", and "error". Status notifications will only be shown
in the user interface and typically contain information about the progress of a job
(number of completed scans in an EPR measurement, countdown until the temperature is
stable, etc). Info notifications typically contain information about the beginning or
completion of a job (e.g., "Waiting for temperature to stabilize.", "All scans
complete."), and potentially useful information about how the job was completed (e.g.,
"Temperature stable at 120.01±0.02 K during scans.").

Warning notifications are logged when CustomXepr believes that there may be a problem
which requires user intervention, for instance if a job is taking significantly longer
than expected, or if the gas flow required to maintain a certain temperature is unusually
high. Finally, error messages are released if CustomXepr is unable to proceed with a job,
in which case it will abort and pause all pending jobs. Such errors may include loss of
communication with an instrument, repeated strong temperature fluctuations during an EPR
measurement, etc.

By default, all messages of level "info" and higher are saved to a log file in the user's
home directory and messages of level "warning" and higher are sent as an email to the
user's address. In addition, temperature readings are saved to a log file every 5 min,
allowing the user to retrospectively confirm the temperature stability during
measurements.

![Screenshot of CustomXepr GUI](/screenshots/CustomXepr_log.png)

## Mercury controls
CustomXepr includes a higher-level worker thread which regularly queries the MercuryiTC
for its sensor readings and provides a live stream of this data to other parts of the
software. This prevents individual functions from querying the MercuryiTC directly and
causing unnecessary overhead.

The user interface for the cryostat plots historic temperature readings going back up to
24 h and provides access to relevant temperature control settings such as gas flow, heater
power, and ramping speed while lower-level configurations such as calibration tables must
be changed programmatically through the provided Jupyter console.

The MercuryiTC user interface and driver have been split off as separate packages
[mercuryitc](https://github.com/OE-FET/mercuryitc) and [mercurygui](https://github.com/OE-
FET/mercurygui).

![Screenshot of Mercury GUI](/screenshots/MercuryGUI.png)

## Keithley controls
As with the cryostat, CustomXepr includes a high-level user interface for Keithley 2600
series instruments which allows the user to configure, record and save voltage sweeps such
as transfer and output measurements. Since there typically is no need to provide a live
stream of readings from the Keithley, the data from an IV-curve is buffered locally on the
instrument and only transferred to CustomXepr after completion of a measurement.

The Keithley 2600 user interface and driver have been split off as separate packages
[keithley2600](https://github.com/OE-FET/keithley2600) and
[keithleygui](https://github.com/OE-FET/keithleygui).

![Screenshot of Keithley GUI](/screenshots/KeithleyGUI.png)

## Example code

A measurement script which cycles through different temperatures and records EPR spectra
and transfer curves at each step reads as follows:

```python
# get preconfigured experiment from Xepr
exp = xepr.XeprExperiment('Experiment')
# set up different modulation amplitudes in Gauss for different temperatures
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
	transfer_file = folder + title + '_' + str(T) + 'K_transfer.txt'
	# record default transfer curve and save to file
	customXepr.transferMeasurement(path=transfer_file)

	# =================================================================
	# Perform EPR measurements at Vg = -70V and Vg = 0V
	# =================================================================
	for Vg in [0, -70]:
        customXepr.biasGate(Vg)  # bias gate
        # perform preconfigured EPR measurement, save to 'esr_path'
        esr_file = folder + title + '_' + str(T) + 'K_Vg_' + str(Vg)
        customXepr.runXeprExperiment(exp, path=esr_file, ModAmp=modAmp[T])
        customXepr.biasGate(0)  # set gate voltage to zero

customXepr.setStandby()  # ramp down field and set MW bridge to standby
```

In this code, all functions belonging to CustomXepr will be added to the job queue and
will be carried out successively such that, for instance, EPR measurements will not start
while the temperature is still being ramped.

## Email notifications

By default, email notifications are sent from 'ss2151@cam.ac.uk' via 'localhost' and most
email clients will therefore reject them as spam. CustomXepr at the moment provides no way
to modify the email settings via the user interface, but you can set them manually in the
config file in your home directory: '~/.CustomXepr/CustomXepr.ini'. Changes will be
applied when restarting CustomXper.

By default, the relevant section in the config file reads:

```ini
[SMTP]
mailhost = localhost
fromaddr = ss2151@cam.ac.uk
credentials = None
secure = None
```

To specify a non-standard SMTP port, use the `(host, port)` tuple format for the mailhost
argument. To specify authentication credentials, supply a `(username, password)` tuple for
the credentials argument. To specify the use of a secure protocol (TLS), pass in a tuple
for the secure argument. This will only be used when authentication credentials are
supplied. The tuple will be either an empty tuple, or a single-value tuple with the name
of a keyfile, or a 2-value tuple with the names of the keyfile and certificate file. For
example, to send emails via the Cambridge SMTP server, this section should be modified to
read:

```ini
[SMTP]
mailhost = ('smtp.hermes.cam.ac.uk', 587)
fromaddr = ss2151@cam.ac.uk
credentials = ('ss2151', 'my-secret-password')
secure = ()
```

## Requirements
*System requirements:*

- Linux or macOS (not tested on Windows)
- Python 2.7 or 3.6 and higher

*Recommended:*

- Bruker Xepr software with Python XeprAPI (required for EPR related functions)
- Postfix - mail transfer agent (required for email notifications from localhost)

*Required python modules:*
- PyQt5 >= 5.9 (PySide2 should also work but is not actively tested)

*Recommended python modules:*
- pyusb (only when using pyvisa-py backend)
- pyserial (only when using pyvisa-py backend)

## Acknowledgements
- Config modules are based on the implementation from [Spyder](https://github.com/spyder-ide).
- Scientific spin boxes are taken from [qudi](https://github.com/Ulm-IQO/qudi).
