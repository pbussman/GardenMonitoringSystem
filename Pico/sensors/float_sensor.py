from config import load_config
from umqtt.simple import MQTTClient
import machine, time, json

cfg = load_config()
pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

def read_and_publish():
    state = pin.value() == 0  # 0 = submerged, float activated
    level = "full" if state else "low"

    client = MQTTClient(
        client_id=cfg["client_id"],
        server=cfg["mqtt_broker"],
        port=cfg["mqtt_port"],
        user=cfg["username"],
        password=cfg["password"]
    )

    client.connect()
    client.publish(f"garden/sensor/{cfg['sensor_name']}/water_level", json.dumps({
        "value": level
    }))
    client.disconnect()

while True:
    read_and_publish()
    time.sleep(300)
