import json
import logging
import utime
import umqtt.simple as mqtt

class MQTTClient:
    def __init__(self, client_id, mqtt_server, topic_pub):
        self.client_id = client_id
        self.mqtt_server = mqtt_server
        self.topic_pub = topic_pub
        self.client = mqtt.MQTTClient(self.client_id, self.mqtt_server)
        self.sunrise = None
        self.sunset = None

    def connect(self, username, password):
        try:
            self.client.connect(user=username, password=password)
            logging.info('Connected to MQTT Broker')
            self.client.subscribe("garden/sunrise_sunset")
        except Exception as e:
            logging.error(f"Failed to connect to MQTT Broker: {e}")

    def publish(self, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            self.client.publish(self.topic_pub, message)
            logging.info(f'Published: {message}')
        except Exception as e:
            logging.error(f"Error publishing message: {e}")
            self.reconnect()

    def reconnect(self):
        """Reconnect to the MQTT broker."""
        for attempt in range(3):
            try:
                self.client.connect()
                logging.info("MQTT reconnected successfully")
                return
            except Exception as e:
                logging.warning(f"MQTT reconnection attempt {attempt + 1} failed: {e}")
                utime.sleep(2 ** attempt)
        logging.error("Unable to reconnect to MQTT Broker")

    def on_message(self, topic, msg):
        if topic == b'garden/sunrise_sunset':
            data = json.loads(msg)
            self.sunrise = data['sunrise']
            self.sunset = data['sunset']
            logging.info(f"Received sunrise: {self.sunrise}, sunset: {self.sunset}")
