import ujson
import uasyncio as asyncio

from node.utils.logger import Log

class InputClient(object):
    def __init__(self):
        self.__active_state_task = None
        self.__on_active_state = None
        self.__on_settings = None
        self.__publish = None

    # set in base 
    def set_on_active_state_fn(self, fn):
        self.__on_active_state = fn

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

    def send_value(self, channel, value):
        message = ujson.dumps({"channel": channel, "value": value})
        topic = "input/{}".format(self.system.config["secret_key"])
        asyncio.create_task(self.__publish(topic, message))

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
            if type == "activate":
                channels = data["action"]["channels"]
                self.__active_state_task = asyncio.create_task(self.__on_active_state(channels)) 
                self._subscribe_response(topic, payloadObj["id"], "success")
                Log.info("InputClient.incoming","status: ACTIVE")
            elif type == "deactivate":
                self.__active_state_task.cancel()
                self._subscribe_response(topic, payloadObj["id"], "success")
                Log.info("InputClient.incoming","status: INACTIVE")
            return

    # for use in base
    async def node_routine(self):
        while True:
            await asyncio.sleep_ms(300)
            
            

        

        
 