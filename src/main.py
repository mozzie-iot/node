import uasyncio as asyncio

from node.core.interface.device import Device
from node.core.mqtt_client import MQTTClient
from node.core.lib.bluetooth import Ble

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
        led.pulse("blue")
        # if not setup, Ble advertising with non terminating event
        await asyncio.create_task(Ble(system).routine())

    await asyncio.create_task(MQTTClient(system, led).routine())
try:
    if config:
        asyncio.run(main())
finally:
    asyncio.new_event_loop()