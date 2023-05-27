from utils.fs import read
from interface.led import LED
from utils.logger import Log

led = LED()
led.blue()
Log.info("system", "booting up!")

def get_config():
    try:
        file = read()
        return file
    except:
        led.red()
        Log.error("Boot", "config.json not found")
        return None

config = get_config()

print("Config: ", config)