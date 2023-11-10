import logging
from util import media_control
from .media_control.controls import Controls

logger = logging.getLogger(__name__)

class vidObj:

    def __init__(self):
        pass

    def media_control(self, source):
        return media_control(source)

    def controls(self):
        return Controls()
