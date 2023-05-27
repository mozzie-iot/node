import uasyncio as asyncio

from mqtt_client import MQTTClient
from utils.logger import Log

def set_global_exception():
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

async def main():
    set_global_exception()  # Debug aid        
    await asyncio.create_task(MQTTClient(config, led).routine())

loop = asyncio.get_event_loop()
try:
    if config is not None:
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