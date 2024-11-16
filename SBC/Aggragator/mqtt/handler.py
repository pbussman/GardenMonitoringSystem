import paho.mqtt.client as mqtt
import json
import logging
from datetime import datetime

class MQTTHandler:
    def __init__(self, client_id, server, username, password, db_manager, weather_fetcher):
        self.client = mqtt.Client(client_id=client_id)
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(server)
        self.db_manager = db_manager
        self.weather_fetcher = weather_fetcher

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected to MQTT Broker")
        client.subscribe("water_tank/sensors")
        client.subscribe("garden/logs")  # Subscribe to the logs topic

    def on_message(self, client, userdata, msg):
        logging.info(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        if msg.topic == "garden/logs":
            with open('pi5_log.log', 'a') as log_file:
                log_file.write(f"{datetime.now()} - {msg.payload.decode()}\n")
        else:
            sensor_data = json.loads(msg.payload.decode())
            for barrel, sensors in sensor_data.items():
                self.db_manager.insert_float_sensor_reading(barrel, sensors)
            
            weather_data = self.weather_fetcher.fetch_weather_data()
            if weather_data:
                self.db_manager.insert_weather_data(weather_data)
                self.publish_sunrise_sunset(weather_data['sunrise'], weather_data['sunset'])

    def publish_sunrise_sunset(self, sunrise, sunset):
        data = {
            'sunrise': sunrise,
            'sunset': sunset
        }
        self.client.publish("garden/sunrise_sunset", json.dumps(data))

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
