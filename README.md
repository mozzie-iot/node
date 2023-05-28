## Description
A MicroPython MQTT client for WiFi enabled microcontrollers to communicate in the Huebot environment
<br><br>
Most of the credit for the Huebot node functionality goes to [MicroPython](https://github.com/micropython/micropython) and, more specifically, [MicroPython Asynchronous MQTT](https://github.com/peterhinch/micropython-mqtt/tree/master/mqtt_as)

<br>

## Getting Started
**Two options - Quick Setup or Development Setup**

### Quick Setup
Source files and functionality baked into the firmware
1. Follow board-specific setup/installation instructions *but use the latest [Huebot firmware](https://github.com/huebot-iot/node/releases/latest) build in releases instead of MicroPython firmware*
    - [ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
2. Create [client.py](https://github.com/huebot-iot/node/blob/main/README.md#clientpy) and [config.json](https://github.com/huebot-iot/node/blob/main/README.md#configjson) files in root directory
3. Upload files to the MCU. This might require some Googling depending on the board. We've found success using the [PyMakr extension](https://github.com/pycom/pymakr-vsc) in VScode with the ESP32 (see more [below](https://github.com/huebot-iot/node/blob/main/README.md#pymakr-configuration)).
4. Setup MCU on breadboard per schematic to take advantage of LED status indicator
    - [ESP32](https://github.com/huebot-iot/node/blob/main/README.md#esp32)

### Development Setup
Ability to view/edit source files
1. Flash MCU with MicroPython using board-specific setup/installation instructions 
    - [ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
2. Clone this repo 
3. In the src create the [client.py](https://github.com/huebot-iot/node/blob/main/README.md#clientpy) and [config.json](https://github.com/huebot-iot/node/blob/main/README.md#configjson) files
4. Upload files to the MCU. This might require some Googling depending on the board. We've found success using the [PyMakr extension](https://github.com/pycom/pymakr-vsc) in VScode with the ESP32 (see more [below](https://github.com/huebot-iot/node/blob/main/README.md#pymakr-configuration)).
5. Setup MCU on breadboard per schematic to take advantage of LED status indicator
    - [ESP32](https://github.com/huebot-iot/node/blob/main/README.md#esp32)

<br>

## client.py
This file is tasked with core node functionality; equipped the MQTT client property and status callbacks.

### Boilerplate

```
from node import NodeCore

class NodeClient(NodeCore):
```

### Properties
<b>client</b> [[MQTTClient class](https://github.com/peterhinch/micropython-mqtt/blob/master/mqtt_as/README.md#3-mqttclient-class)] access to MQTT client methods (notably `client.publish`)

### Methods
<b>connected_cb</b> Called when connection to broker is estbalished. Recieves the `client` instance as an argument.
<br>
<b>disconnected_cb</b> Called when connection to broker is lost. 
<br>
<b>subscribe_cb</b> Called when a message is received that matches topic subscription. Receives arguments `topic`, `message`, and `retained`.

<br>

## config.json
MQTT configuration settings. Use `config-sample.json` as a template.
<br>

```
{
  "client_id": "", // Unique ID identifying device
  "server": "", // Huebot hub IP address or name (if DNS is configured)
  "ssid": "", // WiFi network name (must be on same network as hub)
  "wifi_pw": "", // WiFI network password
  "port": null, // MQTT broker port on hub (default: 1883)
  "user": "", // MQTT broker username
  "password": "", // MQTT broker password
  "keepalive": null, // Per mqtt_as docs: 'Period (secs) before broker regards client as having died' (default: 10)
  "ping_interval": null, // Per mqtt_as docs: 'Period (secs) between broker pings' (default: 5)
  "response_time": null, // Per mqtt_as docs: 'Time in which server is expected to respond' (default: 10)
  "max_repubs": null // Per mqtt_as docs: 'Maximum no. of republications before reconnection is attempted' (default: 4)
}

```

<br>

## Base Schematic
### ESP32
![core schematic](https://github.com/huebot-iot/node/assets/8736328/289aeaa0-d72a-49ac-ae95-237afb306a97)

<br>

## PyMakr Configuration
If using PyMakr for MCU development and file uploading, here are the settings recommended for the `pymakr.conf` file:

```
{
  "py_ignore": [
    ".vscode",
    ".gitignore",
    ".git",
    "config-sample.json"
  ],
  "name": "temp-sensor", // Anything you want here 
  "dist_dir": "src" // Omit this property if using the "Quick Setup"
}

```

<br>

## License
Huebot is [GPLv3 licensed](LICENSE).
