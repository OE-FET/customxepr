#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  23 14:03:29 2019

@author: SamSchott

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""

import sys
import time
import logging
# noinspection PyCompatibility
from queue import Queue, Empty
from threading import RLock
from decorator import decorator
from qtpy import QtCore

PY2 = sys.version[0] == '2'
logger = logging.getLogger('customxepr.main')


# =============================================================================
# class to wrap queued function calls and provide metadata
# =============================================================================

class Experiment(object):

    QUEUED = 0
    RUNNING = 1
    ABORTED = 2
    FAILED = 3
    FINISHED = 4

    def __init__(self, func, args, kwargs):

        self.func = func
        self.args = args
        self.kwargs = kwargs

        self._status = self.QUEUED
        self.result = None

        if PY2:
            self.func.__name__ = func.func_name

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s):
        if s not in [self.QUEUED, self.RUNNING, self.ABORTED, self.FAILED, self.FINISHED]:
            raise ValueError('Invalid experiment status.')
        else:
            self._status = s


# =============================================================================
# custom queue which emits PyQt signals on put and get
# =============================================================================

class SignalQueue(QtCore.QObject, Queue):
    """
    Custom queue that emits Qt signals if an item is added or removed and if
    `task_done` is called.

    :cvar put_signal: Is emitted when an item is put into the queue.
    :cvar pop_signal: Is emitted when an item is removed from the queue.
    """

    put_signal = QtCore.Signal()
    pop_signal = QtCore.Signal()
    task_done_signal = QtCore.Signal(str)

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
        with self.mutex:
            del self.queue[i]
        self.task_done()


# =============================================================================
# custom queue for experiments where all history is kept
# =============================================================================

class ExperimentQueue(QtCore.QObject):

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
        with self._lock:
            return list(self._history.queue) + list(self._running.queue) + list(self._queued.queue)

    def put(self, exp):
        if not exp.status == Experiment.QUEUED:
            raise ValueError('Can only append experiments with status "QUEUED".')
        with self._lock:
            self._queued.put(exp)
        self.added_signal.emit()

    def next_job(self):
        with self._lock:
            exp = self._queued.get_nowait()
            exp.status = Experiment.RUNNING
            self._running.put(exp)
            index = self.first_queued_index() - 1

        self.status_changed_signal.emit((index, exp.status))
        return exp

    def task_done(self, exit_status, result):
        with self._lock:
            exp = self._running.get_nowait()
            exp.status = exit_status
            exp.result = result
            self._history.put(exp)
            index = self._history.qsize() - 1

        self.status_changed_signal.emit((index, exit_status))

    def remove_item(self, i):
        index = i - self.first_queued_index()
        with self._lock:
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

        Args:
            status: Can be 'queued', 'running', or 'history'. Otherwise, the full
            queue size will be returned.
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


# =============================================================================
# worker that gets function / method calls from queue and carriers them out
# =============================================================================

class Worker(QtCore.QObject):
    """
    Worker that gets all method calls with args from job_q and executes them.
    Results are then stored in the result_q.

    Args:
        job_q: Queue with jobs to be performed.
        result_q:  Queue with results from completed jobs.
        running: Event that causes the worker to pause between jobs if set.
        abort: Event that tells a job to abort if set. After a job has
            been aborted, Worker will clear the `abort` event.
    """

    def __init__(self, job_q, result_q, running, abort):
        super(self.__class__, self).__init__(None)
        self.job_q = job_q
        self.result_q = result_q
        self.running = running
        self.abort = abort

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
                    self.job_q.task_done(exp.FAILED, result=None)
                    self.running.clear()
                    logger.status('PAUSED')
                else:
                    if result is not None:
                        self.result_q.put(result)

                    if self.abort.is_set():
                        exit_status = exp.ABORTED
                        self.abort.clear()
                    else:
                        exit_status = exp.FINISHED

                    self.job_q.task_done(exit_status, result)
                    logger.status('IDLE')


# =============================================================================
# queued execution decorator which dumps a function / method call into a queue
# =============================================================================

def queued_exec(queue):
    """
    Wrapper that ads a method call with *args and **kwargs to a queue instead
    of executing in the main thread.
    """
    @decorator
    def put_to_queue(func, *args, **kwargs):
        exp = Experiment(func, args, kwargs)
        queue.put(exp)

    return put_to_queue
