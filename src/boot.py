from node.core.utils.uuid import uuid4
from node.core.utils.fs import read, write
from node.core.interface.led import LED
from node.core.utils.logger import Log

from client import NodeClient

led = LED()
led.blue()
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
        api_key = getattr(node, 'api_key')
        
        try:
            # Setup config validation
            if type is None:
                raise Exception("Failed to determine node type - node client must inherit either InputMQTT or OutputMQTT")
            
            if api_key is None:
                raise Exception("Node client 'api_key' not set")

            # Save as string
            secret_key = str(uuid4())

            config = {
                "type": type, 
                "api_key": api_key, 
                "secret_key": secret_key, 
                "ap": None
            }
            write(config)

            return config
        except Exception as e:
            led.red()
            Log.error("Boot", "config failed", e)
            return None

config = get_config()

print("Config deets: ", config)