import ujson
import ubluetooth as bt
from micropython import const
from uasyncio import Event
import struct

import node.core.constants as constants
from node.core.utils.logger import Log
import node.core.utils.ble_codes as ble_codes

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)

_SERVICE_UUID = bt.UUID(constants.BLE_SERVICE_UUID)
_CHAR_RX = (bt.UUID(constants.BLE_CHAR_RX_UUID), bt.FLAG_WRITE_NO_RESPONSE | bt.FLAG_NOTIFY,)
_SERVICE = (_SERVICE_UUID, (_CHAR_RX,),)
SERVICES = (_SERVICE,)

class Ble:
    def __init__(self, system):
        self.__system = system
        self.__ble = bt.BLE()
        self.__ble.active(True)
        self.__ble.config(gap_name=constants.BLE_NAME)
        ((self.__handle_rx, ), ) = self.__ble.gatts_register_services(SERVICES)
        self.__ble.gatts_set_buffer(self.__handle_rx, 150, True)
        self.__ble.irq(self.__irq)
        self.__connections = set()
        self.__is_connected = Event()
        self.__is_setup = False
       
    @staticmethod
    def advertising_payload(limited_disc=False, br_edr=False, name=None):
        payload = bytearray()

        def _append(adv_type, value):
            nonlocal payload
            payload += struct.pack('BB', len(value) + 1, adv_type) + value

        _append(_ADV_TYPE_FLAGS, struct.pack('B', (0x01 if limited_disc else 0x02) + (0x00 if br_edr else 0x04)))
        _append(_ADV_TYPE_NAME, name)

        return payload

    def __handle_actions(self):
        try: 
            buffer = self.__ble.gatts_read(self.__handle_rx)
            string = buffer.decode('UTF-8').strip()
            obj = ujson.loads(string)
            action = obj["action"]
            payload = obj["payload"]

            Log.info("Ble.__handle_actions", "ACTION: {0}, PAYLOAD: {1}".format(action, payload))

            if action == "auth":
                data = ujson.dumps({"public_key": self.__system.config["public_key"]}) 
                self.__write(data)
            elif action == "setup":
                self.__system.set_config(payload)
                data = ujson.dumps({"secret_key": self.__system.config["secret_key"]}) 
                self.__write(data)
            elif action == "complete":
                # based on success of hub setup, reset if fail
                if payload == "success":
                    self.__is_setup = True
                    # Make ble event terminating, move to mqtt
                    self.__is_connected.set()
                    
                elif payload == "error":
                    # Clear ap credentials, start advertising
                    self.__system.set_config(None)
                    self.__advertise(100)
                else:
                    raise Exception("Invalid 'complete' action payload: {}".format(payload))
            else:
                raise Exception("Invalid setup action")

        except Exception as e:
            Log.error("Ble.__handle_actions", "failed to handle ble write", e)

    def __irq(self, event, data):
        Log.info("Ble.__irq", "event: {}".format(ble_codes.event_dict[event]))
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _, = data
            self.__connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _, = data
            self.__connections.remove(conn_handle)
            if not self.__is_setup: 
                self.__advertise(100)
        elif event == _IRQ_GATTS_WRITE:
            self.__handle_actions()

    def __write(self, data):
        self.__ble.gatts_notify(0, self.__handle_rx, data + '\n')
    
    def __advertise(self, interval):
        payload = Ble.advertising_payload(name=constants.BLE_NAME)
        self.__ble.gap_advertise(interval, adv_data=payload, connectable=True)
        
    async def routine(self):
        self.__advertise(100)
        await self.__is_connected.wait()