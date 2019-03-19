# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
import os
import time
import logging
import logging.handlers
import operator
# noinspection PyCompatibility
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty
from threading import RLock, Event
from enum import Enum
import collections

from decorator import decorator
from qtpy import QtCore

from customxepr.main import PY2
from customxepr.config import CONF


logger = logging.getLogger('customxepr')


# ========================================================================================
# class to wrap queued function calls ("experiments") and provide metadata
# ========================================================================================

class ExpStatus(Enum):
    """
    Enumeration to hold experiment status.
    """
    QUEUED = object()
    RUNNING = object()
    ABORTED = object()
    FAILED = object()
    FINISHED = object()


class Experiment(object):
    """
    Class to hold a scheduled job / experiment and keep track of its
    status and result.

    :param func: Function or method to call when running experiment.
    :param args: Arguments for function call.
    :param kwargs: Keyword arguments for function call.

    :ivar result: Holds the result returned by `func` after successful job completion.
    """

    def __init__(self, func, args, kwargs):

        self.func = func
        self.args = args
        self.kwargs = kwargs

        self._status = ExpStatus.QUEUED
        self.result = None

        if PY2:
            self.func.__name__ = func.func_name

    @property
    def status(self):
        """
        Returns the status of the job.

        :returns: Experiment status of type :class:`ExpStatus`.
        """
        return self._status

    @status.setter
    def status(self, s):
        """
        Sets status of the job to `s`.

        :param s: Experiment status. Must be of type :class:`ExpStatus`.
        """
        if s not in ExpStatus:
            raise ValueError('Argument must be of type %s' % type(ExpStatus))
        else:
            self._status = s


# =============================================================================
# custom queue which emits PyQt signals on put and get
# =============================================================================

class SignalQueue(QtCore.QObject, Queue):
    """
    Custom queue that emits Qt signals if an item is added or removed. Inherits
    from :class:`queue.Queue` and provides a thread-safe method to remove items
    from the center of the queue.

    :cvar put_signal: Is emitted when an item is put into the queue.
    :cvar pop_signal: Is emitted when an item is popped from the queue.
    :cvar removed_signal: Is emitted when items are removed from the queue.
    """

    put_signal = QtCore.Signal()
    pop_signal = QtCore.Signal()
    removed_signal = QtCore.Signal(int, int)

    def __init__(self):
        QtCore.QObject.__init__(self)
        Queue.__init__(self)

    def _put(self, item):
        Queue._put(self, item)
        self.put_signal.emit()

    def _get(self):
        item = Queue._get(self)
        self.pop_signal.emit()
        return item

    def remove_item(self, i):
        """
        Removes item from the queue in a thread safe manner. Calls
        :meth:`task_done` when done.

        :param int i: Index of item to remove.
        """
        self.remove_items(i)

    def remove_items(self, i_start, i_end=None):
        """
        Removes the items from index `i_start` to `i_end` from the queue.
        Raises a :class:`ValueError` if the item belongs to a running or
        already completed job. Emits the :attr:`removed_signal` for
        every removed item. Calls :meth:`task_done` for every item removed.

        This call has O(n) performance with regards to the queue length and
        number of items to be removed.

        :param int i_start: Index of first item to remove.
        :param int i_end: Index of last item to remove (defaults to i_end = i_start).
        """

        with self.mutex:
            if i_end is None:
                i_end = i_start

            # convert negative indices to positive
            i0 = self.qsize() + i_start if i_start < 0 else i_start
            i1 = self.qsize() + i_end if i_end < 0 else i_end

            if not i0 <= i1:
                raise ValueError("'i_end' must be larger than or equal to 'i_start'.")
            else:
                new_items = [x for i, x in enumerate(self.queue) if i < i0 or i > i1]
                self.queue = collections.deque(new_items)

            n_items = i1 - i0 + 1

            self.removed_signal.emit(i0, n_items)

        for i in range(n_items):
            self.task_done()


# ========================================================================================
# custom queue for experiments where all history is kept
# ========================================================================================

