## v3.1.3

#### Fixed:

- Fixed spurious notifications from log messages emitted outside of customxepr. 

## v3.1.2

#### Added:

- Added support to parse and plot the pulse sequence information stored in the Bruker DSC
  file in the tables Psd1 to Psd36:

  ```Python
  >>> from customxepr.experiment import XeprData
  >>> dset = XeprData("path")
  >>> dset.pulse_sequence.plot()
  >>> print(dset.pulse_sequence.pulse_channels[5])
  <PulseChannel(Psd6: +x)>
  >>> print(dset.pulse_sequence.pulse_channels[5].pulses)
  [<Pulse(position=276, length=4)>, <Pulse(position=676, length=44)>]
  ```
- Added a keyword argument `settling_time` to `runXeprExperiment` to wait between
  individual scans. This can be useful in case of temperature fluctuations between
  scans.

#### Changed:

- Remove custom `exit_customxepr()` function. Instead, close the console to exit
  CustomXepr or run `exit` when started from an IPython or Jupyter shell.
- Increase default maximum cooling temperature to 20°C.
- Remember the location of the console window between restarts.
- Set current directory of Xepr to directory of last-saved data.
- The Qt event loop is no longer started on every import but just when actually starting
  the GUI or plotting a figure.
- `getValueXepr` no longer accepts a path argument.
- `getQValueCalc` no longer saves two files but the mode picture only. The given path
  must now be the full file path. The temperature data will now be saved together with
  the mode picture.
- `getQValueCalc` no longer accepts a temperature argument. Instead, the temperature
  will be read from the Mercury if available.
- The `ModePicture` class now accepts arbitrary metadata in dictionary form. This data
  will be saved as tab-delimited metadata in the mode picture file.

#### Fixed:

- Fixed an issue when saving a dateset through Xepr when the path contains whitespace or
  backslashes. The path is now quoted with `shlex.quote` before being passed to Xepr.

## v3.1.1

#### Changed:

- Only show single-line previews of results in GUI.
- Improve warnings for too high gasflow.
- Allow overriding default tolerance and wait time in `waitTemperatureStable`.

#### Added:

- Monitor cooling water temperature during measurements and interrupt ESR measurements if
  too high.
- Added config file entries for the maximum cooling temperature and the temperature sensor
  names for the ESR and cooling water.

#### Fixed:

- Fixes an issue in `customxepr.experiment.xepr_dataset.XeprParam` where the `unit`
  attribute would return the value instead of the unit.

## v3.1.0

#### Added:

- Added API similar to `concurrent.futures.Future` to `customxepr.manager.Experiment`.
- Return an experiment instance from all async customxepr method calls. This instance can
  be used to get the result directly, instead of getting it from the result queue. Usage:

  ```Python
  future = customXepr.runXeprExperiment(...)
  result = future.result()  # will block until result is available
  ```

#### Changed:

- `CustomXepr.tune` and `CustomXepr.finetune` can now be aborted.
- `ModePicture.load(...)` no longer returns the raw data but rather populates the class
  attributes of `ModePicture` with the loaded data.
- `XeprData` now shows the experiment title in its string representation.
- Changed the default email address for notifications to physics-oe-esr-owner@lists.cam.ac.uk.
- Improvements to documentation.
- Require PyQt5 instead of qtpy / PySide2.

#### Fixed:

- Fixes an issue where `CustomXepr.tune` and `CustomXepr.finetune` would return
  immediately, even if tuning was not complete.

## v3.0.0

This release drops support for Python 2.7. Only Python 3.6 and higher are supported.

#### Added:

- Method `CustomXepr.getExpDuration` to estimate the duration of an Xepr experiment.
- Added synchonous functions for all of CustomXepr's asynchronous functions (which will be
  queued). These are automatically generated and end with the suffix "_sync".
- Added `shape` attribute to `XeprData` class.

#### Changed:

- Changed the abort behaviour of a measurement: Instead of finishing the current scan and
  pausing afterwards, the scan is aborted immediately.
- Renamed `setDrainCurrent` to `setCurrent` and `setGateVoltage` to `setVoltage`.
- `setVoltage` no longer turns the other SMUs off.
- Optimized the truncation of long items in the list of running expriements.
- Changed the priority of locations to search for the XeprAPI:
    1) path from the environment variable `XEPR_API_PATH` (if set)
    2) installed python packages
    3) pre-installed version from Xepr
- Renamed `applyCurrent` to `setCurrent`.
- The `queued_exec` decorator is now an attribute of `customXepr.manager.Manager` and no
  longer requires the job queue as an argument. Instead, the manager's `job_queue` will be
  used automatically.
- The `queued_exec` decorator now is re-entrant: decorated functions which are called from
  within the worker thread won't be queued themselves.
