import uasyncio as asyncio

import constants as constants
from utils.logger import Log
import interface.led as led

class Events(object):
    def __init__(self):
        self.__task = None

    def __set_task(self, fn):
        self.__task = asyncio.create_task(fn())

    def event(self, event):
        Log.info("Events.event", "event: {}".format(event))

        if self.__task:
            self.__task.cancel()

        if event == constants.SYSTEM_RESET:
            led.boot()
        elif event == constants.SYSTEM_NOT_SETUP:
            self.__set_task(led.not_setup)
        elif event == constants.SYSTEM_SETUP:
            led.setup()
        elif event == constants.SYSTEM_ERROR:
            led.error()
        else:
            Log.error("Led.init", "invalid state")

        
