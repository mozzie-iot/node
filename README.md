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

## Huebot Environment
- **Important:** In order to obtain sensor readings from the HTTP endpoint ([server]/node/sensor) they must be published to topic "sensor/[client_id]". Also, the payload must be a string. 

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
<b>config</b> Access to settings in `config.json`. Mostly used to reference `client_id`.

### Methods
<b>connected_cb</b> Asynchronous. Called when connection to broker is estbalished. Recieves the `client` instance as an argument.
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

### Supplies
This supplies list points to Amazon for simplicity but they can certainly be found eslewhere!
- [ESP32](https://www.amazon.com/KeeYees-Development-Bluetooth-Microcontroller-ESP-WROOM-32/dp/B07QCP2451/ref=d_pd_di_sccai_cn_sccl_2_1/145-1624382-0187119?pd_rd_w=Os7VE&content-id=amzn1.sym.e13de93e-5518-4644-8e6b-4ee5f2e0b062&pf_rd_p=e13de93e-5518-4644-8e6b-4ee5f2e0b062&pf_rd_r=K6DEVWWDGGP0H822W8YB&pd_rd_wg=JVwyk&pd_rd_r=4898c4b7-7dde-4af4-a9a1-41a528af7373&pd_rd_i=B07QCP2451&th=1)
- [Breadboards](https://www.amazon.com/Pcs-MCIGICM-Points-Solderless-Breadboard/dp/B07PCJP9DY/ref=sr_1_4?crid=2198DX37ZIMM5&keywords=breadboard&qid=1685540187&sprefix=breadboard+%2Caps%2C193&sr=8-4)
- [Jumper wires](https://www.amazon.com/AUSTOR-Lengths-Assorted-Preformed-Breadboard/dp/B07CJYSL2T/ref=sr_1_4?keywords=breadboard+jumper+wires&qid=1685540223&sprefix=breadboard+jumpe%2Caps%2C149&sr=8-4)
- [RGB multicolor LED](https://www.amazon.com/Tricolor-Multicolor-Lighting-Electronics-Components/dp/B01C19ENFK/ref=sr_1_1_sspa?crid=1VRXY3B140ITQ&keywords=multicolor%2Bled&qid=1685539952&sprefix=multicolor%2Bled%2Caps%2C221&sr=8-1-spons&smid=A14FP9XIRL6C1F&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExVU5CTFdQRlhSQ0o3JmVuY3J5cHRlZElkPUEwODIxODEyMTFET1ZUREMwU1dCMSZlbmNyeXB0ZWRBZElkPUEwMTEyNzY4MVdCOVI0VjdUVE4wWiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1)
- [~500 ohm resistors](https://www.amazon.com/EDGELEC-Resistor-Tolerance-Multiple-Resistance/dp/B07QK8VRZX/ref=sxin_16_ac_d_bv?ac_md=0-0-QnVkZ2V0IFBpY2s%3D-ac_d_bv_bv_bv&content-id=amzn1.sym.8f2bf95d-b9c2-4e6d-96a9-5fdf77a1951d%3Aamzn1.sym.8f2bf95d-b9c2-4e6d-96a9-5fdf77a1951d&cv_ct_cx=500+ohm+resistor&keywords=500+ohm+resistor&pd_rd_i=B07QK8VRZX&pd_rd_r=92d5e2d7-de0b-4ca4-b96f-f3f1aa74d18c&pd_rd_w=Dk8KR&pd_rd_wg=8TvPz&pf_rd_p=8f2bf95d-b9c2-4e6d-96a9-5fdf77a1951d&pf_rd_r=VMBTMBHK42Y9FFC2GY7M&qid=1685540398&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=500ohm+res%2Caps%2C243&sr=1-1-270ce31b-afa8-499f-878b-3bb461a9a5a6)

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