- Moved `CustomXepr._wait_stable` to a public method `CustomXepr.waitTemperatureStable`.
- Enforce usage of `exit_customxepr()` to exit.
- Set the default address for email notifications to 'physics-oe-esr-owner@lists.cam.ac.uk'.
- Increased the default timeout for PyVisa communication from 2 sec to 5 sec.

#### Fixed:

- Fixed a bug when plotting aquired results: This was related to the IPython kernel or the
  interactive console using the wrong GUI backend. It now uses the Qt backend.
- Fixed a bug which would cause `XeprData.plot` to fail in case of multiple datasets per
  scan, e.g., for simultanious detection of the in-phase and out-of-phase signals.
- Fixed several Python 3 compatibility issues.

#### Removed:

- Support for Python 2.7. Only Python 3.6 and higher will be supported. Please migrate.

## v2.3.4 (2019-10-09)

Main changes are:

- Possible file names for Xepr data are no longer limited by Xepr's file name restrictions.
- Added a function `exit_customxepr` which gracefully disconnects all instruments before
  quitting the Python console. This avoids errors on the next startup.
- Bug fixes.

In more detail:

#### Added:

- Added a function `exit_customxepr` which gracefully disconnects all instruments
  and then exits the Python console. This avoids errors on the next startup.
- Added a help button to the main UI, replacing the copyright notice.
- Added support for dark interface themes, such as dark mode in macOS Mojave. This
  requires a version of PyQt / Qt which supports system themes, e.q. PyQt 5.12+ for macOS.

#### Changed:

- Changed how Xepr data is saved: CustomXepr will now *always* save to a temporary file
  first which is guaranteed to comply with Xepr's file name restrictions. This temporary
  file will then be reloaded to add custom parameters and will be saved through Python to
  any path which the file system accepts.
- If CustomXepr is not started from an IPython console, use an in-process IPython kernel
  and Jupyter console widget for user interactions. This gives us better control over the
  appearance of the console widget.
- Removed pyqrgraph dependency.

#### Fixed:

- Fixed a bug which could cause `customXepr.setGateVoltage()` and subsequent Keithley
  commands to fail due to an invalid command sent to the Keithley.
- Fixed a bug which would cause queued function calls without any arguments not to show
  in the job queue window.
- Fixed a bug which would prevent the phase from being cycled by 360 deg when hitting the
  upper or lower limit during a tuning routine.

## v2.3.3 (2019-07-15)

This release focuses on minor UI improvements. The most notable change is a better
handling of Bruker data files: the order of entries in DSC files is preserved when saving
through CustomXepr.

#### Changed:

- Small tweaks to dialog windows (update info, about window, etc.).
- Preserve order of entries in DSC files in Python 2. Previously, the order of sections
  and parameter would be randomized when loading and saving a Bruker DSC files with
  CustomXepr in Python 2.7.
- Moved some custom widgets which are shared between `customxepr`, `keithleygui` and
  `mercurygui` to a common submodule `pyqt_labutils`.

## v2.3.2 (2019-05-25)

Improves compatibility of `XeprData` with Bruker's Xepr BES3T file format: support
complex data and more exotic data formats.

#### Added:

- Expanded support for Xepr data files: introduced support for complex data sets, 32-bit
  floats and 32-bit signed integers as well as multiple ordinate data sets per data file.
- Introduced support for different byte-orders, as specified in '.DSC' file.
- Save the standard error from fitting the Q-Value as a new parameter 'QValueErr' in the
  DSC file, if available.
- Allow configuration of a custom SMTP server for email notifications in the config file
  '~/.CustomXepr/CustomXepr.ini'.

#### Changed:

- Improved the usefulness of some log messages.
- Keep measurement logs for 356 days instead of 7 days.
- Improved formatting of DSC files saved through CustomXepr vs Xepr. Number formatting,
  e.g., the number of significant digits, will be preserved unless the parameter value
  has changes

#### Fixed:

- Fixed a bug in `XeprData` which would save y-axis and z-axis data files with the wrong
  byte-order. Ordinate data and x-axis data were not affected. Xepr expects data files to
  be saved with the byte-order specified in the DSC file (typically big-endian).
- Fixed a bug in `XeprData` when saving the 'PolyCof' parameter or other array data to
  DSC files: The array shape would be incorrectly saved in the header (with row and
  column numbers swapped).
- Fixed a deadlock when removing an item from the result queue.
- Fixed an issue where the job status icons might not update until the user clicks on the
  CustomXepr window.

## v2.3.1 (2019-04-23)

This release adds several options (keyword arguments) to CustomXepr functions. It also
fully separates UI from non-UI modules.

#### Added:

- Double click on a result in the GUI to plot it.
- Enable editing of ordinate data in `XeprData` instance.
- Added a keyword argument `low_q` to `customtune` to enable tuning with low Q-values
  (default: `low_q=False`).
