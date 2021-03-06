# -*- coding: utf-8 -*-

from collections import deque
import importlib
import numpy as np

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class Taskmanager(object):

    """taskmanager creates and manages a queue of task() objects
    for the pyfab/jansen system.

    Tasks are added to the queue with registerTask() and are
    performed on a first-come-first-served basis.
    Video frames are passed to the active task by handleTask().
    Once the active task is complete, it is cleaned up and replaced
    with the next task from the queue.
    """

    def __init__(self, parent):
        self.parent = parent
        self.vision = parent.vision
        self.source = parent.screen.source
        self.task = None
        self.queue = deque()
        self._paused = False

    def handleTask(self, frame):
        """Activates the next task in the queue, processes the
        next video frame, then cleans up the task if it is done."""
        if self._paused:
            return
        if self.task is None:
            try:
                self.task = self.queue.popleft()
            except IndexError:
                if isinstance(frame, np.ndarray):
                    self.source.sigNewFrame.disconnect(self.handleTask)
                else:
                    self.vision.sigNewFrame.disconnect(self.handleTask)
                return
        self.task.process(frame)
        if self.task.isDone():
            self.task = None

    def registerTask(self, task, vision=False, **kwargs):
        """Places the named task into the task queue."""
        if isinstance(task, str):
            try:
                taskmodule = importlib.import_module('tasks.' + task)
                taskclass = getattr(taskmodule, task)
                task = taskclass(parent=self.parent, **kwargs)
            except ImportError as err:
                logger.error('Could not import {}: {}'.format(task, err))
                return
        self.queue.append(task)
        if self.task is None:
            if (vision is True or vision == 'True') \
               and hasattr(self.vision, 'sigNewFrame'):
                self.vision.sigNewFrame.connect(self.handleTask)
            else:
                self.source.sigNewFrame.connect(self.handleTask)

    def paused(self):
        return self._paused

    def pauseTasks(self):
        """Toggle the pause state of the task manager"""
        self._paused = not self._paused

    def clearTasks(self):
        """Empty task queue"""
        self.queue.clear()
