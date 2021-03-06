# -*- coding: utf-8 -*-

"""QTrap.py: Base class for an optical trap."""

from PyQt5.QtCore import (pyqtSignal, pyqtSlot, QObject, QPointF)
from PyQt5.QtGui import QVector3D
import numpy as np
import pyqtgraph as pg
from enum import Enum
from collections import OrderedDict


class states(Enum):
    static = 0
    normal = 1
    selected = 2
    grouping = 3


class QTrap(QObject):
    """A trap has physical properties, including three-dimensional
    position, relative amplitude and relative phase.  A structuring
    field can change its optical properties.
    It also has an appearance as presented on the QFabScreen.
    """

    valueChanged = pyqtSignal(QObject)

    def __init__(self,
                 parent=None,
                 r=QVector3D(),
                 alpha=1.,          # relative amplitude
                 phi=None,          # relative phase
                 cgh=None,          # computational pipeline
                 structure=None,    # structuring field
                 state=states.normal):
        super(QTrap, self).__init__(parent)

        self.blockRefresh(True)

        # operational state
        self._state = state

        # appearance
        self.brush = {states.normal: pg.mkBrush(100, 255, 100, 120),
                      states.selected: pg.mkBrush(255, 105, 180, 120),
                      states.grouping: pg.mkBrush(255, 255, 100, 120)}
        self.baseSize = 15.
        self.spot = {'pos': QPointF(),
                     'size': self.baseSize,
                     'pen': pg.mkPen('w', width=0.2),
                     'brush': self.brush[state],
                     'symbol': self.plotSymbol()}

        # physical properties
        self.r = r
        self._alpha = alpha
        if phi is None:
            self.phi = np.random.uniform(low=0., high=2. * np.pi)
        else:
            self.phi = phi
        self.registerProperties()
        self.updateAppearance()

        # hologram calculation
        self._structure = structure
        self.psi = None
        self.cgh = cgh

        self.needsRefresh = True
        self.blockRefresh(False)

    # Customizable methods for subclassed traps
    def plotSymbol(self):
        """Graphical representation of trap"""
        return 'o'

    def updateAppearance(self):
        """Adapt trap appearance to trap motion and property changes"""
        self.spot['pos'] = self.coords()
        self.spot['size'] = np.clip(self.baseSize - self.r.z() / 20., 10., 35.)

    def updateStructure(self):
        """Update structuring field for changes in trap properties
        and calibration constants
        """
        pass

    # Computational pipeline for calculating structure field
    @property
    def cgh(self):
        return self._cgh

    @cgh.setter
    def cgh(self, cgh):
        self._cgh = cgh
        if cgh is None:
            return
        self._cgh.sigUpdateGeometry.connect(self.updateStructure)
        self._cgh.sigUpdateTransformationMatrix.connect(self.updateStructure)
        self.updateStructure()

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, field):
        self._structure = self.cgh.bless(field)
        self.refresh()

    # Implementing changes in properties
    def blockRefresh(self, state):
        """Do not send refresh requests to parent if state is True"""
        self._blockRefresh = bool(state)

    def refreshBlocked(self):
        return self._blockRefresh

    def refresh(self):
        """Request parent to implement changes"""
        if self.refreshBlocked():
            return
        self.valueChanged.emit(self)
        self.updateAppearance()
        self.needsRefresh = True
        self.parent().refresh()

    # Methods for moving the trap
    def moveBy(self, dr):
        """Translate trap by specified displacement vector"""
        self.r = self.r + dr

    def moveTo(self, r):
        """Move trap to position r"""
        self.r = r

    def coords(self):
        """In-plane position of trap for plotting"""
        return self._r.toPointF()

    def isWithin(self, rect):
        """Return True if this trap lies within the specified rectangle"""
        return rect.contains(self.coords())

    # Methods for editing properties with QTrapWidget
    def registerProperty(self, name, decimals=2, tooltip=False):
        """Register a property so that it can be edited"""
        self.properties[name] = {'decimals': decimals,
                                 'tooltip': tooltip}

    @pyqtSlot(str, float)
    def setProperty(self, name, value):
        """Thread-safe method to change a specified property without
        emitting signals.  This is called by QTrapWidget when the
        user edits a property.  Blocking signals prevents a loop.
        """
        self.blockSignals(True)
        setattr(self, name, value)
        self.blockSignals(False)

    # Trap properties
    def registerProperties(self):
        self.properties = OrderedDict()
        self.registerProperty('x')
        self.registerProperty('y')
        self.registerProperty('z')
        self.registerProperty('alpha', decimals=2)
        self.registerProperty('phi', decimals=2)

    @property
    def r(self):
        """Three-dimensional position of trap"""
        return self._r

    @r.setter
    def r(self, r):
        self._r = QVector3D(r)
        self.refresh()

    @property
    def x(self):
        return self._r.x()

    @x.setter
    def x(self, x):
        self._r.setX(x)
        self.refresh()

    @property
    def y(self):
        return self._r.y()

    @y.setter
    def y(self, y):
        self._r.setY(y)
        self.refresh()

    @property
    def z(self):
        return self._r.z()

    @z.setter
    def z(self, z):
        self._r.setZ(z)
        self.refresh()

    @property
    def alpha(self):
        """Relative amplitude of trap"""
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._alpha = alpha
        self.amp = alpha * np.exp(1j * self.phi)
        self.refresh()

    @property
    def phi(self):
        """Relative phase of trap"""
        return self._phi

    @phi.setter
    def phi(self, phi):
        self._phi = phi
        self.amp = self.alpha * np.exp(1j * phi)
        self.refresh()

    @property
    def state(self):
        """Current state of trap"""
        return self._state

    @state.setter
    def state(self, state):
        if self.state is not states.static:
            self._state = state
            self.spot['brush'] = self.brush[state]
