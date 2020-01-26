# -*- coding: utf-8 -*-
# MENU: Auto-Trap

from .Task import Task
from PyQt5.QtGui import QVector3D


class AutoTrap(Task):
    """Detect and trap particles on the screen."""

    def __init__(self, **kwargs):
        super(AutoTrap, self).__init__(**kwargs)
        self.traps = None

    def center(self, rectangle):
        return (rectangle[0] + rectangle[2]/2.,
                rectangle[1] + rectangle[3]/2., 0.)

    def initialize(self, frame):
        rects = self.parent.filters.detector.grab(frame)
        coords = list(map(lambda r: QVector3D(*self.center(r)), rects))
        self.traps = self.parent.pattern.createTraps(coords)