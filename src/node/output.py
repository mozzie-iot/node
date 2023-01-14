import uasyncio as asyncio

from node.core.node import Node
from node.core.utils.logger import Log

class OutputClient(Node):   
    def __init__(self):
        super().__init__()
        self.__on_state_update = None
        self.__on_settings = None

    # set in base   
    def set_on_state_update_fn(self, fn):
        self.__on_state_update = fn

    def set_on_settings_fn(self, fn):
        self.__on_settings = fn

    # for use in base (mqtt callback)
    def incoming(self, topic, payload, retained):
        secret = self.system.config["secret_key"]

        if topic == f"node/{secret}/settings":
            self.__on_settings(payload)
            self.subscribe_response(topic, payload["id"], "received")
            return

        if topic == f"node/{secret}/state":
            channel = payload["channel"]
            state = payload["state"]
            asyncio.create_task(self.__on_state_update(channel, state)) 
            self.subscribe_response(topic, payload["id"], "success")
            return

        Log.error("OutputClient", f"Unhandled topic: {topic}")

        

        
 