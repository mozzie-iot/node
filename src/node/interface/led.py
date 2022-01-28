import machine 
import uasyncio as asyncio

DUTY_OFF = 1023
DUTY_ON = 0

green = machine.PWM(machine.Pin(12, machine.Pin.OUT), freq=5000, duty=DUTY_OFF)
blue = machine.PWM(machine.Pin(13, machine.Pin.OUT), freq=5000, duty=DUTY_OFF)
red = machine.PWM(machine.Pin(14, machine.Pin.OUT), freq=5000, duty=DUTY_OFF)
   
def boot():
    blue.duty(DUTY_ON)
    green.duty(DUTY_OFF)
    red.duty(DUTY_OFF)

async def not_setup():
    green.duty(DUTY_OFF)
    red.duty(DUTY_OFF)
    while True:
        for i in range(1024):
            blue.duty(i)
            await asyncio.sleep_ms(2)
        for i in range(1023, -1, -1):
            blue.duty(i)
            await asyncio.sleep_ms(2)

def setup():
    green.duty(DUTY_ON)
    blue.duty(DUTY_OFF)
    red.duty(DUTY_OFF)

def error():
    red.duty(DUTY_ON)
    green.duty(DUTY_OFF)
    blue.duty(DUTY_OFF)
