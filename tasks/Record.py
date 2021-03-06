# -*- coding: utf-8 -*-

'''Task to record a video for a certain number of frames.'''

from .Task import Task


class Record(Task):

    def __init__(self, fn=None, stop=True, **kwargs):
        # Pass in nframes keyword for length of recording
        super(Record, self).__init__(**kwargs)
        self.fn = fn
        self.stop = stop

    def initialize(self, frame):
        self.dvr = self.parent.dvr
        if self.fn is not None:
            self.dvr.filename = self.fn
        self.dvr.recordButton.animateClick()

    def dotask(self):
        if self.stop:
            self.dvr.stopButton.animateClick()
