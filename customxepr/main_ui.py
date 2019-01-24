# -*- coding: utf-8 -*-

"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import
import os
from qtpy import QtCore, QtWidgets, QtGui, uic
import logging
import platform
import subprocess
import re
import pydoc
import inspect
import webbrowser

# local imports
from customxepr.main import CustomXepr, __version__, __year__, __author__
from customxepr.manager import Experiment
from customxepr.config.main import CONF
from customxepr.utils.misc import ErrorDialog
from customxepr.utils.notify import Notipy

_root = QtCore.QFileInfo(__file__).absolutePath()


# =============================================================================
# Set up logging handlers for STATUS, INFO and ERROR messages
# =============================================================================


class QInfoLogHandler(logging.Handler, QtCore.QObject):
    """
    Handler which adds all logging event messages to a QStandardItemModel. This
    model will be used to populate the "Message log" in the GUI with all
    logging messages of level INFO and higher.
    """

    notify = Notipy()

    def __init__(self):
        logging.Handler.__init__(self)
        QtCore.QObject.__init__(self)

        # create QStandardItemModel
        self.model = QtGui.QStandardItemModel(0, 3)
        self.model.setHorizontalHeaderLabels(['Time', 'Level', 'Message'])

    def emit(self, record):
        # format logging record
        self.format(record)
        time_item = QtGui.QStandardItem(record.asctime)
        level_item = QtGui.QStandardItem(record.levelname)
        msg_item = QtGui.QStandardItem(record.msg)

        # add logging record to QStandardItemModel
        self.model.appendRow([time_item, level_item, msg_item])
        # show notification
        self.notify.send(title='CustomXepr Info', message=record.message)


class QStatusLogHandler(logging.Handler, QtCore.QObject):
    """
    Handler which emits a signal containing the logging message for every
    logged event. The signal will be connected to "Status" field of the GUI and
    trigger a 30 min time out counter which will be reset by the next signal.
    """
    status_signal = QtCore.Signal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QtCore.QObject.__init__(self)

    def emit(self, record):
        # format logging record
        self.format(record)
        # emit logging record as signal
        self.status_signal.emit('Status: ' + record.message)


class QErrorLogHandler(logging.Handler, QtCore.QObject):
    """
    Handler which displays a message box with information about occurred errors.
    """

    error_signal = QtCore.Signal(tuple)

    def __init__(self):
        logging.Handler.__init__(self)
        QtCore.QObject.__init__(self)

    def emit(self, record):
        self.format(record)
        self.error_signal.emit(record.exc_info)


# create QInfoLogHandler to handle all INFO level events
fmt_string = '%(asctime)s %(threadName)s %(levelname)s: %(message)s'
info_fmt = logging.Formatter(fmt=fmt_string, datefmt='%H:%M')
info_handler = QInfoLogHandler()
info_handler.setFormatter(info_fmt)
info_handler.setLevel(logging.INFO)

# create QStatusLogHandler to handle all STATUS level events
status_handler = QStatusLogHandler()
status_handler.setLevel(logging.STATUS)

# create QErrorLogHandler to handle all ERROR level events
error_handler = QErrorLogHandler()
error_handler.setLevel(logging.ERROR)

# add handlers
root_logger = logging.getLogger()
logger = logging.getLogger('customxepr.main')

root_logger.addHandler(status_handler)
root_logger.addHandler(info_handler)
logger.addHandler(error_handler)


# =============================================================================
# Define JobStatusApp class
# =============================================================================


