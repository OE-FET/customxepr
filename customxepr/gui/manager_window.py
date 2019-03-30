# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 11:03:57 2016

@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import
import sys
import os
import logging
import platform
import subprocess
import re
import inspect
import webbrowser
from qtpy import QtCore, QtWidgets, QtGui, uic

# local imports
from customxepr.gui.about_window import AboutWindow
from customxepr.gui.update_dialog import UpdateWindow
from customxepr.gui.error_dialog import ErrorDialog
from customxepr.main import __version__, __year__, __author__, __url__
from customxepr.manager import ExpStatus
from customxepr.config.main import CONF
from customxepr.gui.notify import Notipy


PY2 = sys.version[0] == '2'
_root = os.path.dirname(os.path.realpath(__file__))


# ========================================================================================
# Set up logging handlers for STATUS, INFO and ERROR messages
# ========================================================================================


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
    logged event. The signal will be connected to "Status" field of the GUI.
    """
    status_signal = QtCore.Signal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QtCore.QObject.__init__(self)

    def emit(self, record):
        # format logging record
        self.format(record)
        # emit logging record as signal
        self.status_signal.emit('Status: %s' % record.message)


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

# add handlers to customxepr logger
logger = logging.getLogger('customxepr')
logger.addHandler(status_handler)
logger.addHandler(info_handler)
logger.addHandler(error_handler)


# ========================================================================================
# Define JobStatusApp class
# ========================================================================================

# noinspection PyArgumentList,PyCallByClass
class ManagerApp(QtWidgets.QMainWindow):

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

    This class requires a :class:`main.CustomXepr` instance as input.

    """

    MAX_JOB_HISTORY_LENGTH = 1
    QUIT_ON_CLOSE = False

    def __init__(self, manager):
        # noinspection PyArgumentList
        QtWidgets.QMainWindow.__init__(self)

        # get input arguments
        self.manager = manager
        self.job_queue = self.manager.job_queue
        self.result_queue = self.manager.result_queue

        # ================================================================================
        # Set-up the UI
        # ================================================================================

        # load layout file, setup toolbar on macOS
        if platform.system() == 'Darwin':
            layout_file = 'manager_window_macos.ui'
        else:
            layout_file = 'manager_window_linux.ui'

        uic.loadUi(os.path.join(_root, layout_file), self)

        if platform.system() == 'Darwin':
            # create unified toolbar
            self.toolbar = QtWidgets.QToolBar(self)
            self.create_toolbar()

        cpr_text = '© {0}, {1}.'.format(__year__, __author__)
        self.labelCopyRight.setText(cpr_text)
        if not platform.system() == 'Darwin':
            # every tab has its own label if not on macOS
            self.labelCopyRight_2.setText(cpr_text)
            self.labelCopyRight_3.setText(cpr_text)

        # create about window and update window
        self.aboutWindow = AboutWindow()

        # load resources
        self.icon_queued = QtGui.QIcon(_root + '/resources/queued@2x.icns')
        self.icon_running = QtGui.QIcon(_root + '/resources/running@2x.icns')
        self.icon_aborted = QtGui.QIcon(_root + '/resources/aborted@2x.icns')
        self.icon_failed = QtGui.QIcon(_root + '/resources/failed@2x.icns')
        self.icon_finished = QtGui.QIcon(_root + '/resources/finished@2x.icns')

        # assign menu bar actions
        self.action_About.triggered.connect(self.aboutWindow.show)
        self.actionCustomXepr_Help.triggered.connect(lambda: webbrowser.open_new(__url__))
        self.actionShow_log_files.triggered.connect(self.on_log_clicked)
        self.action_Exit.triggered.connect(self.exit_)

        if not os.popen('Xepr --apipath').read() == '':
            url = 'file://' + os.popen('Xepr --apipath').read() + '/docs/XeprAPI.html'
            self.actionXeprAPI_Help.triggered.connect(lambda: webbrowser.open_new(url))
        else:
            self.actionXeprAPI_Help.setEnabled(False)

        # restore last position and size
        self.restore_geometry()

        # ================================================================================
        # Updated UI to reflect Manager status
        # ================================================================================

        # check status of worker thread (Paused or Running) and adjust buttons
        self.check_paused()

        # get states of checkboxes, text edits, etc
        self.get_email_list()
        self.get_notification_level()
        self.plotCheckBox.setChecked(CONF.get('Window', 'auto_plot_results'))

        # create data models for message log, job queue and result queue
        self.messageLogModel = info_handler.model
        self.jobQueueModel = QtGui.QStandardItemModel(0, 2)
        self.resultQueueModel = QtGui.QStandardItemModel(0, 3)

        h0 = ['Function', 'Arguments']
        h1 = ['Type', 'Size', 'Value']
        h2 = ['Time', 'Level', 'Message']

        self.jobQueueModel.setHorizontalHeaderLabels(h0)
        self.resultQueueModel.setHorizontalHeaderLabels(h1)
        self.messageLogModel.setHorizontalHeaderLabels(h2)

        # add models to views
        self.jobQueueDisplay.setModel(self.jobQueueModel)
        self.resultQueueDisplay.setModel(self.resultQueueModel)
        self.messageLogDisplay.setModel(self.messageLogModel)

        # populate models with queue elements
        self.populate_results()
        self.populate_jobs()

        # set context menus for job_queue and result_queue items
        self.resultQueueDisplay.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.jobQueueDisplay.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # ================================================================================
        # Connect signals, slots, and callbacks
        # ================================================================================

        # cannot call Qt slots directly from PySignal in Python 2
        def on_result_rows_removed(i0, n_items):
            self.resultQueueModel.removeRows(i0, n_items)

        def on_job_rows_removed(i0, n_items):
            self.jobQueueModel.removeRows(i0, n_items)

        # update views when items are added to or removed from queues
        self.result_queue.put_signal.connect(self.add_result)
        self.result_queue.pop_signal.connect(self.on_result_pop)
        self.result_queue.removed_signal.connect(on_result_rows_removed)

        self.job_queue.added_signal.connect(self.on_job_added)
        self.job_queue.removed_signal.connect(self.on_job_rows_removed)
        self.job_queue.status_changed_signal.connect(on_job_status_changed)

        # perform various UI updates after status change
        status_handler.status_signal.connect(self.statusField.setText)
        if not platform.system() == 'Darwin':
            # every tab has its own field if not on macOS
            status_handler.status_signal.connect(self.statusField_2.setText)
            status_handler.status_signal.connect(self.statusField_3.setText)
        status_handler.status_signal.connect(self.check_paused)
        status_handler.status_signal.connect(self.get_email_list)

        # notify user of any errors in job execution with a message box
        error_handler.error_signal.connect(self.show_error)

        # connect context menu callbacks
        self.resultQueueDisplay.customContextMenuRequested.connect(self.open_result_context_menu)
        self.jobQueueDisplay.customContextMenuRequested.connect(self.open_job_context_menu)

        # plot result on double click
        self.resultQueueDisplay.doubleClicked.connect(self.on_result_double_clicked)

        # connect job control buttons
        self.pauseButton.clicked.connect(self.on_pause_clicked)
        self.abortButton.clicked.connect(self.manager.abort_job)
        self.clearButton.clicked.connect(self.manager.clear_all_jobs)

        # connect log control settings
        self.lineEditEmailList.returnPressed.connect(self.set_email_list)
        self.bG.buttonClicked['int'].connect(self.on_bg_clicked)
        self.plotCheckBox.toggled.connect(self.on_plot_checkbox_toggeled)

        # Universal timeout:
        # Send an email notification if there is no status update for 30 min.
        _timeout_min = 30
        self._min2msec = 60 * 1000

        self.timeout_timer = QtCore.QTimer()
        self.timeout_timer.setInterval(_timeout_min * self._min2msec)
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self.timeout_warning)

        status_handler.status_signal.connect(self.timeout_timer.start)

        # ================================================================================
        # Inform user of changes
        # ================================================================================

        if self.is_updated():
            self.updateWindow = UpdateWindow()
            QtCore.QTimer.singleShot(5000, self.updateWindow.exec_)

    # ====================================================================================
    # User interface setup
    # ====================================================================================

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
        self.manager.clear_all_jobs()
        self.manager.abort_job()
        self.save_geometry()
        self.deleteLater()

    def closeEvent(self, event):
        if self.QUIT_ON_CLOSE:
            self.exit_()
        else:
            self.hide()

    def show_error(self, exc_info):
        title = 'CustomXepr Job Error'
        message = 'CustomXepr has encountered an error while executing a job.'
        msg = ErrorDialog(title, message, exc_info, parent=self)
        msg.exec_()

    def on_result_double_clicked(self, index):
        """Plot item if double clicked."""
        i = index.row()
        try:
            self.result_queue.queue[i].plot()
        except AttributeError:
            pass

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
            self.result_queue.remove_items(i0, i1)
        elif action == save_action:
            prompt = 'Save as file'
            filename = 'untitled.txt'
            filepath = QtWidgets.QFileDialog.getSaveFileName(None, prompt, filename)
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
            self.job_queue.remove_items(i0, i1)

    def timeout_warning(self):
        """
        Issues a warning email if no status update has come in for the time
        specified in self.t_timeout.
        """
        if self.job_queue.has_running() > 0:
            logger.warning('No status update for %i min.' % self.t_timeout +
                           ' Please check on experiment')

    @staticmethod
    def is_updated():
        old_version = CONF.get('Version', 'old_version')

        if old_version in [__version__, None]:
            return False
        else:
            CONF.set('Version', 'old_version', __version__)
            return True

