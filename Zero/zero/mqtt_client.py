# Zero/mqtt_client.py

import paho.mqtt.client as mqtt
import json
from Zero.logger import setup_logger

logger = setup_logger()

class MQTTClient:
    def __init__(self, broker, port, client_id, tls_conf=None):
        self.client = mqtt.Client(client_id=client_id)
        if tls_conf:
            self.client.tls_set(
                ca_certs=tls_conf['ca_certs'],
                certfile=tls_conf['certfile'],
                keyfile=tls_conf['keyfile']
            )
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self._handlers = {}

        self.client.connect(broker, port)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        logger.info("Connected to MQTT broker with result code %s", rc)
        for topic in self._handlers:
            client.subscribe(topic)
            logger.debug("Subscribed to topic: %s", topic)

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        logger.debug("Received message on %s: %s", topic, payload)
        if topic in self._handlers:
            try:
                self._handlers[topic](payload)
            except Exception as e:
                logger.error("Error handling message on %s: %s", topic, str(e))

    def register(self, topic, callback):
        self._handlers[topic] = callback
        self.client.subscribe(topic)
        logger.debug("Registered handler for topic: %s", topic)

    def publish(self, topic, payload):
        self.client.publish(topic, json.dumps(payload))
        logger.debug("Published to %s: %s", topic, payload)
