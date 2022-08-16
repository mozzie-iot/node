import uasyncio as asyncio

from node.core.lib.mqtt_as import MQTT_AS_Client, eliza
from node.core.utils.logger import Log
import node.core.constants as constants

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
        topic = 'status/online/{}'.format(config["secret_key"])
        await self.__on_publish(topic, '')

    async def __conn_han(self, client):
        config = self.system.config
        sub_topic = "node/{}".format(config["secret_key"])
        await client.subscribe("alive_check", 0)
        Log.info("MQTT.__conn_han", "Subscription topic: {}".format(sub_topic))
        await client.subscribe(sub_topic, 1)
        await self.__node_online()

    def __subscribe(self, topic, payload, retained):
        Log.info("MQTT.subscribe", "topic:{0}, payload:{1}, retained:{2}".format(topic, payload, retained))
        decodedTopic = topic.decode("utf-8")

        if decodedTopic == "alive_check":
            asyncio.create_task(self.__node_online())
            return
        
        self.incoming(decodedTopic, payload, retained)

    async def __wifi_coro(self, network_state):
        if not network_state:
            self.led.pulse("red")


    async def routine(self):
        config = self.system.config
        MQTT_AS_Client.DEBUG = True
        self.__client  = MQTT_AS_Client({
            # 'client_id':     "{0}:{1}".format(config["type"], config["secret_key"]),
            'client_id':     "Output:123",
            # 'server':        config["ap"]["ip"],
            'server':        '',
            'subs_cb':       self.__subscribe,
            'connect_coro':  self.__conn_han,
            # 'ssid':          config["ap"]["ssid"],
            'ssid':          '',
            # 'wifi_pw':       config["ap"]["pw"],
            'wifi_pw':       '',
            'port':          1883,
            'user':          '',
            'password':      '',
            'keepalive':     60,
            'ping_interval': 10,
            'ssl':           False,
            'ssl_params':    {},
            'response_time': 10,
            'clean_init':    True,
            'clean':         True,
            'max_repubs':    4,
            # 'will':          ['status/offline/{}'.format(config["secret_key"]),'', False],
            'will':          ['status/offline/test','', False],
            'wifi_coro':     self.__wifi_coro
        })

        try:
            self.led.green()
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
            
            # Non terminating
            await asyncio.create_task(self.node_routine())
        except Exception as e:
            self.led.pulse("red")
            Log.error("MQTT.routine", "Failed to connect", e)
            # broker not available
            await asyncio.create_task(self.system.restart(5))

        
