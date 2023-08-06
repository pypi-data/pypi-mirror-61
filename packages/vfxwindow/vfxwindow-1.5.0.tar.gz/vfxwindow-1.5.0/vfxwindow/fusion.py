"""Window class for Blackmagic Fusion."""

from __future__ import absolute_import

import os
import sys

import fusionscript

from .utils import setCoordinatesToScreen, hybridmethod
from .standalone import StandaloneWindow


VERSION = sys.executable.split(os.path.sep)[-2].split(' ')[1]


class FusionWindow(StandaloneWindow):
    def __init__(self, parent=None, **kwargs):
        super(FusionWindow, self).__init__(parent, **kwargs)
        self.fusion = True
        self.standalone = False

    def saveWindowPosition(self):
        """Save the window location."""
        try:
            fusionSettings = self.windowSettings['fusion']
        except KeyError:
            fusionSettings = self.windowSettings['fusion'] = {}
        try:
            mainWindowSettings = fusionSettings['main']
        except KeyError:
            mainWindowSettings = fusionSettings['main'] = {}
        mainWindowSettings['width'] = self.width()
        mainWindowSettings['height'] = self.height()
        mainWindowSettings['x'] = self.x()
        mainWindowSettings['y'] = self.y()

        super(FusionWindow, self).saveWindowPosition()

    def loadWindowPosition(self):
        """Set the position of the window when loaded."""
        try:
            width = self.windowSettings['fusion']['main']['width']
            height = self.windowSettings['fusion']['main']['height']
            x = self.windowSettings['fusion']['main']['x']
            y = self.windowSettings['fusion']['main']['y']
        except KeyError:
            super(FusionWindow, self).loadWindowPosition()
        else:
            x, y = setCoordinatesToScreen(x, y, width, height, padding=5)
            self.resize(width, height)
            self.move(x, y)

    @hybridmethod
    def show(cls, self, *args, **kwargs):
        # Window is already initialised
        if self is not cls:
            return super(FusionWindow, self).show()

        # Close down window if it exists and open a new one
        try:
            cls.clearWindowInstance(cls.WindowID)
        except AttributeError:
            pass
        kwargs['exec_'] = True
        return super(FusionWindow, cls).show(*args, **kwargs)
