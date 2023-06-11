import sys
import uasyncio as asyncio
import ujson

from lib.mqtt_as import MQTT_AS_Client

from client import NodeClient

class MQTTClient(NodeClient):
    def __init__(self, config):
        super().__init__(config)

    # Format required by NestJS MQTT transporter
    def __subscribe_resp(self, topic, transaction_id, message):
        responsePayload = ujson.dumps({
            "response": message, 
            "id": transaction_id,
            "isDisposed": True
        })

        asyncio.create_task(self.client.publish("{}/reply".format(topic), responsePayload))

    async def __node_online(self, client):
        if self.config["debug"]:
            print("Publish node online")

        # note: need id to get response and nestjs doesn't expose id
        # we set data as client_id too
        payload = {
            "id": self.config["client_id"],
            "data": self.config["client_id"]
        }

        await client.publish('status/online', ujson.dumps(payload))

    async def __connect_coro(self, client):
        asyncio.create_task(self.connected_cb(client))

        # If broker or transporter go down, they will publish 'alive_check' when 
        # back up - mostly relevant for hot reloading in development
        await client.subscribe("alive_check", 0)

        # Responds to node online alert with status detail to sync hub/node
        await client.subscribe("status/online/reply", 0)
       
        # After subscribing to topics, let broker know we are ready
        await self.__node_online(client)

    def __subs_cb(self, topic, payload, retained):
        try:
            if self.config["debug"]:
                print(f"Msg received - topic: {topic}, payload: {payload}, retained: {retained}")

            decodedTopic = topic.decode("utf-8")
            decodedPayload = payload.decode("utf-8");
            payloadDict = ujson.loads(decodedPayload)

            if decodedTopic == "alive_check":
                asyncio.create_task(self.__node_online(self.client))
                return
            
            if decodedTopic == "status/online/reply":
                if self.config["debug"]:
                    print("Publish node online ACK")
                return
            
            self.subscribe_cb(topic, payloadDict, retained)

            self.__subscribe_resp(decodedTopic, payloadDict["id"], "ACK")
        except Exception as e:
            if self.config["debug"]:
                print("__subs_cb error: ", e)
            sys.exit()

    async def __wifi_coro(self, network_state):
        if not network_state:
            self.disconnected_cb()

    async def routine(self):
        MQTT_AS_Client.DEBUG = self.config["debug"]
        client  = MQTT_AS_Client({
            'client_id':     self.config["client_id"],
            'server':        self.config["server"],
            'subs_cb':       self.__subs_cb,
            'connect_coro':  self.__connect_coro,
            'ssid':          self.config["ssid"],
            'wifi_pw':       self.config["wifi_pw"],
            'port':          self.config["port"] or 1883,
            'user':          self.config["user"],
            'password':      self.config["password"],
            'keepalive':     self.config["keepalive"] or 10,
            'ping_interval': self.config["ping_interval"] or 5,
            'ssl':           False,
            'ssl_params':    {},
            'response_time': self.config["response_time"] or 10,
            'clean_init':    True,
            'clean':         True,
            'max_repubs':    self.config["max_repubs"] or 4,
            'will':          ['status/offline',ujson.dumps({"data": self.config["client_id"]}), False],
            'wifi_coro':     self.__wifi_coro,
            'queue_len': 0
        })

        try:
            self.set_client(client)
            await client.connect()

            # Non-terminating event 
            while True:
                await asyncio.sleep(1)

        finally:
            client.close()

        
