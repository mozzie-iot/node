# This file should exist as 'client.py' in project root

import machine
import onewire 
import ds18x20
import uasyncio as asyncio

from node import NodeCore

# VARIABLES
DATA_PIN = 4
PUBLISH_INTERVAL = 15 

class NodeClient(NodeCore):
    _pin = machine.Pin(DATA_PIN)
    _node = ds18x20.DS18X20(onewire.OneWire(_pin))

    async def connected_cb(self, client):
        asyncio.create_task(self.get_temperature())

    async def get_temperature(self):
        while True: 
            roms = NodeClient._node.scan()
            NodeClient._node.convert_temp()
            
            for rom in roms:
                temp = NodeClient._node.read_temp(rom)

                if isinstance(temp, float):
                    measurement = round(temp, 2)
                    await self.client.publish(f"sensor/{self.config['client_id']}", f"{measurement}")
                else:
                    await self.client.publish(f"sensor/{self.config['client_id']}", "0.0")

            await asyncio.sleep(PUBLISH_INTERVAL)