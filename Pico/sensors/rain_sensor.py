from config import load_config
from mqtt_helper import connect_mqtt
import machine, time, json

cfg = load_config()
adc = machine.ADC(28)

def read_and_publish():
    value = adc.read_u16()
    is_raining = value < 30000  # Adjust based on sensor curve

    client = connect_mqtt(cfg)
    client.connect()
    client.publish(
        f"garden/sensor/{cfg['sensor_name']}/rain_detected",
        json.dumps({"value": is_raining})
    )
    client.disconnect()

while True:
    read_and_publish()
    time.sleep(300)