class JobStatusApp(QtWidgets.QMainWindow):

    """
    A GUI for CustomXepr, composed of three panels:

        1) List of queued jobs and functionality to pause, resume and abort any
           job execution. Basic CustomXepr settings such as the temperature
           settling time and tolerance, as well as shortcuts to tuning and
           Q-value evaluation routines, can be accesses here as well.

        2) List of all results. Right-clicking on a result exposes plotting and
           saving functionality if corresponding methods are provided by the
           result object (e.g, FET characteristics, mode pictures, etc.)

        3) Message log for info-messages and higher. This panel also exposes a
           UI to specify email addresses for notifications and the desired
           notification level (Status, Info, Warning or Error).

    This class requires a :class:`CustomXepr` instance as input.

    """

    MAX_JOB_HISTORY_LENGTH = 1

    def __init__(self, customxepr):
        super(self.__class__, self).__init__()

        # get input arguments
        self.customxepr = customxepr
        self.job_queue = customxepr.job_queue
        self.result_queue = customxepr.result_queue
        self.running = customxepr.running
        self.abort_event = customxepr.abort
        self.abort_event_keithley = customxepr.keithley.abort_event

        # =====================================================================
        # Set-up the UI
        # =====================================================================

        # load layout file, setup toolbar on macOS
        if platform.system() == 'Darwin':
            layout_file = 'main_ui_macos.ui'
        else:
            layout_file = 'main_ui_linux.ui'

        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                layout_file), self)

        if platform.system() == 'Darwin':
            # create unified toolbar
            self.toolbar = QtWidgets.QToolBar(self)
            self.create_toolbar()

        self.labelCopyRight.setText('© {0}, {1}.'.format(
                __year__, __author__))

        # create about window
        self.aboutWindow = AboutWindow()

        # load resources
        self.icon_queued = QtGui.QIcon(_root + '/resources/queued@2x.png')
        self.icon_running = QtGui.QIcon(_root + '/resources/running@2x.png')
        self.icon_paused = QtGui.QIcon(_root + '/resources/pause@2x.png')
        self.icon_aborted = QtGui.QIcon(_root + '/resources/aborted@2x.png')
        self.icon_failed = QtGui.QIcon(_root + '/resources/failed@2x.png')
        self.icon_finished = QtGui.QIcon(_root + '/resources/finished@2x.png')

        # assign menu bar actions
        self.action_About.triggered.connect(self.aboutWindow.show)
        self.actionCustomXepr_Help.triggered.connect(self.aboutWindow.show)
        self.actionShow_log_files.triggered.connect(self.on_log_clicked)
        self.action_Exit.triggered.connect(self.exit_)

        if not os.popen('Xepr --apipath').read() == '':
            url = 'file://' + os.popen('Xepr --apipath').read() + '/docs/XeprAPI.html'
            self.actionXeprAPI_Help.triggered.connect(lambda: webbrowser.open_new(url))
        else:
            self.actionXeprAPI_Help.setEnabled(False)

        # restore last position and size
        self.restore_geometry()

        # =====================================================================
        # Connect UI to CustomXepr functionality
        # =====================================================================

        # check status of worker thread (Paused or Running) and adjust buttons
        self.check_paused()

        # get email list and notification level
        self.get_email_list()
        self.get_notification_level()

        # get temperature control settings
        self.lineEditT_tolerance.setValue(self.customxepr.temperature_tolerance)
        self.lineEditT_settling.setValue(self.customxepr.temp_wait_time)

        # perform various UI updates after status change
        status_handler.status_signal.connect(self.statusField.setText)
        status_handler.status_signal.connect(self.check_paused)
        status_handler.status_signal.connect(self.get_email_list)

        # notify user of any errors in job execution with a message box
        error_handler.error_signal.connect(self.show_error)

        # create data models for message log, job queue and result queue
        self.messageLogModel = info_handler.model
        self.jobQueueModel = QtGui.QStandardItemModel(0, 3)
        self.resultQueueModel = QtGui.QStandardItemModel(0, 3)

        h1 = ['Time', 'Level', 'Message']
        h2 = ['Function', 'Arguments', 'Keyword Arguments']
        h3 = ['Type', 'Size', 'Value']

        self.messageLogModel.setHorizontalHeaderLabels(h1)
        self.jobQueueModel.setHorizontalHeaderLabels(h2)
        self.resultQueueModel.setHorizontalHeaderLabels(h3)

        # add models to views
        self.messageLogDisplay.setModel(self.messageLogModel)
        self.jobQueueDisplay.setModel(self.jobQueueModel)
        self.resultQueueDisplay.setModel(self.resultQueueModel)

        # populate models with queue elements
        self.populate_results()
        self.populate_jobs()

        # update views when items are added to or removed from queues
        self.customxepr.result_queue.put_signal.connect(self.add_result)
        self.customxepr.result_queue.pop_signal.connect(self.on_result_pop)

        self.customxepr.job_queue.added_signal.connect(self.on_job_added)
        self.customxepr.job_queue.removed_signal.connect(self.on_job_removed)
        self.customxepr.job_queue.status_changed_signal.connect(self.on_job_status_changed)

        # set context menus for job_queue and result_queue items
        self.resultQueueDisplay.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.jobQueueDisplay.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.resultQueueDisplay.customContextMenuRequested.connect(self.open_result_context_menu)
        self.jobQueueDisplay.customContextMenuRequested.connect(self.open_job_context_menu)

        # =====================================================================
        # Connect signals, slots, and callbacks
        # =====================================================================

        self.qValueButton.clicked.connect(self.on_qvalue_clicked)
        self.tuneButton.clicked.connect(self.on_tune_clicked)

        self.pauseButton.clicked.connect(self.on_pause_clicked)
        self.abortButton.clicked.connect(self.on_abort_clicked)
        self.clearButton.clicked.connect(self.on_clear_clicked)

        self.lineEditEmailList.returnPressed.connect(self.set_email_list)
        self.lineEditT_tolerance.valueChanged.connect(self.set_temperature_tolerance)
        self.lineEditT_settling.valueChanged.connect(self.set_t_settling)

        self.bG.buttonClicked['int'].connect(self.on_bg_clicked)

        # Universal timeout:
        # Send an email notification if there is no status update for 30 min.

        _timeout_min = 30  # time in minutes before timeout warning
        self.min2msec = 60*1000  # conversion factor for min to msec

        self.timeout_timer = QtCore.QTimer()
        self.timeout_timer.setInterval(_timeout_min * self.min2msec)
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self.timeout_warning)

        status_handler.status_signal.connect(self.timeout_timer.start)

    # =========================================================================
    # User interface setup
    # =========================================================================

    def create_toolbar(self):
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
        self.toolbar.addWidget(self.tabWidget)

    def restore_geometry(self):
        x = CONF.get('Window', 'x')
        y = CONF.get('Window', 'y')
        w = CONF.get('Window', 'width')
        h = CONF.get('Window', 'height')

        self.setGeometry(x, y, w, h)

    def save_geometry(self):
        geo = self.geometry()
        CONF.set('Window', 'height', geo.height())
        CONF.set('Window', 'width', geo.width())
        CONF.set('Window', 'x', geo.x())
        CONF.set('Window', 'y', geo.y())

    def exit_(self):
        self.on_abort_clicked()
        self.on_clear_clicked()
        self.save_geometry()
        self.deleteLater()

    def closeEvent(self, event):
        self.exit_()

    def show_error(self, exc_info):
        title = 'CustomXepr Job Error'
        message = 'CustomXepr has encountered an error while executing a job.'
        msg = ErrorDialog(title, message, exc_info, parent=self)
        msg.exec_()

    def open_result_context_menu(self):
        """
        Context menu for items in resultQueueDisplay. Gives the options to
        delete the item, to plot it or to save it, depending on the implemented
        methods.
        """

        indexes = self.resultQueueDisplay.selectedIndexes()
        if not indexes:
            return

        i0, i1 = indexes[0].row(), indexes[-1].row()

        popup_menu = QtWidgets.QMenu()

        plot_action = popup_menu.addAction('Plot')
        save_action = popup_menu.addAction('Save...')
        delete_action = popup_menu.addAction('Delete')

        plot_action.setEnabled(False)
        save_action.setEnabled(False)

        if hasattr(self.result_queue.queue[i0], 'plot') and i0 == i1:
            plot_action.setEnabled(True)
        if hasattr(self.result_queue.queue[i0], 'save') and i0 == i1:
            save_action.setEnabled(True)

        action = popup_menu.exec_(QtGui.QCursor.pos())

        if action == 0:
            return
        elif action == delete_action:
            for i in range(i1, i0-1, -1):
                self.result_queue.remove_item(i)
                self.resultQueueModel.removeRow(i)
        elif action == save_action:
            prompt = 'Save as file'
            filename = 'untitled.txt'
            formats = 'Text file (*.txt)'
            filepath = QtWidgets.QFileDialog.getSaveFileName(self, prompt,
                                                             filename, formats)
            if len(filepath[0]) < 4:
                return
            self.result_queue.queue[i0].save(filepath[0])

        elif action == plot_action:
            self.result_queue.queue[i0].plot()

    def open_job_context_menu(self):
        """
        Context menu for items in jobQueueDisplay. Gives the option to
        delete the item.
        """
        indexes = self.jobQueueDisplay.selectedIndexes()
        if not indexes:
            return
        i0, i1 = indexes[0].row(), indexes[-1].row()

        popup_menu = QtWidgets.QMenu()
        delete_action = popup_menu.addAction('Delete')

        if i0 < self.job_queue.first_queued_index():
            delete_action.setEnabled(False)

        action = popup_menu.exec_(QtGui.QCursor.pos())

        if action == delete_action:
            for i in range(i1, i0-1, -1):
                self.job_queue.remove_item(i)

    def timeout_warning(self):
        """
        Issues a warning email if no status update has come in for the time
        specified in self.t_timeout.
        """
        if self.job_queue.has_running() > 0:
            logger.warning('No status update for %s min.' % self.t_timeout +
                           ' Please check on experiment')

