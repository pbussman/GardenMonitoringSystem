import utime
from sensors.dht22_sensor import DHT22Sensor
from sensors.rain_sensor import RainSensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.soil_temp import SoilTempSensor
from communications import wifi
# from communications.mqtt_client import MQTTClientimport wifi

# Initialize sensors
dht22 = DHT22Sensor(pin_number=22)
rain_sensor = RainSensor(power_pin=27, data_pin=21)
soil_moisture_sensor = SoilMoistureSensor(power_pin=18, data_pin=26)
soil_temp_sensor = SoilTempSensor(power_pin=14, data_pin=15)

# Connect to WiFi
wlan = wifi.connect_wifi()

# Initialize MQTT client
# mqtt_client = MQTTClient(client_id='pico_sensor', mqtt_server='192.168.4.1', topic_pub='garden/sensors')
# mqtt_client.connect()

# Function to read and print sensor data
def read_sensors():
    dht22_data = dht22.read()
    rain_data = rain_sensor.read()
    soil_moisture_data = soil_moisture_sensor.read()
    soil_temp_data = soil_temp_sensor.read()

    if dht22_data:
        print(f"DHT22 - Temperature: {dht22_data['temperature_f']} F, Humidity: {dht22_data['humidity']} %")
    if rain_data:
        print(f"Rain Sensor: {rain_data}")
    if soil_moisture_data:
        print(f"Soil Moisture: {soil_moisture_data['moisture_percentage']} %")
    if soil_temp_data:
        print(f"Soil Temperature: {soil_temp_data['temperature_f']} F")

# Main function
while True:
    if wlan.isconnected():
        read_sensors()
        utime.sleep(600)  # Pause for 10 minutes (600 seconds)
    else:
        print("Reconnecting to WiFi...")
        wlan = wifi.connect_wifi()
