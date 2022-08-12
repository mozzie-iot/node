from machine import Pin

from node.output import OutputClient
from node.core.utils.logger import Log

class NodeClient(OutputClient):
    # Node public key - required
    public_key = "5f65c49c-d2d6-4fcc-a4e3-78c893df4da5"
    channels = {
        1: {"pin": 18},
        2: {"pin": 19},
        3: {"pin": 21},
        4: {"pin": 22}
    }

    def on_settings(self, settings):
        Log.info("NodeClient.on_settings", settings)
    
    async def on_state_update(self, status, channel):
        pin = NodeClient.channels[int(channel)]["pin"]
        Log.info("NodeClient.on_state_update", "pin:{0} status:{1}".format(pin, status))
        relay = Pin(pin, Pin.OUT)
        num_status = 0 if status == "on" else 1 # setup for normally open config
        relay.value(num_status)
        
    