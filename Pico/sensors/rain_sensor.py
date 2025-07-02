from config import load_config
from umqtt.simple import MQTTClient
import machine, time, json

cfg = load_config()
adc = machine.ADC(28)

def read_and_publish():
    value = adc.read_u16()
    raining = value < 30000

    client = MQTTClient(
        client_id=cfg["client_id"],
        server=cfg["mqtt_broker"],
        port=cfg["mqtt_port"],
        user=cfg["username"],
        password=cfg["password"]
    )

    client.connect()
    client.publish(f"garden/sensor/{cfg['sensor_name']}/rain_detected", json.dumps({
        "value": raining
    }))
    client.disconnect()

while True:
    read_and_publish()
    time.sleep(300)
