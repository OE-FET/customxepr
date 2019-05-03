#### v2.3.2-dev (2019-05-03)
_Added:_
- Allow configuration of a custom SMTP server for email notifications in the config file '~/.CustomXepr/CustomXepr.ini'.

#### v2.3.1 (2019-04-23)

_Added:_
- Double click on a result in the GUI to plot it.
- Enable editing of ordinate data in `XeprData` instance.
- Added a keyword argument `low_q` to `customtune` to enable tuning with low Q-values (default: `low_q=False`).
- Added a keyword argument `auto_gf` to `setTemperature` to disable or enable automatic gasflow control (default: `auto_gf=True`).
- Added a keyword argument `htt_file` to `heater_target` to select a file with a custom heater target table.

_Changed:_
- Simplified access and modification of `XeprData` paramaters. Parameter values can now be updated directly by assigning a value to their dictionary entry.
- Updated default heater target table for MercuryITC.
- Log files older than 7 days are deleted automatically on startup.
- Removed all Qt related depencies from non-GUI modules. This makes it easier to run CustomXepr in headless mode from the command line.

_Removed:_
- Deprecated `set_param` and `get_param` methods of `XeprData`. Use the `pars` attribute with dictionary type access instead.

#### v2.3.0 (2019-03-20)

This release focuses on under-the-hood improvements and provides significant speedups to the user interface (plotting data, deleting a large number of queued jobs, etc).

_Changed:_

- Reduced the startup time when no instruments can be found.
- Added info messages to the splash screen.
- Swtiched plotting library for Mercury ITC and Keithley 2600 from Matplotlib to pyqtgraph. This allows for smoother user interactions with plots.
- Bug fixes for PyQt 5.12.
- Performance improvements when deleting a large number of results or pending jobs: previously _O(n^2)_, now _O(n)_ performance.
- Better organization of code into submodules.

#### v2.2.2 (2019-02-19)

This release adds support for reading and writing Bruker Xepr data files in the BES3T format.

_Added:_

- Added `XeprData` class to hold, read and save Xepr measurement data files. `XeprData`
  provides methods to access and modifiy measurement parameters and to plot the data.
  It is compalitble with all Xepr experiment types, saved in the Bruker BES3T file format
  up to version 1.2 (currently used by Xepr).

_Changed:_

- `runXeprExperiment` now accepts a path parameter. If given, the resulting data
  will be saved to the specified path, togther with the last-measured Q-value
  and temperature setpoint.
- Tweaked icons in user interface.

_Removed:_

- Removed the option to specify a title when saving an ESR data file. The file
  name is now always used as title.
- `saveCurrentData` will be removed in a future version of CustomXepr. Use the `path`
  keyword of `runXeprExperiment` to save the measurement data instead.

#### v2.2.1 (2019-01-25)

This release introduces online documentation for CustomXepr and user interface improvements.

_Added:_

- Job history now remains visible together with icons indicating the job status.
- Documentation is now available at [https://customxepr.readthedocs.io](https://customxepr.readthedocs.io).

_Changed:_

- Switched from custom TslSMTPHandler to python-bundled SMTPHandler for email
  notifications.
- Improved docstrings.

#### v2.2.0 (2019-01-09)

_Added:_

- Added terminal / command line script "CustomXepr".
- Added confidence interval for Q-value calculation in ModePicture class.
- Window positions and sizes are saved and restored between sessions.
- Show errors during job excecution in GUI in addition to email notifications.
- Nicely colored tracebacks for error messages.

_Changed:_

- CustomXepr is now distributed as a python package and can be installed with
  pip.

_Fixed:_

- Fixed a bug that could result in values inside spin-boxes to be displayed
  without their decimal marker on some systems.
- Fixed a bug that could result in crashes after closing the keithley or
  mercury control windows.

_Removed:_

- Removed all ETA estimates for experiments.

#### v2.1.1

_Added:_

- Included revamped keithleygui with IV sweep functionality.
- Compatability with Python 3.6 and higher.

_Changed:_

- Proper disconnection from instruments when closing windows or shutting down
  the console with "exit" command.

_Fixed:_

- Fixed a bug that would prevent Xepr experiments to run if the measurement
  time cannot be estimated. Applies for instance to rapid scan and time domain
  measurements where proper ETA estimates have not yet been implemented.

#### v2.1.0

_Added:_

- Warnings when invalid file paths are handed to Xepr.

_Changed:_

- Split off mercury_gui and keithley_gui as separate packages.

_Removed:_

- Removed dark theme: code is easier to maintain. System level dark themes,
  such as macOS Mojave's dark mode, may be supported in the future when Qt
  support is added.

#### v2.0.1

_Changed:_

- Moved default driver backends from NI-VISA to pyvisa-py. It is no longer
  necessary to install NI-VISA from National Instruments on your system.
- Moved drivers to external packages. Install with pip before first use.
- Improved data plotting in Mercury user interface:
    - heater output and gasflow are plotted alongside the temperature
    - major speedups in plotting framerate by relying on numpy for updating the
      data and redrawing only changed elements of plot widget
    - allow real-time panning and zooming of plots
- Started working on Python 3 compatability.
