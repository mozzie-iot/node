import ujson
import uasyncio as asyncio

from node.core.node import Node

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

    def set_publish(self, fn):
        self.__publish = fn

    def _subscribe_response(self, topic, transaction_id, message):
        responsePayload = ujson.dumps({
            "response": message, 
            "id": transaction_id,
            "isDisposed": True
        })
        asyncio.create_task(self.__publish("{}/reply".format(topic), responsePayload))

    # for use in base (mqtt callback)
    def incoming(self, topic, payload, retained):
        payloadStr = payload.decode("utf-8");
        payloadObj = ujson.loads(payloadStr)
        data = payloadObj["data"]

        # Set node run settings
        if "settings" in data:
            self.__on_settings(data["settings"])
            self._subscribe_response(topic, payloadObj["id"], "received")
            return
        
        # Handle action
        if "action" in data:
            type = data["action"]["type"]
            channel = data["action"]["channel"]
            asyncio.create_task(self.__on_state_update(channel, type)) 
            self._subscribe_response(topic, payloadObj["id"], "success")
    
    # for use in base
    async def node_routine(self):
        # Constant non terminating pinging for outputs
         while True:
            await asyncio.sleep_ms(300)
        

        
 