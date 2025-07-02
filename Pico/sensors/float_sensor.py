import sys
sys.path.append("/lib")  # Tell MicroPython where to look

from config import load_config
from mqtt_helper import connect_mqtt
from ota_updater import fetch_remote_version, update_if_needed
import machine, time, json

cfg = load_config()
pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

def read_and_publish():
    full = pin.value() == 0
    level = "full" if full else "low"

    client = connect_mqtt(cfg)
    client.connect()
    client.publish(
        f"garden/sensor/{cfg['sensor_name']}/water_level",
        json.dumps({"value": level})
    )
    client.disconnect()

while True:
    read_and_publish()
    time.sleep(300)
