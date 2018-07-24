# -*- coding: utf-8 -*-

"""QTrap.py: Base class for an optical trap."""

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from enum import Enum


class states(Enum):
    static = 0
    normal = 1
    selected = 2
    grouping = 3
    inactive = 4


class QTrap(QtCore.QObject):
    """A trap has physical properties, including three-dimensional
    position, relative amplitude and relative phase.
    It also has an appearance as presented on the QFabScreen.
    """

    valueChanged = QtCore.pyqtSignal(QtCore.QObject)

    def __init__(self,
                 parent=None,
                 r=QtGui.QVector3D(),
                 a=1.,  # relative amplitude
                 phi=None,  # relative phase
                 psi=None,  # current hologram
                 cgh=None,  # computational pipeline
                 structure=1.+0.j,  # structuring field
                 state=states.normal):
        super(QTrap, self).__init__()

        self.ignoreUpdates = True

        # organization
        if parent is not None:
            self.parent = parent
        # operational state
        self._state = state
        # appearance
        self.brush = {states.normal: pg.mkBrush(100, 255, 100, 120),
                      states.selected: pg.mkBrush(255, 100, 100, 120),
                      states.grouping: pg.mkBrush(255, 255, 100, 120),
                      states.inactive: pg.mkBrush(0, 0, 255, 120)}
        self.spot = {'pos': QtCore.QPointF(),
                     'size': 10.,
                     'pen': pg.mkPen('k', width=0.5),
                     'brush': self.brush[state],
                     'symbol': self.plotSymbol()}
        # physical properties
        self.properties = []
        self.registerProperty('x')
        self.registerProperty('y')
        self.registerProperty('z')
        self.registerProperty('a', decimals=2)
        self.registerProperty('phi', decimals=2)
        self.r = r
        self._a = a
        if phi is None:
            self.phi = np.random.uniform(low=0., high=2. * np.pi)
        else:
            self.phi = phi
        self.psi = psi
        self._structure = structure
        self.cgh = cgh

        self.update_appearance()
        self.needsUpdate = True
        self.ignoreUpdates = False

    # Customizable methods for subclassed traps
    def plotSymbol(self):
        """Graphical representation of trap"""
        return 'o'

    def update_appearance(self):
        """Adapt trap appearance to trap motion and property changes"""
        self.spot['pos'] = self.coords()
        self.spot['size'] = np.clip(10. + self.r.z() / 10., 5., 20.)

    def update_structure(self):
        """Update structuring field to properties of CGH pipeline"""
        self.structure = 1. + 0.j

    # Private method to implement changes
    def _update(self):
        """Implement changes in trap properties"""
        if self.ignoreUpdates:
            return
        self.needsUpdate = True
        self.valueChanged.emit(self)
        self.update_appearance()
        self.parent._update()

    @property
    def cgh(self):
        return self._cgh

    @cgh.setter
    def cgh(self, cgh):
        self._cgh = cgh
        if cgh is None:
            return
        self._cgh.sigUpdateGeometry.connect(self.update_structure)
        self.update_structure()

    # Methods for implementing motion
    def coords(self):
        """In-plane position of trap for plotting"""
        return self._r.toPointF()

    def moveBy(self, dr):
        """Translate trap."""
        self.r = self.r + dr

    def moveTo(self, r):
        """Move trap to position r"""
        self.r = r

    def isWithin(self, rect):
        """Return True if this trap lies within the specified rectangle"""
        return rect.contains(self.coords())

    # Slot for updating parameters with QTrapWidget
    def registerProperty(self, property, decimals=1, tooltip=False):
        prop = {'name': property,
                'decimals': decimals,
                'tooltip': tooltip}
        self.properties.append(prop)

    @QtCore.pyqtSlot(str, float)
    def setProperty(self, name, value):
        self.blockSignals(True)
        setattr(self, name, value)
        self.blockSignals(False)

    # Trap properties
    @property
    def r(self):
        """Three-dimensional position of trap"""
        return self._r

    @r.setter
    def r(self, r):
        self._r = QtGui.QVector3D(r)
        self._update()

    @property
    def x(self):
        return self._r.x()

    @x.setter
    def x(self, x):
        self._r.setX(x)
        self._update()

    @property
    def y(self):
        return self._r.y()

    @y.setter
    def y(self, y):
        self._r.setY(y)
        self._update()

    @property
    def z(self):
        return self._r.z()

    @z.setter
    def z(self, z):
        self._r.setZ(z)
        self._update()

    @property
    def a(self):
        """Relative amplitude of trap"""
        return self._a

    @a.setter
    def a(self, a):
        self._a = a
        self.amp = a * np.exp(1j * self.phi)
        self._update()

    @property
    def phi(self):
        """Relative phase of trap"""
        return self._phi

    @phi.setter
    def phi(self, phi):
        self._phi = phi
        self.amp = self.a * np.exp(1j * phi)
        self._update()

    @property
    def state(self):
        """Current state of trap"""
        return self._state

    @state.setter
    def state(self, state):
        if self.state is not states.static:
            self._state = state
            self.spot['brush'] = self.brush[state]

    # Structure field for multifunctional traps
    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, field):
        self._structure = self.cgh.bless(field)
        self._update()