- Added a keyword argument `auto_gf` to `setTemperature` to disable or enable automatic
  gas flow control (default: `auto_gf=True`).
- Added a keyword argument `htt_file` to `heater_target` to select a file with a custom
  heater target table.

#### Changed:

- Simplified access and modification of `XeprData` parameters. Parameter values can now be
  updated directly by assigning a value to their dictionary entry.
- Updated default heater target table for MercuryITC.
- Log files older than 7 days are deleted automatically on startup.
- Removed all Qt related dependencies from non-GUI modules. This makes it easier to run
  CustomXepr in headless mode from the command line.

#### Removed:

- Deprecated `set_param` and `get_param` methods of `XeprData`. Use the `pars` attribute
  with dictionary type access instead.

## v2.3.0 (2019-03-20)

This release focuses on under-the-hood improvements and provides significant speedups to
the user interface (plotting data, deleting a large number of queued jobs, etc).

#### Changed:

- Reduced the startup time when no instruments can be found.
- Added info messages to the splash screen.
- Switched plotting library for Mercury ITC and Keithley 2600 from Matplotlib to
  pyqtgraph. This allows for smoother user interactions with plots.
- Performance improvements when deleting a large number of results or pending jobs:
  previously _O(n^2)_, now _O(n)_ performance.
- Better organization of code into submodules.

#### Fixed:

- Bug fixes for PyQt 5.12.


## v2.2.2 (2019-02-19)

This release adds support for reading and writing Bruker Xepr data files in the BES3T
format.

#### Added:

- Added `XeprData` class to hold, read and save Xepr measurement data files. `XeprData`
  provides methods to access and modify measurement parameters and to plot the data.
  It is compatible with all Xepr experiment types, saved in the Bruker BES3T file format
  up to version 1.2 (currently used by Xepr).

#### Changed:

- `runXeprExperiment` now accepts a path parameter. If given, the resulting data
  will be saved to the specified path, together with the last-measured Q-value
  and temperature set point.
- Tweaked icons in user interface.

#### Removed:

- Removed the option to specify a title when saving an ESR data file. The file
  name is now always used as title.
- `saveCurrentData` will be removed in a future version of CustomXepr. Use the `path`
  keyword of `runXeprExperiment` to save the measurement data instead.

## v2.2.1 (2019-01-25)

This release introduces online documentation for CustomXepr and user includes interface
improvements.

#### Added:

- Job history now remains visible together with icons indicating the job status.
- Documentation is now available at [https://customxepr.readthedocs.io](https://customxepr.readthedocs.io).

#### Changed:

- Switched from custom TslSMTPHandler to python-bundled SMTPHandler for email
  notifications.
- Improved docstrings.

## v2.2.0 (2019-01-09)

#### Added:

- Added terminal / command line script "CustomXepr".
- Added confidence interval for Q-value calculation in ModePicture class.
- Window positions and sizes are saved and restored between sessions.
- Show errors during job execution in GUI in addition to email notifications.
- Nicely colored trace backs for error messages.

#### Changed:

- CustomXepr is now distributed as a python package and can be installed with
  pip.

#### Fixed:

- Fixed a bug that could result in values inside spin-boxes to be displayed
  without their decimal marker on some systems.
- Fixed a bug that could result in crashes after closing the keithley or
  mercury control windows.

#### Removed:

- Removed all ETA estimates for experiments.

## v2.1.1

#### Added:

- Included revamped keithleygui with IV sweep functionality.
- Compatibility with Python 3.6 and higher.

#### Changed:

- Proper disconnection from instruments when closing windows or shutting down
  the console with "exit" command.

#### Fixed:

- Fixed a bug that would prevent Xepr experiments to run if the measurement
  time cannot be estimated. Applies for instance to rapid scan and time domain
  measurements where proper ETA estimates have not yet been implemented.

## v2.1.0

#### Added:

- Warnings when invalid file paths are handed to Xepr.

#### Changed:

- Split off mercury_gui and keithley_gui as separate packages.

#### Removed:

- Removed dark theme: code is easier to maintain. System level dark themes,
  such as macOS Mojave's dark mode, may be supported in the future when Qt
  support is added.

## v2.0.1

#### Changed:

- Moved default driver backends from NI-VISA to pyvisa-py. It is no longer
  necessary to install NI-VISA from National Instruments on your system.
- Moved drivers to external packages. Install with pip before first use.
- Improved data plotting in Mercury user interface:
    - heater output and gas flow are plotted alongside the temperature
    - major speedups in plotting frame rate by relying on numpy for updating the
      data and redrawing only changed elements of plot widget
    - allow real-time panning and zooming of plots
- Started working on Python 3 compatibility.
