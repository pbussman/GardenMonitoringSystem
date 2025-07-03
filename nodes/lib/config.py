# config.py

import json

def load_config(filename="config.json"):
    with open(filename, "r") as f:
        config = json.load(f)

    sensor_name = config.get("sensor_name", "default_sensor")
    mqtt = config.get("mqtt", {})
    mqtt_broker = mqtt.get("broker", "localhost")
    mqtt_port = mqtt.get("port", 1883)
    client_id = mqtt.get("client_id", f"{sensor_name}_client")
    username = mqtt.get("username", "")
    password = mqtt.get("password", "")

    return {
        "sensor_name": sensor_name,
        "mqtt_broker": mqtt_broker,
        "mqtt_port": mqtt_port,
        "client_id": client_id,
        "username": username,
        "password": password
    }