# =============================================================================
# Functions to handle communication with job and result queues
# =============================================================================

    def on_job_added(self, index=-1):
        """
        Adds new entry to jobQueueDisplay.
        """
        exp = self.job_queue.queue[index]

        if len(exp.args) > 0 and exp.args[0] == self.customxepr:
            args = exp.args[1:]
        else:
            args = exp.args

        func_item = QtGui.QStandardItem(exp.func.__name__)
        args_item = QtGui.QStandardItem(str(args).lstrip('(').strip(',)'))
        kwargs_item = QtGui.QStandardItem(str(exp.kwargs).lstrip('{').strip(',}'))

        func_item.setIcon(self.icon_queued)

        self.jobQueueModel.appendRow([func_item, args_item, kwargs_item])

    def on_job_status_changed(self, index_status_tuple):
        """
        Updates status of top item in jobQueueDisplay.
        """
        index, status = index_status_tuple

        if status is Experiment.RUNNING:
            self.jobQueueModel.item(index).setIcon(self.icon_running)
        elif status is Experiment.ABORTED:
            self.jobQueueModel.item(index).setIcon(self.icon_aborted)
        elif status is Experiment.FAILED:
            self.jobQueueModel.item(index).setIcon(self.icon_failed)
        elif status is Experiment.FINISHED:
            self.jobQueueModel.item(index).setIcon(self.icon_finished)
        elif status is Experiment.QUEUED:
            self.jobQueueModel.item(index).setIcon(self.icon_queued)

        self.jobQueueDisplay.scrollTo(self.jobQueueModel.createIndex(index-3, 1),
                                      self.jobQueueDisplay.PositionAtTop)

    def on_job_removed(self, i):
        self.jobQueueModel.removeRow(i)

    def add_result(self, index=-1):
        """
        Adds new result to the resultQueueDisplay, tries to plot the result.
        The new result is added to the end of the resultQueueDisplay.
        """
        result = self.result_queue.queue[index]

        try:
            result_size = len(result)
        except TypeError:
            result_size = '--'

        if self.plotCheckBox.isChecked():
            try:
                result.plot()
            except AttributeError:
                pass

        rslt_type = QtGui.QStandardItem(type(result).__name__)
        rslt_size = QtGui.QStandardItem(str(result_size))
        rslt_value = QtGui.QStandardItem(str(result))

        self.resultQueueModel.appendRow([rslt_type, rslt_size, rslt_value])

    def on_result_pop(self, index=0):
        """
        Removes entry with index `i` from resultQueueDisplay (default: i = 1).
        """
        self.resultQueueModel.removeRow(index)

    def populate_jobs(self):
        """
        Gets all current items of job_queue and adds them to jobQueueDisplay.
        """
        for i in range(0, self.job_queue.qsize()):
            self.on_job_added(i)

    def populate_results(self):
        """
        Gets all current items of result_queue and adds them to
        resultQueueDisplay.
        """
        for i in range(0, self.result_queue.qsize()):
            self.add_result(i)

    def check_paused(self):
        """
        Checks if worker thread is running and updates the Run/Pause button
        accordingly.
        """
        if self.running.is_set():
            self.pauseButton.setText('Pause')
        else:
            self.pauseButton.setText('Resume')

    # =========================================================================
    # Button callbacks
    # =========================================================================

    def on_tune_clicked(self):
        """
        Schedules a tuning job if the ESR is connected.
        """

        self.customxepr.customtune()

        if self.job_queue.qsize('queued') > 0:
            logger.info('Tuning job added to the job queue.')

    def on_qvalue_clicked(self):
        """
        Schedules a Q-Value readout if the ESR is connected.
        """

        self.customxepr.getQValueCalc()

        if self.job_queue.qsize('queued') > 0:
            logger.info('Q-Value readout added to the job queue.')

    def on_clear_clicked(self):
        """
        Clears all pending jobs in job_queue.
        """
        while self.job_queue.has_queued():
            self.job_queue.remove_item(-1)
            self.jobQueueModel.removeRow(self.jobQueueModel.rowCount() - 1)

    def on_pause_clicked(self):
        """
        Pauses or resumes worker thread on button click.
        """
        if self.running.is_set():
            self.running.clear()
            self.pauseButton.setText('Resume')
            logger.status('PAUSED')
        else:
            self.running.set()
            self.pauseButton.setText('Pause')
            logger.status('IDLE')

    def on_abort_clicked(self):
        """
        Aborts a running job.
        """
        if self.job_queue.has_running() > 0:
            self.abort_event.set()
            self.abort_event_keithley.set()

    def on_log_clicked(self):
        """
        Opens directory with log files with current log file selected.
        """
        path = self.customxepr.log_file_dir

        if platform.system() == 'Darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])

    # =========================================================================
    # Callbacks and functions for CustomXepr settings adjustments
    # =========================================================================

    def set_email_list(self):
        """
        Gets the email list from the UI and updates it in CustomXepr.
        """
        # get string from lineEdit field
        address_string = self.lineEditEmailList.text()
        # convert string to list of strings
        address_list = address_string.split(',')
        # strip trailing spaces
        address_list = [x.strip() for x in address_list]
        # validate correct email address format
        for email in address_list:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                logger.info(email + ' is not a valid email address.')
                address_list = [x for x in address_list if (x is not email)]

        # send list to CustomXepr
        self.customxepr.notify_address = address_list

    def get_email_list(self):
        """
        Gets the email list from CustomXepr and updates it in the UI.
        """
        address_list = self.customxepr.notify_address
        if not self.lineEditEmailList.hasFocus():
            self.lineEditEmailList.setText(', '.join(address_list))

    def get_notification_level(self):
        """
        Checks the notification level for email handler and sets the respective
        checkButton to checked.
        """
        level = self.customxepr.email_handler_level
        if level == 40:
            self.radioButtonErrorMail.setChecked(True)
        elif level == 30:
            self.radioButtonWarningMail.setChecked(True)
        elif level == 20:
            self.radioButtonInfoMail.setChecked(True)
        elif level == 50:
            self.radioButtonNoMail.setChecked(True)

    def on_bg_clicked(self):
        """ Sets the email notification level to the selected level."""
        clicked_button = self.bG.checkedButton()
        if clicked_button == self.radioButtonErrorMail:
            self.customxepr.email_handler_level = 40
        elif clicked_button == self.radioButtonWarningMail:
            self.customxepr.email_handler_level = 30
        elif clicked_button == self.radioButtonInfoMail:
            self.customxepr.email_handler_level = 20
        elif clicked_button == self.radioButtonNoMail:
            self.customxepr.email_handler_level = 50

    def set_temperature_tolerance(self, value):
        self.customxepr.temperature_tolerance = value

    def set_t_settling(self, value):
        self.customxepr.temp_wait_time = value

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def t_timeout(self):
        """Gets the timeout limit in minutes from timeout_timer."""
        return self.timeout_timer.interval()/self.min2msec

    @t_timeout.setter
    def t_timeout(self, time_in_min):
        """ Sets the timeout limit in minutes in timeout_timer."""
        self.timeout_timer.setInterval(time_in_min * self.min2msec)


