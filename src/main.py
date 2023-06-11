import uasyncio as asyncio
import ujson

from mqtt_client import MQTTClient

CONFIG_FILE = 'config.json'

def set_global_exception():
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

async def main(config):
    set_global_exception()  # Debug aid        
    await MQTTClient(config).routine()

try:
    f = open(CONFIG_FILE,'r')
    config_str=f.read()
    f.close()

    config = ujson.loads(config_str)

    asyncio.run(main(config))
finally:
    asyncio.new_event_loop()