from node.core.utils.fs import read
from node.core.interface.led import LED
from node.core.utils.logger import Log

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
        led.red()
        Log.error("Boot", "config.json not found")
        return None

config = get_config()

print("Config: ", config)