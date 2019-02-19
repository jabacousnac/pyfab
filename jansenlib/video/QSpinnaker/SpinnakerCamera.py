#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PySpin
import cv2

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

'''
NOTE
USB 3.x communication on Ubuntu 16.04 requires
> sudo sh -c 'echo 1000 > /sys/module/usbcore/parameters/usbfs_memory_mb'
'''

# Dynamic mapping for GenICam attributes
_amap = {'acquisitionmode': 'AcquisitionMode',
         'acquisitionstart': 'AcquisitionStart',
         'acquisitionstop': 'AcquisitionStop',
         'blacklevel': 'BlackLevel',
         'exposure': 'ExposureTime',
         'exposureauto': 'ExposureAuto',
         'exposuremode': 'ExposureMode',
         'framerate': 'AcquisitionFrameRate',
         'framerateauto': 'AcquisitionFrameRateAuto',
         'framerateenabled': 'AcquisitionFrameRateEnabled',
         'gain': 'Gain',
         'gainauto': 'GainAuto',
         'height': 'Height',
         'heightmax': 'HeightMax',
         'mirrored': 'ReverseX',
         'pixelformat': 'PixelFormat',
         'sensorwidth': 'SensorWidth',
         'sensorheight': 'SensorHeight',
         'videomode': 'VideoMode',
         'width': 'Width',
         'widthmax': 'WidthMax',
         'x0': 'OffsetX',
         'y0': 'OffsetY'}


