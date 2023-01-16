import ujson
import uasyncio as asyncio

from node.core.node import Node
from node.core.utils.logger import Log

class InputClient(Node):
    def __init__(self):
        super().__init__()
        self.__active_state_task = None
        self.__on_state_activate = None

    def __update_state(self, state, topic, payload):
        if state == "on":
            self.__active_state_task = asyncio.create_task(self.__on_state_activate())
            self.subscribe_response(topic, payload["id"], "success")
        elif state == "off":
            if self.__active_state_task is not None:
                self.__active_state_task.cancel()
                
            self.subscribe_response(topic, payload["id"], "success")
            self.on_state_deactivate()

    # set in base 
    def set_on_state_activate_fn(self, fn):
        self.__on_state_activate = fn

    # Optional method to be used in client
    def on_state_deactivate(self):
        pass

    # Called when node connects to broker to set initial state
    def on_bootstrap(self, topic, payload, retained):
        state = payload["response"]
        self.__update_state(state, topic, payload)

    def send_value(self, channel, value):
        topic = self.system.config["secret_key"]
        message = ujson.dumps({"channel": channel, "value": value})
        asyncio.create_task(self.__publish(topic, message))

    # for use in base (mqtt callback)
    def incoming(self, topic, payload, retained):
        secret = self.system.config["secret_key"]

        if topic == f"node/{secret}/settings":
            self.on_settings(payload)
            self.subscribe_response(topic, payload["id"], "received")
            return

        if topic == f"node/{secret}/state":
            state = payload["state"]
            self.__update_state(state, topic, payload)
            return

        Log.error("InputClient", f"Unhandled topic: {topic}")
            
            

        

        
 