class ExperimentQueue(QtCore.QObject):
    """
    Queue to hold all jobs: Pending, running and already completed. Items in
    this queue should be of type :class:`Experiment`.

    :cvar added_signal: Emitted when a new job is added to the queue.
    :cvar removed_signal: Emitted when a job is removed from the queue.
        Carriers the index of the job in :class:`ExperimentQueue`.
    :cvar status_changed_signal: Emitted when a job status changes, e.g.,
        from :class:`ExpStatus.QUEUED` to :class:`ExpStatus.RUNNING`. Carries
        a tuple holding the job index and status.
    """

    added_signal = QtCore.Signal()
    removed_signal = QtCore.Signal(int, int)
    status_changed_signal = QtCore.Signal(int, object)

    _lock = RLock()

    def __init__(self):
        super(self.__class__, self).__init__()
        self._queued = Queue()
        self._running = Queue(maxsize=1)
        self._history = Queue()

    @property
    def queue(self):
        """
        Returns list of all items in queue (queued, running, and in history).
        """
        with self._lock:
            return (list(self._history.queue) + list(self._running.queue) +
                    list(self._queued.queue))

    def put(self, exp):
        """
        Adds item `exp` to the end of the queue. Its status must be
        :class:`ExpStatus.QUEUED`. Emits the :attr:`added_signal` signal.
        """
        if not exp.status == ExpStatus.QUEUED:
            raise ValueError('Can only append experiments with status "QUEUED".')
        with self._lock:
            self._queued.put(exp)
            self.added_signal.emit()

    def next_job(self):
        """
        Returns the next item with status :class:`ExpStatus.QUEUED` and flags it as
        running. If there are no items with status :class:`ExpStatus.QUEUED`,
        :class:`queue.Empty` is raised. Emits the :attr:`status_changed_signal`
        with the item's index and its new status.
        """
        with self._lock:
            exp = self._queued.get_nowait()
            exp.status = ExpStatus.RUNNING
            self._running.put(exp)
            index = self.first_queued_index() - 1

            self.status_changed_signal.emit(index, exp.status)

        return exp

    def task_done(self, exit_status, result=None):
        """
        Call to inform the Experiment queue that a task is completed. Changes
        the corresponding item's status to `exit_status` and its result to `result`.
        Emits the `status_changed_signal` with the item's index and its new status.

        :param exit_status: Status of the completed job, i.e., :class:`ExpStatus.ABORTED`.
        :param result: Return value of job, if available.
        """

        with self._lock:
            exp = self._running.get_nowait()
            exp.status = exit_status
            exp.result = result
            self._history.put(exp)
            index = self._history.qsize() - 1

            self.status_changed_signal.emit(index, exit_status)

    def remove_item(self, i):
        """
        Removes the item with index `i` from the queue. Raises a :class:`ValueError`
        if the item belongs to a running or already completed job. Emits the
        :attr:`removed_signal` carrying the index.

        :param int i: Index of item to remove.
        """
        self.remove_items(i)

    def remove_items(self, i_start, i_end=None):
        """
        Removes the items from index `i_start` to `i_end` from the queue.
        Raises a :class:`ValueError` if the item belongs to a running or
        already completed job. Emits the :attr:`removed_signal` for
        every removed item.

        This call has O(n) performance with regards to the queue length and
        number of items to be removed.

        :param int i_start: Index of first item to remove.
        :param int i_end: Index of last item to remove (defaults to i_end = i_start).
        """

        if i_end is None:
            i_end = i_start

        with self._lock:
            # convert negative indices to positive
            i_start = self.qsize() + i_start if i_start < 0 else i_start
            i_end = self.qsize() + i_end if i_end < 0 else i_end

            # convert to index of self._queued.queue
            i0 = i_start - self.first_queued_index()
            i1 = i_end - self.first_queued_index()

            if i0 < 0:
                raise ValueError('Only queued experiments can be removed.')
            elif not i0 <= i1:
                raise ValueError("'i_end' must be larger than or equal to 'i_start'.")
            else:
                new_items = [x for i, x in enumerate(self._queued.queue) if i < i0 or i > i1]
                self._queued.queue = collections.deque(new_items)

            n_items = i_end - i_start + 1
            self.removed_signal.emit(i_start, n_items)

    def clear(self):
        """
        Removes all queued experiments at once.
        """
        with self._lock:
            self.removed_signal.emit(self.first_queued_index(), self._queued.qsize())
            self._queued.queue.clear()

    def has_running(self):
        return self._running.qsize() > 0

    def has_queued(self):
        return self._queued.qsize() > 0

    def has_history(self):
        return self._history.qsize() > 0

    def first_queued_index(self):
        with self._lock:
            return self._history.qsize() + self._running.qsize()

    def qsize(self, status=None):
        """
        Return the approximate number of jobs with given status (not reliable!).

        :param status: Can be 'queued', 'running', 'history' or `None`. If `None`, the
            full queue size will be returned.
        """
        with self._lock:
            return self._qsize(status)

    def _qsize(self, status):
        if status is 'queued':
            return self._queued.qsize()
        elif status is 'running':
            return self._running.qsize()
        elif status is 'history':
            return self._history.qsize()
        else:
            return self._history.qsize() + self._running.qsize() + self._queued.qsize()