class SpinnakerCamera(object):

    '''Abstraction of FLiR camera for PyFab/Jansen

    Attributes
    ----------
    device: PySpin.CameraPtr
        camera device in Spinnaker system

    Attributes
    ----------
    exposureauto: str: 'Off', 'Once', 'Continuous'
        Enable automatic control of exposure time
    exposuremode: str: 'Off', 'Timed', 'TriggerWidth', 'TriggerControlled'
        Method for initiating exposure
    framerateauto: str: 'Off', 'Continuous'
        Enable automatic control of frame rate
    framerateenabled: bool
        Enable manual control of frame rate
    gainauto: 'Off', 'Once', 'Continuous'
        Enable automatic control of gain
    gray: bool
        read() returns single-channel (grayscale) image if True

    Methods
    -------
    get(name):
        Get named property
    set(name, value):
        Set named property to value
    read(): (bool, numpy.ndarray)
        Return next available video frame
    '''

    def __init__(self,
                 acquisitionmode='Continuous',
                 exposuremode='Timed',
                 exposureauto='Off',
                 flipped=False,
                 framerateauto='Off',
                 framerateenabled=True,
                 gainauto='Off',
                 gray=True,
                 mirrored=False):
        # super(SpinnakerCamera, self).__init__()

        # Initialize Spinnaker and get list of cameras
        self._system = PySpin.System.GetInstance()
        self._devices = self._system.GetCameras()
        if self._devices.GetSize() < 1:
            logger.error('No Spinnaker cameras found')

        # Work with first attached camera.  This can be generalized
        self.device = self._devices[0]
        self.device.Init()
        # Camera inodes provide access to device properties
        self._nodes = self.device.GetNodeMap()
        # Start acquisition
        self.acquisitionmode = acquisitionmode
        self.exposureauto = exposureauto
        self.exposuremode = exposuremode
        self.flipped = flipped
        self.framerateauto = framerateauto
        self.framerateenabled = framerateenabled
        self.gainauto = gainauto
        self.gray = gray
        self.mirrored = mirrored
        self.start()

    def __del__(self):
        logger.debug('Cleaning up')
        self.stop()
        self.device.DeInit()
        del self.device
        self._devices.Clear()
        self._system.ReleaseInstance()

    def start(self):
        '''Start image acquisition'''
        self.device.BeginAcquisition()

    def stop(self):
        '''Stop image acquisition'''
        self.device.EndAcquisition()

    def read(self):
        '''The whole point of the thing: Gimme da piccy'''
        res = self.device.GetNextImage()
        error = res.IsIncomplete()
        if error:
            status = res.GetImageStatus()
            error_msg = res.GetImageStatusDescription(status)
            logger.warning('Incomplete Image: ' + error_msg)
        shape = (res.GetHeight(), res.GetWidth())
        image = res.GetData().reshape(shape)
        if self.flipped:
            image = cv2.flip(image, 0)
        return not error, image

    @property
    def acquisitionmode(self):
        return self._get_feature('AcquisitionMode')

    @acquisitionmode.setter
    def acquisitionmode(self, mode):
        self._set_feature('AcquisitionMode', mode)

    @property
    def exposure(self):
        return self._get_feature('ExposureTime')

    @exposure.setter
    def exposure(self, value):
        self._set_feature('ExposureTime', value)

    @property
    def exposureauto(self):
        return self._get_feature('ExposureAuto')

    @exposureauto.setter
    def exposureauto(self, value):
        self._set_feature('ExposureAuto', value)

    @property
    def exposuremode(self):
        return self._get_feature('ExposureMode')

    @exposuremode.setter
    def exposuremode(self, value):
        self._set_feature('ExposureMode', value)

    @property
    def flipped(self):
        return self._flipped

    @flipped.setter
    def flipped(self, state):
        self._flipped = bool(state)

    @property
    def framerate(self):
        return self._get_feature('AcquisitionFrameRate')

    @framerate.setter
    def framerate(self, value):
        self._set_feature('AcquisitionFrameRate', value)

    @property
    def framerateauto(self):
        return self._get_feature('AcquisitionFrameRateAuto')

    @framerateauto.setter
    def framerateauto(self, state):
        self._set_feature('AcquisitionFrameRateAuto', state)

    @property
    def framerateenabled(self):
        return self._get_feature('AcquisitionFrameRateEnabled')

    @framerateenabled.setter
    def framerateenabled(self, state):
        self._set_feature('AcquisitionFrameRateEnabled', state)

    @property
    def gain(self):
        return self._get_feature('Gain')

    @gain.setter
    def gain(self, value):
        self._set_feature('Gain', value)

    @property
    def gainauto(self):
        return self._get_feature('GainAuto')

    @gainauto.setter
    def gainauto(self, value):
        self._set_feature('GainAuto', value)

    @property
    def gray(self):
        return self.pixelformat == 'Mono8'

    @gray.setter
    def gray(self, state):
        if (state):
            self.pixelformat = 'Mono8'
        else:
            self.pixelformat = 'RGB8'

    @property
    def height(self):
        return self._get_feature('Height')

    @height.setter
    def height(self, value):
        self._set_feature('Height', value)

    @property
    def heightmax(self):
        return self._get_feature('HeightMax')

    @property
    def mirrored(self):
        return self._get_feature('ReverseX')

    @mirrored.setter
    def mirrored(self, state):
        self._set_feature('ReverseX', state)

    @property
    def pixelformat(self):
        return self._get_feature('PixelFormat')

    @pixelformat.setter
    def pixelformat(self, value):
        self._set_feature('PixelFormat', value)

    @property
    def videomode(self):
        return self._get_feature('VideoMode')

    @videomode.setter
    def videomode(self, mode):
        self.stop()
        self._set_feature('VideoMode', mode)
        self.start()

    @property
    def width(self):
        return self._get_feature('Width')

    @width.setter
    def width(self, value):
        self._set_feature('Width', value)

    @property
    def widthmax(self):
        return self._get_feature('WidthMax')

    def autoexposure(self):
        self.exposureauto = 'Once'

    def autogain(self):
        self.gainauto = 'Once'

    def size(self):
        return (self.height, self.width)

    #
    # private methods for handling interactions with GenICam
    #
    _fmap = {PySpin.intfICategory: PySpin.CCategoryPtr,
             PySpin.intfIString: PySpin.CStringPtr,
             PySpin.intfIInteger: PySpin.CIntegerPtr,
             PySpin.intfIFloat: PySpin.CFloatPtr,
             PySpin.intfIBoolean: PySpin.CBooleanPtr,
             PySpin.intfICommand: PySpin.CCommandPtr,
             PySpin.intfIEnumeration: PySpin.CEnumerationPtr}

    def _feature(self, fname):
        '''Return inode for named feature'''
        feature = None
        try:
            node = self._nodes.GetNode(fname)
            type = node.GetPrincipalInterfaceType()
            feature = self._fmap[type](node)
        except AttributeError:
            logger.warn('Could not access Property: {}'.format(fname))
        return feature

    def _get_feature(self, fname):
        feature = self._feature(fname)
        value = None
        if self._is_enum(feature) or self._is_command(feature):
            value = feature.ToString()
        elif self._is_readable(feature):
            value = feature.GetValue()
        logger.debug('Getting {}: {}'.format(fname, value))
        return value

    def _set_feature(self, fname, value):
        logger.debug('Setting {}: {}'.format(fname, value))
        feature = self._feature(fname)
        if not self._is_writable(feature):
            logger.warning('Property {} is not writable'.format(fname))
            return
        try:
            if self._is_enum(feature) or self._is_command(feature):
                feature.FromString(value)
            else:
                feature.SetValue(value)
        except PySpin.SpinnakerException as ex:
            logger.warning('Could not set {}: {}'.format(fname, ex))

    def _is_readable(self, feature):
        return PySpin.IsAvailable(feature) and PySpin.IsReadable(feature)

    def _is_writable(self, feature):
        return PySpin.IsAvailable(feature) and PySpin.IsWritable(feature)

    def _is_type(self, feature, typevalue):
        return (self._is_readable(feature) and
                feature.GetPrincipalInterfaceType() == typevalue)

    def _is_category(self, feature):
        return self._is_type(feature, PySpin.intfICategory)

    def _is_enum(self, feature):
        return self._is_type(feature, PySpin.intfIEnumeration)

    def _is_command(self, feature):
        return self._is_type(feature, PySpin.intfICommand)

    #
    # Methods for introspection
    #
    def camera_info(self):
        '''Return dict of camera inodes and values'''
        root = PySpin.CCategoryPtr(self._nodes.GetNode('Root'))
        categories = dict()
        for category in root.GetFeatures():
            if self._is_category(category):
                cname = category.GetName()
                cnode = self._feature(cname)
                features = dict()
                for node in cnode.GetFeatures():
                    if not self._is_readable(node):
                        continue
                    fname = node.GetName()
                    features[fname] = self._get_feature(fname)
                categories[cname] = features
        return categories

    def transport_info(self):
        '''Return dict of Transport Layer Device inodes and values'''
        nodemap = self.device.GetTLDeviceNodeMap()  # Transport layer
        try:
            info = PySpin.CCategoryPtr(nodemap.GetNode('DeviceInformation'))
            if self._is_readable(info):
                features = info.GetFeatures()
                for feature in features:
                    this = PySpin.CValuePtr(feature)
                    print('{}: {}'.format(this.GetName(), this.ToString()))
                else:
                    print('Device control information not available')
        except PySpin.SpinnakerException as ex:
            logger.warning('{}'.format(ex))


if __name__ == '__main__':
    cam = SpinnakerCamera()
    print(cam.width)
    _, img = cam.read()
    print(img.shape)
    del cam