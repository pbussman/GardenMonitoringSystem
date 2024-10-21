import utime
from sensors.dht22_sensor import DHT22Sensor
from sensors.rain_sensor import RainSensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.soil_temp_sensor import SoilTempSensor
from communications import wifi
from communications.mqtt_client import MQTTClient

# Initialize sensors
dht22 = DHT22Sensor(pin_number=22)
rain_sensor = RainSensor(power_pin=27, data_pin=21)
soil_moisture_sensor = SoilMoistureSensor(power_pin=18, data_pin=26)
soil_temp_sensor = SoilTempSensor(power_pin=14, data_pin=15)

# Connect to WiFi
wlan = wifi.connect_wifi()

# Initialize MQTT client
mqtt_client = MQTTClient(client_id='pico_sensor', mqtt_server='192.168.4.1', topic_pub='garden/sensors')
mqtt_client.connect()

# Function to read and publish sensor data
def read_and_publish():
    dht22_data = dht22.read()
    rain_data = rain_sensor.read()
    soil_moisture_data = soil_moisture_sensor.read()
    soil_temp_data = soil_temp_sensor.read()

    msg = {
        'temperature_f': dht22_data['temperature_f'],
        'humidity': dht22_data['humidity'],
        'rain_status': rain_data,
        'soil_moisture_percentage': soil_moisture_data['moisture_percentage'],
        'soil_temperature_f': soil_temp_data['temperature_f']
    }

    mqtt_client.publish(str(msg))

# Main function
while True:
    if wlan.isconnected():
        read_and_publish()
        utime.sleep(600)  # Pause for 10 minutes
    else:
        print("Reconnecting to WiFi...")
        wlan = wifi.connect_wifi()
