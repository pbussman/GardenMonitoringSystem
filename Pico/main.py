import utime
from sensors.dht22_sensor import DHT22Sensor
from sensors.rain_sensor import RainSensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.soil_temp import SoilTempSensor
from communications import wifi
from communications.mqtt_client import MQTTClientimport wifi

# Initialize sensors
dht22 = DHT22Sensor(pin_number=22)
rain_sensor = RainSensor(power_pin=27, data_pin=21)
soil_moisture_sensor = SoilMoistureSensor(power_pin=18, data_pin=26)
soil_temp_sensor = SoilTempSensor(power_pin=14, data_pin=15)

# Connect to WiFi
wlan = wifi.connect_wifi()

# Initialize MQTT client
mqtt_client = MQTTClient(
    client_id='GardenSensor',
    mqtt_server=secrets.MQTT_SERVER,
    topic_pub='garden/sensors'
)
mqtt_client.connect()

# Function to read and publish sensor data
def read_sensors():
    dht22_data = dht22.read()
    rain_data = rain_sensor.read()
    soil_moisture_data = soil_moisture_sensor.read()
    soil_temp_data = soil_temp_sensor.read()

    if dht22_data:
        message = f"DHT22 - Temperature: {dht22_data['temperature_f']} F, Humidity: {dht22_data['humidity']} %"
        print(message)
        mqtt_client.publish(message)
    if rain_data:
        message = f"Rain Sensor: {rain_data}"
        print(message)
        mqtt_client.publish(message)
    if soil_moisture_data:
        message = f"Soil Moisture: {soil_moisture_data['moisture_percentage']} %"
        print(message)
        mqtt_client.publish(message)
    if soil_temp_data:
        message = f"Soil Temperature: {soil_temp_data['temperature_f']} F"
        print(message)
        mqtt_client.publish(message)

# Main function
while True:
    if wlan.isconnected():
        read_sensors()
        utime.sleep(600)  # Pause for 10 minutes (600 seconds)
    else:
        print("Reconnecting to WiFi...")
        wlan = wifi.connect_wifi()
