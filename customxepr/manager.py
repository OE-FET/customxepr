#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""

import sys
import time
import logging
# noinspection PyCompatibility
from queue import Queue, Empty
from threading import RLock, Event
from enum import Enum

from decorator import decorator
from qtpy import QtCore

PY2 = sys.version[0] == '2'
logger = logging.getLogger('customxepr.main')


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
    :cvar pop_signal: Is emitted when an item is removed from the queue.
    """

    put_signal = QtCore.Signal()
    pop_signal = QtCore.Signal()

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
        Removed item from the queue in thread safe manner. Calls
        :func:`task_done` when done.

        :param int i: Index of item to remove.
        """
        with self.mutex:
            del self.queue[i]
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
    removed_signal = QtCore.Signal(int)
    status_changed_signal = QtCore.Signal(tuple)

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

        self.status_changed_signal.emit((index, exp.status))
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

        self.status_changed_signal.emit((index, exit_status))

    def remove_item(self, i):
        """
        Removes the item with index `i` from the queue. Raises a :class:`ValueError`
        if the item belongs to a running or already completed job. Emits the
        :attr:`removed_signal` carrying the index.

        :param int i: Index of item to remove.
        """
        with self._lock:
            if i < 0:
                # convert to positive index if negative
                i = self.qsize() + i

            # convert to index of self._queued.queue
            index = i - self.first_queued_index()

            if index < 0:
                raise ValueError('Only queued experiments can be removed.')
            else:
                del self._queued.queue[index]

        self.removed_signal.emit(i)

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
    abort = Event()

    def __init__(self, job_q, result_q):
        super(self.__class__, self).__init__(None)
        self.job_q = job_q
        self.result_q = result_q

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
                    logger.exception('EXCEPTION')
                    self.job_q.task_done(ExpStatus.FAILED, result=None)
                    self.running.clear()
                    logger.status('PAUSED')
                else:
                    if result is not None:
                        self.result_q.put(result)

                    if self.abort.is_set():
                        exit_status = ExpStatus.ABORTED
                        self.abort.clear()
                    else:
                        exit_status = ExpStatus.FINISHED

                    self.job_q.task_done(exit_status, result)
                    logger.status('IDLE')


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
