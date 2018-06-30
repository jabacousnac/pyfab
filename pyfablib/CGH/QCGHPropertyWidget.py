# -*- coding: utf-8 -*-

"""Control panel for configuring hologram calculation."""

from common.QPropertySheet import QPropertySheet
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class QCGHPropertyWidget(QPropertySheet):

    def __init__(self, parent):
        super(QCGHPropertyWidget, self).__init__(title='CGH Pipeline')
        cgh = parent.cgh
        slm = cgh.slm
        cam = parent.screen.video.defaultSource
        register = self.registerProperty
        setter = cgh.setProperty

        self.wqpp = register('qpp', cgh.qpp, 0.1, 100., setter)
        self.walpha = register('alpha', cgh.alpha, 0.1, 10., setter)
        self.wxc = register('xc', cgh.rc.x(), 0, cam.width, setter)
        self.wyc = register('yc', cgh.rc.y(), 0, cam.height, setter)
        self.wzc = register('zc', cgh.rc.z(), -500, 500, setter)
        self.wthetac = register('thetac', cgh.thetac, -180, 180, setter)
        self.wxs = register('xs', cgh.rs.x(), 0, slm.width(), setter)
        self.wys = register('ys', cgh.rs.y(), 0, slm.height(), setter)
        self.wk0 = register('k0', cgh.k0, -10, 10, setter)
        self.addToolTips()

    def addToolTips(self):
        self.wqpp.setToolTip('Overall scale factor [mrad/pixel]')
        self.walpha.setToolTip('x-y anisotropy')
        self.wxc.setToolTip('x position of optical axis on camera [pixel]')
        self.wyc.setToolTip('y position of optical axis on camera [pixel]')
        self.wzc.setToolTip('axial position of zeroth-order plane [pixel]')
        self.wthetac.setToolTip(
            'orientation of camera relative to SLM [degrees]')
        self.wxs.setToolTip('x position of optical axis on SLM [pixel]')
        self.wys.setToolTip('y position of optical axis on SLM [pixel]')
        self.wk0.setToolTip('Axial splay factor [radian/pixel]')

    def configuration(self):
        return {'xs': self.wxs.value,
                'ys': self.wys.value,
                'qpp': self.wqpp.value,
                'alpha': self.walpha.value,
                'xc': self.wxc.value,
                'yc': self.wyc.value,
                'zc': self.wzc.value,
                'thetac': self.wthetac.value,
                'k0': self.wk0.value}

    def setConfiguration(self, properties):
        for property, value in properties.items():
            try:
                self.__dict__['w' + property].value = value
            except KeyError:
                logger.warning('Unknown attribute: {}'.format(property))