# ========================================================================================
# Functions to handle communication with job and result queues
# ========================================================================================

    @staticmethod
    def _trunc_str(string, max_length=13):
        """
        Returns string truncated to given length.

        :param str string: String to truncate.
        :param int max_length: Maximum number of characters in truncated string.
            Must be >= 5.
        :returns: Truncated string of length `max_length`.
        :rtype: str
        """
        if max_length < 5:
            raise ValueError("'max_length' must be larger than 4.")
        ll = max_length - 4
        return string[:ll] + (string[ll:] and '...' + string[-1])

    def _trunc_str_list(self, string_list, max_total_len=150, min_item_len=13):
        """
        Tries to truncate strings in list until total length is smaller than
        `max_total_len`. Starts with the last string in list and moves backward.
        No individual string will be truncated shorter than `min_item_len`,
        even if `max_total_len` must be exceeded.

        :param list string_list: List of strings to truncate
        :param int max_total_len: Maximum number of characters in truncated
            string list (default = 150).
        :param int min_item_len: Minimum number of characters per string (default = 13).
        :returns: List of truncated strings.
        :rtype: list
        """
        overlength = sum(len(s) for s in string_list) - max_total_len
        i = len(string_list) - 1

        while overlength > 0 and i > -1:
            keep = max(len(string_list[i]) - overlength, min_item_len)
            string_list[i] = self._trunc_str(string_list[i], max_length=keep)

            overlength = sum(len(s) for s in string_list) - max_total_len
            i -= 1

        return string_list

    def on_job_added(self, index=-1):
        """
        Adds new entry to jobQueueDisplay.
        """

        exp = self.job_queue.queue[index]

        if PY2:
            argspec = inspect.getargspec(exp.func)
        else:
            argspec = inspect.getfullargspec(exp.func)

        argument_strings = [v for v in list(argspec.args) + list(exp.kwargs.keys())]
        value_strings = [repr(v) for v in list(exp.args) + list(exp.kwargs.values())]
        value_strings = self._trunc_str_list(value_strings)

        str_list = ['%s=%s' % (n, v) for n, v in zip(argument_strings, value_strings)]

        if argspec.args[0] == 'self':
            str_list.pop(0)

        func_item = QtGui.QStandardItem(exp.func.__name__)
        args_item = QtGui.QStandardItem(', '.join(str_list))

        func_item.setIcon(self.icon_queued)

        self.jobQueueModel.appendRow([func_item, args_item])

    def on_job_status_changed(self, index, status):
        """
        Updates status of top item in jobQueueDisplay.
        """

        if status is ExpStatus.RUNNING:
            self.jobQueueModel.item(index).setIcon(self.icon_running)
        elif status is ExpStatus.ABORTED:
            self.jobQueueModel.item(index).setIcon(self.icon_aborted)
        elif status is ExpStatus.FAILED:
            self.jobQueueModel.item(index).setIcon(self.icon_failed)
        elif status is ExpStatus.FINISHED:
            self.jobQueueModel.item(index).setIcon(self.icon_finished)
        elif status is ExpStatus.QUEUED:
            self.jobQueueModel.item(index).setIcon(self.icon_queued)

        self.jobQueueDisplay.scrollTo(self.jobQueueModel.createIndex(index-3, 1),
                                      self.jobQueueDisplay.PositionAtTop)

    def add_result(self, index=-1):
        """
        Adds new result to the :attr:`resultQueueDisplay` and tries to plot the result.
        The new result is added to the end of :attr:`resultQueueDisplay`.
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
        Removes entry with index ``i`` from :attr:`resultQueueDisplay` (default: i = 1).
        """
        self.resultQueueModel.removeRow(index)

    def populate_jobs(self):
        """
        Gets all current items of :attr:`job_queue` and adds them to
        :attr:`jobQueueDisplay`.
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
        if self.manager.worker.running.is_set():
            self.pauseButton.setText('Pause')
        else:
            self.pauseButton.setText('Resume')

    # ====================================================================================
    # Button callbacks
    # ====================================================================================

    def on_pause_clicked(self):
        """
        Pauses or resumes worker thread on button click.
        """
        if self.manager.worker.running.is_set():
            self.manager.pause_worker()
        else:
            self.manager.resume_worker()

    def on_log_clicked(self):
        """
        Opens directory with log files with current log file selected.
        """
        path = self.manager.log_file_dir

        if platform.system() == 'Darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])

    @staticmethod
    def on_plot_checkbox_toggeled(checked):
        CONF.set('Window', 'auto_plot_results', checked)

    # ====================================================================================
    # Callbacks and functions for CustomXepr settings adjustments
    # ====================================================================================

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
        self.manager.notify_address = address_list

    def get_email_list(self):
        """
        Gets the email list from CustomXepr and updates it in the UI.
        """
        address_list = self.manager.notify_address
        if not self.lineEditEmailList.hasFocus():
            self.lineEditEmailList.setText(', '.join(address_list))

    def get_notification_level(self):
        """
        Checks the notification level for email handler and sets the respective
        checkButton to checked.
        """
        level = self.manager.email_handler_level
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
            self.manager.email_handler_level = 40
        elif clicked_button == self.radioButtonWarningMail:
            self.manager.email_handler_level = 30
        elif clicked_button == self.radioButtonInfoMail:
            self.manager.email_handler_level = 20
        elif clicked_button == self.radioButtonNoMail:
            self.manager.email_handler_level = 50

    # ====================================================================================
    # Properties
    # ====================================================================================

    @property
    def t_timeout(self):
        """Gets the timeout limit in minutes from timeout_timer."""
        return self.timeout_timer.interval()/self._min2msec

    @t_timeout.setter
    def t_timeout(self, time_in_min):
        """ Sets the timeout limit in minutes in timeout_timer."""
        self.timeout_timer.setInterval(time_in_min * self._min2msec)
