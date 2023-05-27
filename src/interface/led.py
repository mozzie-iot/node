import machine 
import uasyncio as asyncio

from utils.logger import Log

DUTY_OFF = 1023
DUTY_ON = 0

green = machine.PWM(machine.Pin(12, machine.Pin.OUT), freq=5000, duty=DUTY_OFF)
red = machine.PWM(machine.Pin(13, machine.Pin.OUT), freq=5000, duty=DUTY_OFF)
blue = machine.PWM(machine.Pin(14, machine.Pin.OUT), freq=5000, duty=DUTY_OFF)

class LED:
    def __init__(self):
        self.pulse_task = None

    def reset(self, cancel_task=True):
        if cancel_task and self.pulse_task is not None:
            self.pulse_task.cancel()
        
        blue.duty(DUTY_OFF)
        green.duty(DUTY_OFF)
        red.duty(DUTY_OFF)

    async def pulse_handler(self, color, interval_ms):
        if color == "green":
            target = green
        elif color == "blue":
            target = blue
        elif color == "red":
            target = red
        else: 
            raise Exception("LED pulse color must be either 'green', 'blue' or 'red'")

        while True:
            for i in range(0, 1024, 10):
                target.duty(i)
                await asyncio.sleep_ms(interval_ms)
            for i in range(1023, -1, -10):
                target.duty(i)
                await asyncio.sleep_ms(interval_ms)

    def pulse(self, color, interval_ms=1):
        Log.info("LED.pulse", "color: {}, interval_ms: {}".format(color, interval_ms))
        self.reset()
        self.pulse_task = asyncio.create_task(self.pulse_handler(color, interval_ms))

    def green(self):
        self.reset()
        green.duty(DUTY_ON)

    # Need cancel_task arg to use on system error or keyboard interrupt
    # because when asyncio loop is complete it automatically cleans up tasks    
    # so this would throw exception as it would be canceling tasks that dont exist
    def red(self, cancel_task=True):
        self.reset(cancel_task)
        red.duty(DUTY_ON)

    def blue(self):
        self.reset()
        blue.duty(DUTY_ON)