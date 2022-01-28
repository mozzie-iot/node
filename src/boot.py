from node.core.utils.uuid import uuid4
from node.core.utils.fs import read, write
import node.core.interface.led as led
from node.core.utils.logger import Log

from client import NodeClient

led.boot()
Log.info("system", "booting up!")

def get_config():

    def get_node_type(node):
        for base in node.__class__.__bases__:
            if base.__name__ == "InputClient":
                return "input"
            elif base.__name__ == "OutputClient":
                return "output"
            else:
                return None

    try:
        file = read()
        return file
    except:
        node = NodeClient()
        # initial boot or reset
        type = get_node_type(node)
        public_key = getattr(node, 'public_key')
        
        try:
            # Setup config validation
            if type is None:
                raise Exception("Failed to determine node type - node client must inherit either InputMQTT or OutputMQTT")
            
            if public_key is None:
                raise Exception("Node client 'public_key' not set")

            # Save as string
            secret_key = str(uuid4())

            config = {
                "type": type, 
                "public_key": public_key, 
                "secret_key": secret_key, 
                "ap": None
            }
            write(config)

            return config
        except Exception as e:
            led.error()
            Log.error("Boot", "config failed", e)
            return None

config = get_config()