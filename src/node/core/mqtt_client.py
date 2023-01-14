import uasyncio as asyncio
import ujson

from node.core.lib.mqtt_as import MQTT_AS_Client, eliza
from node.core.utils.logger import Log

from client import NodeClient

class MQTTClient(NodeClient):
    def __init__(self, system, led):
        super().__init__()
        self.system = system
        self.led = led
        self.__client = None

    async def __on_publish(self, topic, msg):
        await self.__client.publish(topic, msg, qos = 0)


    async def __node_online(self):
        Log.info("MQTT.__node_online", "Publish Node Online")
        config = self.system.config

        # note: need id to get response and nestjs doesn't expose id
        # we set data as secret too
        payload = {
            "id": config["secret_key"],
            "data": config["secret_key"]
        }

        await self.__on_publish('status/online', ujson.dumps(payload))

    async def __conn_han(self, client):
        self.led.green()

        secret = self.system.config["secret_key"]

        # Set custom node settings
        await client.subscribe(f"node/{secret}/settings", 1)
        
        # Update node state
        await client.subscribe(f"node/{secret}/state", 1)

        # If broker or transporter go down, they will publish 'alive_check' when 
        # back up - mostly relevant for hot reloading in development
        await client.subscribe("alive_check", 0)

        # Responds to node online alert with status detail to sync hub/node
        await client.subscribe("status/online/reply", 0)
       
        # After subscribing to topics, let broker know we are ready
        await self.__node_online()

    def __subscribe(self, topic, payload, retained):
        Log.info("MQTT.subscribe", "topic:{0}, payload:{1}, retained:{2}".format(topic, payload, retained))
        decodedTopic = topic.decode("utf-8")
        decodedPayload = payload.decode("utf-8");
        payloadDict = ujson.loads(decodedPayload)

        if decodedTopic == "alive_check":
            asyncio.create_task(self.__node_online())
            return

        if decodedTopic == "status/online/reply":
            # Set node state
            channels = payloadDict["response"]
            for key, value in channels.items():
                asyncio.create_task(self.on_state_update(key, value))                   

            return
        
        self.incoming(decodedTopic, payloadDict, retained)

    async def __wifi_coro(self, network_state):
        if not network_state:
            self.on_disconnect()
            self.led.pulse("red")


    async def routine(self):
        config = self.system.config
        MQTT_AS_Client.DEBUG = True
        self.__client  = MQTT_AS_Client({
            'client_id':     config["secret_key"],
            'server':        'hub.huebot',
            'subs_cb':       self.__subscribe,
            'connect_coro':  self.__conn_han,
            'ssid':          config["ap"]["ssid"],
            'wifi_pw':       config["ap"]["pw"],
            'port':          1883,
            'user':          config["mqtt"]["un"],
            'password':      config["mqtt"]["pw"],
            'keepalive':     10,
            'ping_interval': 5,
            'ssl':           False,
            'ssl_params':    {},
            'response_time': 10,
            'clean_init':    True,
            'clean':         True,
            'max_repubs':    4,
            'will':          ['status/offline',ujson.dumps({"data": config["secret_key"]}), False],
            'wifi_coro':     self.__wifi_coro
        })

        try:
            Log.info("MQTT.routine", "Init")
            await self.__client.connect()
            Log.info("MQTT.routine", "Successful network connection")

            if hasattr(super(), 'set_publish'):
                self.set_publish(self.__on_publish)

            if hasattr(super(), 'set_on_settings_fn'):
                self.set_on_settings_fn(self.on_settings)

            # Input only methods
            if hasattr(super(), 'set_on_active_state_fn'):
                self.set_on_active_state_fn(self.on_active_state)

            # Output only methods
            if hasattr(super(), 'set_on_state_update_fn'):
                self.set_on_state_update_fn(self.on_state_update)  

        except Exception as e:
            self.led.pulse("red")
            Log.error("MQTT.routine", "Failed to connect", e)
            # broker not available
            await asyncio.create_task(self.system.restart(5))

        
