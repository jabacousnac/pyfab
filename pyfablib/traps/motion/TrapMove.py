# -*- coding: utf-8 -*-

"""Framework for moving all current traps along some trajectory"""

import numpy as np
from PyQt5.QtGui import QVector3D
from PyQt5.QtCore import (pyqtSlot, pyqtProperty, QObject)


class TrapMove(QObject):

    def __init__(self, **kwargs):
        super(TrapMove, self).__init__(**kwargs)
        self._traps = None
        self._trajectories = None

        self._stepRate = 3.
        self._maxStep = 0.

        self._running = False
        self._t = 0
        self._tf = 0

    #
    # Essential properties and methods for user interaction
    #
    @property
    def traps(self):
        '''A QTrapGroup selected for movement'''
        return self._traps

    @traps.setter
    def traps(self, traps):
        self._traps = traps
        if traps is not None:
            traps.select(True)

    def start(self):
        traps = self.traps
        self.parameterize(traps)
        self._counter = 0
        self._running = True

    #
    # PyQt properties to be tuned for performance
    #
    @pyqtProperty(float)
    def stepRate(self):
        '''Number of displacements per second [steps/s]'''
        return self._stepRate

    @stepRate.setter
    def stepRate(self, stepRate):
        self._stepRate = stepRate

    @pyqtProperty(float)
    def maxStep(self):
        '''Maximum step size in [um]'''
        return self._maxStep

    @maxStep.setter
    def maxStep(self, maxStep):
        self._maxStep = maxStep

    #
    # Properties and methods to be used in subclassing
    #
    @property
    def trajectories(self):
        '''Dictionary with QTrap keys and Trajectory values'''
        return self._trajectories

    def parameterize(self, traps):
        self._t = 0
        self._tf = 0
        trajectories = {}
        for trap in traps.flatten():
            r_i = (trap.r.x(), trap.r.y(), trap.r.z())
            trajectories[trap] = Trajectory(r_i)
        self._trajectories = trajectories

    #
    # Properties and methods for core movement functionality
    #
    @property
    def wait(self):
        fps = self.parent().screen.fps
        stepRate = self.stepRate
        return round(fps/stepRate)

    @pyqtSlot(np.ndarray)
    def move(self, frame):
        if self._running:
            if self._counter == 0:
                if self._t < self._tf:
                    for trap in self.traps.flatten():
                        trajectory = self.trajectories[trap].trajectory
                        r_t = QVector3D(*trajectory[self._t])
                        trap.moveTo(r_t)
                    self._t += 1
                self._counter = self.wait
            else:
                self._counter -= 1
            if self._t == self._tf:
                self._running = False


class Trajectory(object):
    '''
    Creates and manipulates a parameterized trajectory in
    cartesian coordinates
    '''

    def __init__(self, r_i, **kwargs):
        super(Trajectory, self).__init__(**kwargs)
        self.trajectory = np.zeros(shape=(1, 3))
        self.trajectory[0] = np.array([r_i[0], r_i[1], r_i[2]])
        self.last_step = None

    @property
    def r_f(self):
        return self.trajectory[-1]

    @property
    def r_i(self):
        return self.trajectory[0]

    def step(self, d):
        self.last_step = d
        self.trajectory = np.concatenate((self.trajectory,
                                          np.array([self.r_f + d])),
                                         axis=0)

    def add(self, r):
        self.trajectory = np.concatenate((self.trajectory,
                                          np.array([r])),
                                         axis=0)

    def stitch(self, trajectory):
        '''Adds another trajectory to the end of the trajectory
        '''
        self.trajectory = np.append(self.trajectory,
                                    trajectory.trajectory, axis=0)

    def __str__(self):
        np.set_printoptions(
            formatter={'float': lambda x: "{0:0.2f}".format(x)})
        data = [self.trajectory.shape,
                self.r_i,
                self.r_f,
                self.last_step]
        string = "Trajectory(shape={}, r_i={}, r_f={}, last_step={})"
        return string.format(*data)
