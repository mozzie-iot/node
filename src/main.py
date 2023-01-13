import uasyncio as asyncio

from node.core.interface.device import Device
from node.core.mqtt_client import MQTTClient
from node.core.lib.bluetooth import Ble
from node.core.utils.logger import Log

def set_global_exception():
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

async def main():
    set_global_exception()  # Debug aid        

    #  config var passed from boot.py
    system = Device(config, led)

    # Listen for reset btn
    asyncio.create_task(system.routine())

    if not system.is_setup:
        Log.info("main", "Not setup!")
        led.pulse("blue", 1)
        # if not setup, Ble advertising with non terminating event
        await asyncio.create_task(Ble(system).routine())

    Log.info("main", "Device setup!")
    await asyncio.create_task(MQTTClient(system, led).routine())

loop = asyncio.get_event_loop()
try:
    if config:
        asyncio.run(main())
        loop.run_forever()
except Exception as e:
    Log.error("main", "System error", e)
    led.red(False)
except KeyboardInterrupt:
    Log.error("main", "Keyboard interrupt")
    led.red(False)
finally:
    loop.close()