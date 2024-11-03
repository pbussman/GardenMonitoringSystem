import umqtt.simple as mqtt
import secrets

class MQTTClient:
    def __init__(self, client_id, mqtt_server, topic_pub):
        self.client_id = client_id
        self.mqtt_server = mqtt_server
        self.topic_pub = topic_pub
        self.client = mqtt.MQTTClient(self.client_id, self.mqtt_server)

    def connect(self):
        self.client.connect(user=secrets.MQTT_USERNAME, password=secrets.MQTT_PASSWORD)
        print('Connected to MQTT Broker')

    def publish(self, message):
        self.client.publish(self.topic_pub, message)
        print('Published:', message)