# ========================================================================================
# worker that gets function / method calls from queue and carriers them out
# ========================================================================================

class Worker(QtCore.QObject):
    """
    Worker that gets all method calls with args from :attr:`job_q` and executes
    them. Results are then stored in the :attr:`result_q`.

    :param job_q: Queue with jobs to be performed.
    :param result_q: Queue with results from completed jobs.

    :cvar running: Event that causes the worker to pause between jobs if set.
    :cvar abort: Event that tells a job to abort if set. After a job has
        been aborted, Worker will clear the :attr:`abort` event.
    """

    running = Event()

    def __init__(self, job_q, result_q, abort_events):
        super(self.__class__, self).__init__(None)
        self.job_q = job_q
        self.result_q = result_q
        self.abort_events = abort_events

    def abort_is_set(self):
        is_set = operator.methodcaller('is_set')
        return any(map(is_set, self.abort_events))

    def clear_abort(self):
        for event in self.abort_events:
            event.clear()

    def process(self):
        while True:
            time.sleep(0.1)

            if not self.running.is_set():
                logger.status('PAUSED')

            self.running.wait()

            try:
                exp = self.job_q.next_job()  # get next job
            except Empty:
                pass
            else:
                # noinspection PyBroadException
                try:
                    result = exp.func(*exp.args, **exp.kwargs)  # run the job
                except Exception:  # log exception and pause execution of jobs
                    logger.exception('Job error')
                    self.job_q.task_done(ExpStatus.FAILED, result=None)
                    self.running.clear()
                    logger.status('PAUSED')
                else:
                    if result is not None:
                        self.result_q.put(result)

                    if self.abort_is_set():
                        exit_status = ExpStatus.ABORTED
                        self.clear_abort()
                    else:
                        exit_status = ExpStatus.FINISHED

                    self.job_q.task_done(exit_status, result)
                    logger.status('IDLE')


