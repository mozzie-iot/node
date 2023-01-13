# Huebot Node Micropython ESP32 Port

## Setup

- Pymakr extension for VS code is recommended
- Drop in `client.py` on `src` directory

## client.py

Ideally this is the only file that should be edited when developing a custom node - all other code is considered to be 'core'.

### Requirements

- `NodeClient` class with either `OutputClient` or `InputClient` as the parent class. See below for API detail.
- `api_key` is a required property of `NodeClient`. This is the node model api key.

## API

### OutputClient

#### async def on_state_update(self, channel, state):

- required method
- params:
  - channel: node channel getting updated
  - state: ["on" | "off", duty_cycle (int)]

## Example (client.py)

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