# =============================================================================
# About / Help Window
# =============================================================================

def classify_class_attrs(obj):
    """
    Patch classify_class_attrs from pydoc to ignore inherited attributes.
    """
    results = []
    for (name, kind, cls, value) in inspect.classify_class_attrs(obj):
        if inspect.isdatadescriptor(value):
            kind = 'data descriptor'
        if cls is obj:  # only append attributes defined in object
            results.append((name, kind, cls, value))
    return results


pydoc.classify_class_attrs = classify_class_attrs


class CustomHtmlDoc(pydoc.TextDoc):
    """
    Subclass of TextDoc which overrides string styling to basic HTML styling.
    """

    def bold(self, text):
        """Format a string in bold html instead of unicode."""
        return '<span style="font-weight:bold">%s</span>' % text

    def docclass(self, obj, name=None, mod=None, *ignored):
        text = pydoc.TextDoc.docclass(self, obj, name, mod, *ignored)
        wrap_style = '<body style="white-space: pre-wrap;"> %s </body>'
        return wrap_style % text


class AboutWindow(QtWidgets.QWidget, QtCore.QCoreApplication):
    """
    Prints version number, copyright info and help output from CustomXepr to a
    PyQt window.
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        # load user interface file
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'about_window.ui'), self)
        # set copyright text
        placeholder = self.labelCopyRight.text()
        self.labelCopyRight.setText(placeholder.format(__year__, __author__))
        # get help output in html format
        textdoc = CustomHtmlDoc()
        self.help_output = textdoc.docclass(CustomXepr)
        # print help output to scroll area of window
        self.textBrowser.setText(self.help_output)
        # set title string of window to CustomXepr version
        self.title_string = (CustomXepr.__name__ + ' ' + __version__)
        self.titleText.setText(self.title_string)
