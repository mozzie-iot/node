# Huebot Node Micropython ESP32 Port

## Development

### Flashing ESP32 with MicroPython

This setup has only been tested on Mac

#### Requirements

- ESPTool (I think I installed with Homebrew)
- Download the latest [ESP32 MicroPython firmware](https://micropython.org/download/esp32/) (.bin file)

#### Steps

1. Connect ESP32 to computer with USB to Micro USB data cable (Make sure the cable has data transfer ability and not just a charging cable - this is known to trip folks up)
2. Identiy the serial connection port: `ls /dev/tty.usbserial*`
3. Reset the device to ensure we are working with a clean slate: `esptool.py --port [serial port] erase_flash`
4. Install firmware on device: `esptool.py --chip ESP32 --port [serial port] write_flash -z 0x1000 [path to MicroPython firmware]`

### PyMakr Setup

To do...

### client.py

Ideally this is the only file that should be edited when developing a custom node - all other code is considered to be 'core'.
<b>Requires either `OutputClient` or `InputClient` as parent class</b>

### Properties

<b>'api_key'</b> [`uuid`] generated when creating model (required)

### Methods

#### on_disconnect (optional)

Called when node loses connection with the broker.

### Output Only Methods

#### on_state_update (required)

Asynchronous.

Called when when either topic 'node/[instance_key]' (payload has 'action' key) is published by another client or when node connects to broker

Args:

1. `channel` node channel getting updated
2. `state` "on" | "off", duty_cycle (int)]

### Example

4 Channel relay with a normally open config

```
from machine import Pin

from node.output import OutputClient
from node.core.utils.logger import Log

class NodeClient(OutputClient):
    api_key = "c42b4651-e410-47ad-af3b-c47854fa4d63"

    channels = {
        1: {"pin": 18},
        2: {"pin": 19},
        3: {"pin": 21},
        4: {"pin": 22}
    }

    async def on_state_update(self, channel, state):
        pin = NodeClient.channels[int(channel)]["pin"]
        Log.info("NodeClient.on_state_update", "pin:{0} state:{1}".format(pin, state))
        relay = Pin(pin, Pin.OUT)
        num_status = 0 if state[0] == "on" else 1 # setup for normally open config
        relay.value(num_status)


```

## Core Schematic

![base_fritz](https://user-images.githubusercontent.com/8736328/212395999-e01645ff-3b16-40e3-815f-353ec8023aa0.jpg)
