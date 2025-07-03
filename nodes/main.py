import sys
sys.path.append("lib")

from config import load_config
from mqtt_helper import connect_mqtt
from ota_updater import fetch_remote_version, update_if_needed

import RPi.GPIO as GPIO
import time
import json

# OTA update check
ota_info = fetch_remote_version("http://<pi-ip>:8000/remote_version.json")
if ota_info:
    update_if_needed(ota_info)

cfg = load_config()
node_name = cfg["sensor_name"]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup relays
relays = {}
for alias, pin_num in cfg["relays"].items():
    GPIO.setup(pin_num, GPIO.OUT)
    GPIO.output(pin_num, GPIO.HIGH)  # default OFF
    relays[alias] = pin_num

# Setup flow sensors (optional)
flow_sensors = {}
for alias, pin_num in cfg.get("flow_sensors", {}).items():
    GPIO.setup(pin_num, GPIO.IN)
    flow_sensors[alias] = pin_num

def set_relay(alias, state):
    if alias in relays:
        GPIO.output(relays[alias], GPIO.LOW if state else GPIO.HIGH)

def get_relay_states():
    return {
        alias: "on" if GPIO.input(pin) == GPIO.LOW else "off"
        for alias, pin in relays.items()
    }

def get_flow_states():
    return {
        f"{alias}_flow": "yes" if GPIO.input(pin) == GPIO.LOW else "no"
        for alias, pin in flow_sensors.items()
    }

def message_callback(topic, payload):
    try:
        msg = json.loads(payload)
        alias = msg.get("channel")
        state = msg.get("state")
        if alias in relays and state in ["on", "off"]:
            set_relay(alias, state == "on")
            print(f"Relay {alias} set to {state}")
    except Exception as e:
        print("MQTT command error:", e)

# MQTT setup
mqtt = connect_mqtt(cfg)
mqtt.set_callback(message_callback)
mqtt.connect()
mqtt.subscribe(f"garden/command/{node_name}/relay")

def publish_status():
    status = {**get_relay_states(), **get_flow_states()}
    mqtt.publish(f"garden/status/{node_name}/relay", json.dumps(status))

print(f"[{node_name}] Node online and ready.")

# Main loop
try:
    while True:
        mqtt.check_msg()
        publish_status()
        time.sleep(10)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Node shutdown.")
