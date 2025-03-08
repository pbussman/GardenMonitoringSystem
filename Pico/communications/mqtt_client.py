import umqtt.simple as mqtt
import secrets
import logging

# Define the MQTT Client class
class MQTTClient:
    def __init__(self, client_id, mqtt_server, topic_pub):
        self.client_id = client_id
        self.mqtt_server = mqtt_server
        self.topic_pub = topic_pub
        self.client = mqtt.MQTTClient(self.client_id, self.mqtt_server)
        self.connected = False  # Track connection state

    def connect(self):
        try:
            self.client.connect(user=secrets.MQTT_USERNAME, password=secrets.MQTT_PASSWORD)
            self.connected = True
            logging.info('Connected to MQTT Broker')
        except Exception as e:
            self.connected = False
            logging.error(f'Failed to connect to MQTT Broker: {e}')

    def publish(self, message, qos=0):
        if self.connected:
            try:
                self.client.publish(self.topic_pub, message, qos=qos)
                logging.info('Published: %s', message)
            except Exception as e:
                logging.error(f'Failed to publish message: {e}')
        else:
            logging.warning('Cannot publish; not connected to MQTT Broker')

    def subscribe(self, topic, callback=None):
        try:
            self.client.subscribe(topic)
            logging.info(f'Subscribed to {topic}')
            if callback:
                self.client.set_callback(callback)
        except Exception as e:
            logging.error(f'Failed to subscribe to topic {topic}: {e}')

    def check_messages(self):
        try:
            self.client.check_msg()
        except Exception as e:
            logging.error(f'Error checking messages: {e}')
