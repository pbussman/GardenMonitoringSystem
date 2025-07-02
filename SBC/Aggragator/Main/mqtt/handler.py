import paho.mqtt.client as mqtt
import json
import re
import logging

TOPIC_PATTERN = re.compile(r"^garden/(sensor|actuator|status)/([^/]+)/([^/]+)$")

class MQTTHandler:
    def __init__(self, client_id, server, username, password, db_manager, weather_fetcher):
        self.client = mqtt.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.server = server
        self.db = db_manager
        self.weather = weather_fetcher

    def start(self):
        self.client.connect(self.server, 1883, 60)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected to MQTT broker.")
        self.client.subscribe("garden/#")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        if not TOPIC_PATTERN.match(topic):
            logging.warning(f"Invalid topic format: {topic}")
            return

        timestamp = datetime.utcnow().isoformat()
        self.db.store_sensor_reading(topic, payload, timestamp)

    def publish_command(self, zone, command_obj):
        topic = f"garden/command/{zone}/relay"
        self.client.publish(topic, json.dumps(command_obj))

    def publish_advice(self, zone, advice_obj):
        topic = f"garden/advice/{zone}/irrigation"
        self.client.publish(topic, json.dumps(advice_obj))

    def process_command_queue(self):
        commands = self.db.get_pending_commands()
        for cmd in commands:
            self.publish_command(cmd['zone'], json.loads(cmd['command']))
            self.db.mark_command_complete(cmd['id'])
