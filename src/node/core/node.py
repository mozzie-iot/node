import ujson
import uasyncio as asyncio

class Node(object):
    def on_disconnect(self):
        pass

    def set_publish(self, fn):
        self.__publish = fn

    # Format required by NestJS MQTT transporter
    def subscribe_response(self, topic, transaction_id, message):
        responsePayload = ujson.dumps({
            "response": message, 
            "id": transaction_id,
            "isDisposed": True
        })
        asyncio.create_task(self.__publish("{}/reply".format(topic), responsePayload))
