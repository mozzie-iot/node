import sys
import uasyncio as asyncio
import ujson
import machine

from lib.mqtt_as import MQTT_AS_Client
from utils.logger import Log

from client import NodeClient

class MQTTClient(NodeClient):
    def __init__(self, config, led):
        super().__init__()
        self.config = config
        self.led = led

    # Format required by NestJS MQTT transporter
    def __subscribe_resp(self, topic, transaction_id, message):
        responsePayload = ujson.dumps({
            "response": message, 
            "id": transaction_id,
            "isDisposed": True
        })
        asyncio.create_task(self.__publish("{}/reply".format(topic), responsePayload))

    async def __node_online(self, client):
        Log.info("MQTT.__node_online", "Publish Node Online")

        # note: need id to get response and nestjs doesn't expose id
        # we set data as client_id too
        payload = {
            "id": self.config["client_id"],
            "data": self.config["client_id"]
        }

        await client.publish('status/online', ujson.dumps(payload))



    async def __connect_coro(self, client):
        self.led.green()

        if hasattr(super(), 'connected_cb'):
            self.connected_cb(client)

        # If broker or transporter go down, they will publish 'alive_check' when 
        # back up - mostly relevant for hot reloading in development
        await client.subscribe("alive_check", 0)

        # Responds to node online alert with status detail to sync hub/node
        await client.subscribe("status/online/reply", 0)
       
        # After subscribing to topics, let broker know we are ready
        await self.__node_online(client)

    def __subs_cb(self, topic, payload, retained):
        try:
            Log.info("MQTT.subscribe", "topic:{0}, payload:{1}, retained:{2}".format(topic, payload, retained))
            decodedTopic = topic.decode("utf-8")

            if decodedTopic == "alive_check":
                asyncio.create_task(self.__node_online())
                return
            
            if hasattr(super(), 'subscribe_cb'):
                self.subscribe_cb(topic, payload, retained)

            self.__subscribe_resp(topic, payload["id"], "received")
                
        except Exception as e:
            Log.error("MQTTClient", "__subscribe", e)
            self.led.red(False)
            sys.exit()

    async def __wifi_coro(self, network_state):
        if not network_state:
            self.on_disconnect()
            self.led.pulse("red")

    async def routine(self):
        MQTT_AS_Client.DEBUG = True
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
            'wifi_coro':     self.__wifi_coro
        })

        try:
            Log.info("MQTT.routine", "Init")
            await client.connect()
            Log.info("MQTT.routine", "Successful network connection")

            self.set_client(client)

        except Exception as e:
            self.led.pulse("red")
            Log.error("MQTT.routine", "Failed to connect", e)
            # broker not available
            await asyncio.sleep(5)
            machine.reset()

        