# noinspection PyUnresolvedReferences
class Manager(QtCore.QObject):
    """
    :class:`Manager` provides a high level interface for the scheduling and executing
    experiments. All queued experiments will be run in a background thread and
    :class:`Manager` provides methods to pause, resume and abort the execution of
    experiments. All results will be kept in the :cvar:`result_queue` for later retrieval.

    Function calls can be queued as experiments by decorating the function
    with the :func:`manager.queued_exec` decorator:

    >>> import time
    >>> from customxepr.manager import Manager, queued_exec
    >>> manager = Manager()

    >>> # create test function
    >>> @queued_exec(manager.job_queue)
    ... def decorated_test_func(*args):
    ...     # do something
    ...     for i in range(0, 10):
    ...         time.sleep(1)
    ...         # check for requested aborts
    ...         if manager.abort.is_set()
    ...             break
    ...     return args  # return input arguments

    >>> # run the function: this will return immediately
    >>> decorated_test_func('test succeeded')

    The result returned by `test_func` can be retrieved from the result queue as follows:

    >>> result = manager.result_queue.get()  # blocks until result is available
    >>> print(result)
    test succeeded

    Alternatively, it is possible to manually create an experiment from a function call
    and queue it for processing as follows:

    >>> import time
    >>> from customxepr.manager import Manager, Experiment
    >>> manager = Manager()

    >>> # create test function
    >>> def stand_alone_test_func(*args):
    ...     # do something
    ...     for i in range(0, 10):
    ...         time.sleep(1)
    ...         # check for requested aborts
    ...         if manager.abort.is_set()
    ...             break
    ...     return args  # return input arguments

    >>> # create an experiment from function
    >>> exp = Experiment(stand_alone_test_func, args=['test succeeded',], kwargs={})
    >>> # queue the experiment
    >>> manager.job_queue.put(exp)

    This class provides an event :cvar:`abort` which can queried periodically by any
    function to see if it should abort prematurely. Alternatively, functions and methods
    can provide their own abort events and register them with the manager as follows:

    >>> from threading import Event
    >>> abort_event = Event()
    >>> # register the event with the manager instance
    >>> manager.abort_events = [abort_event]

    The manager will automatically set the status of an experiment to ABORTED if it
    finishes while an abort event is set and clear all abort events afterwards.

    :cvar job_queue: An instance of :class:`ExperimentQueue` holding all queued and
        finished experiments.
    :cvar result_queue: A queue holding all results.
    :cvar abort: A generic event which can be used in long-running experiments to check
        if they should be aborted.
    """

    job_queue = ExperimentQueue()
    result_queue = SignalQueue()

    abort = Event()
    _abort_events = [abort]

    def __init__(self):
        super(self.__class__, self).__init__()

        # create background thread to process all executions in queue
        self.worker_thread = QtCore.QThread()
        self.worker_thread.setObjectName('CustomXeprWorkerThread')
        self.worker = Worker(self.job_queue, self.result_queue, self._abort_events)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.process)
        self.worker_thread.start()
        self.worker.running.set()

        self.running = self.worker.running
        self._abort_events = []

        # set up logging functionality
        self._setup_root_logger()

    # ====================================================================================
    # job execution management
    # ====================================================================================

    @property
    def abort_events(self):
        """
        List of abort events to be used when calling :func:`abort_job`. This is
        in addition to :attr:`abort` which can be checked periodically by all experiments
        passed to the worker. All abort events will be cleared after the a job has been
        aborted.
        """
        return self._abort_events[1:]

    @abort_events.setter
    def abort_events(self, events):
        """
        Setter for :attr:`set_abort_events`.
        """
        self._abort_events = [self.abort] + events

    def pause_worker(self):
        """
        Pauses the execution of jobs after the current job has been completed.
        """
        self.worker.running.clear()
        logger.status('PAUSED')

    def resume_worker(self):
        """
        Resumes the execution of jobs.
        """
        self.worker.running.set()
        logger.status('IDLE')

    def abort_job(self):
        """
        Aborts the current job and continues with the next.
        """
        if self.job_queue.has_running() > 0:
            self.abort.set()

        for event in self._abort_events:
            event.set()

    def clear_all_jobs(self):
        """
        Clears all pending jobs in :attr:`job_queue`.
        """
        self.job_queue.clear()

    # ====================================================================================
    # logging facilities
    # ====================================================================================

    @staticmethod
    def _setup_root_logger():

        # Set up new STATUS level
        root_logger = logging.getLogger()

        logging.STATUS = 15
        logging.addLevelName(logging.STATUS, 'STATUS')
        for l in [logger, root_logger]:
            l.setLevel(logging.STATUS)
            setattr(l, 'status', lambda message,
                    *args: logger._log(logging.STATUS, message, args))

        # find all email handlers
        eh = [x for x in root_logger.handlers if type(x) == logging.handlers.SMTPHandler]
        # find all file handlers
        fh = [x for x in root_logger.handlers if type(x) == logging.FileHandler]
        # find all stream handlers
        sh = [x for x in root_logger.handlers if type(x) == logging.StreamHandler]

        # define standard format of logging messages
        f = logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)s: ' +
                                  '%(message)s', datefmt='%H:%M')

        # remove stream handlers
        for handler in sh:
            root_logger.handlers.remove(handler)

        # add email handler if not present
        if len(eh) == 0:
            # create and add email handler

            email_handler = logging.handlers.SMTPHandler(
                'localhost', 'ss2151@cam.ac.uk', CONF.get('CustomXepr', 'notify_address'),
                'Xepr logger')
            email_handler.setFormatter(f)
            email_handler.setLevel(CONF.get('CustomXepr', 'email_handler_level'))

            root_logger.addHandler(email_handler)

        # add file handler if not present
        if len(fh) == 0:
            home_path = os.path.expanduser('~')
            logging_path = os.path.join(home_path, '.CustomXepr', 'LOG_FILES')

            if not os.path.exists(logging_path):
                os.makedirs(logging_path)

            log_file = os.path.join(logging_path, 'root_logger '
                                    + time.strftime("%Y-%m-%d_%H-%M-%S") + '.txt')
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(f)
            file_handler.setLevel(logging.INFO)
            root_logger.addHandler(file_handler)

    @property
    def notify_address(self):
        """ List of addresses for email notifications."""
        # get root logger
        root_logger = logging.getLogger()
        # find all email handlers (there should be only one)
        eh = [x for x in root_logger.handlers if type(x) == logging.handlers.SMTPHandler]

        if len(eh) == 0:
            logging.warning('No email handler could be found.')

        elif len(eh) > 0:
            # get emails from all handlers
            email_list = []
            for handler in eh:
                email_list += handler.toaddrs
            # remove duplicates and return
            return list(set(email_list))

    @notify_address.setter
    def notify_address(self, email_list):
        """Setter: Address list for email notifications."""
        # get root logger
        root_logger = logging.getLogger()
        # find all email handlers (there should be only one)
        eh = [x for x in root_logger.handlers if type(x) == logging.handlers.SMTPHandler]

        if len(eh) == 0:
            logging.warning('No email handler could be found.')
        elif len(eh) > 0:
            for handler in eh:
                handler.toaddrs = email_list

        email_list_str = ', '.join(email_list)
        logger.info('Email notifications will be sent to ' + email_list_str + '.')

        # update conf file
        CONF.set('CustomXepr', 'notify_address', email_list)

    @property
    def log_file_dir(self):
        """Directory for log files. Defaults to '~/.CustomXepr'."""
        # get root logger
        root_log = logging.getLogger()
        # find all email handlers (there should be only one)
        fh = [x for x in root_log.handlers if type(x) == logging.FileHandler]

        if len(fh) == 0:
            logger.warning('No file handler could be found.')
        else:
            file_name = fh[0].baseFilename
            return os.path.dirname(file_name)

    @property
    def email_handler_level(self):
        """
        Logging level for email notifications. Defaults to :class:`logging.WARNING`.
        """
        # get root logger
        root_logger = logging.getLogger()
        # find all email handlers (there should be only one)
        eh = [x for x in root_logger.handlers if type(x) == logging.handlers.SMTPHandler]

        if len(eh) == 0:
            logger.warning('No email handler could be found.')
        else:
            return eh[0].level

    @email_handler_level.setter
    def email_handler_level(self, level=logging.WARNING):
        """Setter: Logging level for email notifications."""
        # get root logger
        root_logger = logging.getLogger()
        # find all email handlers (there should be only one)
        eh = [x for x in root_logger.handlers if type(x) == logging.handlers.SMTPHandler]

        if len(eh) == 0:
            logger.warning('No email handler could be found.')
        else:
            eh[0].setLevel(level)
        # update conf file
        CONF.set('CustomXepr', 'email_handler_level', level)


# ========================================================================================
# queued execution decorator which dumps a function / method call into a queue
# ========================================================================================

def queued_exec(queue):
    """
    Decorator that puts a call to a wrapped function into a
    queue instead of executing it. Items in the queue will be
    of type :class:`Experiment`.

    :param queue: Queue to put function calls.
    """
    @decorator
    def put_to_queue(func, *args, **kwargs):
        exp = Experiment(func, args, kwargs)
        queue.put(exp)

    return put_to_queue
