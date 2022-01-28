import uasyncio as asyncio

from node.lib.mqtt_as import MQTT_AS_Client, eliza
from node.utils.logger import Log
import node.constants as constants

from client import NodeClient

class MQTTClient(NodeClient):
    def __init__(self, system):
        super().__init__()
        self.system = system
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

    async def routine(self):
        config = self.system.config
        MQTT_AS_Client.DEBUG = True
        self.__client  = MQTT_AS_Client({
            'client_id':     "{0}:{1}".format(config["type"], config["secret_key"]),
            'server':        config["ap"]["ip"],
            'subs_cb':       self.__subscribe,
            'connect_coro':  self.__conn_han,
            'ssid':          config["ap"]["ssid"],
            'wifi_pw':       config["ap"]["pw"],
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
            'will':          ['status/offline/{}'.format(config["secret_key"]),'', False],
            'wifi_coro':     eliza
        })

        try:
            self.system.event(constants.SYSTEM_SETUP)
            await self.__client.connect()

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
            self.system.event(constants.SYSTEM_ERROR)
            Log.error("MQTT.routine", "Failed to connect", e)
            # broker not available
            await asyncio.create_task(self.system.restart(5))

        
