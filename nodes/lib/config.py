import json

def load_config(filename="config.json"):
    with open(filename, "r") as f:
        config = json.load(f)

    sensor_name = config.get("sensor_name", "default_sensor")
    mqtt_cfg = config.get("mqtt", {})
    relays = config.get("relays", {})
    flow_sensors = config.get("flow_sensors", {})

    return {
        "sensor_name": sensor_name,
        "mqtt_broker": mqtt_cfg.get("broker", "localhost"),
        "mqtt_port": mqtt_cfg.get("port", 1883),
        "client_id": mqtt_cfg.get("client_id", f"{sensor_name}_client"),
        "username": mqtt_cfg.get("username", ""),
        "password": mqtt_cfg.get("password", ""),
        "relays": relays,
        "flow_sensors": flow_sensors
    }

