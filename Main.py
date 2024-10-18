import utime
from machine import Pin, ADC
import dht
import onewire, ds18x20
import wifi  # Import the wifi module

# Initialize sensors
dht_sensor = dht.DHT22(Pin(22))
rain_power_pin = Pin(27, Pin.OUT)  # Use GPIO 27 to control power to the rain sensor
rain_sensor = Pin(21, Pin.IN)      # Use GPIO 21 to read the rain sensor
soil_power_pin = Pin(18, Pin.OUT)  # Use GPIO 18 to control power to the soil moisture sensor
soil_moisture_sensor = ADC(Pin(26))  # Use GPIO 26 for the soil moisture sensor
ds_power_pin = Pin(14, Pin.OUT)  # Use GPIO 14 to control power to the DS18B20 sensor
ds_pin = Pin(15)  # Use GPIO 15 for the DS18B20 data line
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

# Connect to WiFi
wlan = wifi.connect_wifi()

# Function to read and print sensor data
def read_sensors():
    try:
        # Read DHT22 data
        dht_sensor.measure()
        temp_c = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        temp_f = temp_c * 9 / 5 + 32

        # Read Rain Sensor data
        rain_power_pin.value(1)  # Turn the rain sensor's power ON
        utime.sleep_ms(10)  # Wait 10 milliseconds
        rain_state = rain_sensor.value()
        rain_power_pin.value(0)  # Turn the rain sensor's power OFF
        rain_status = "It's raining!" if rain_state == 0 else "No rain."

        # Read Soil Moisture Sensor data
        soil_power_pin.value(1)  # Turn the soil moisture sensor's power ON
        utime.sleep_ms(10)  # Wait 10 milliseconds
        soil_moisture_value = soil_moisture_sensor.read_u16()
        soil_power_pin.value(0)  # Turn the soil moisture sensor's power OFF
        soil_moisture_percentage = (soil_moisture_value / 65535.0) * 100

        # Read DS18B20 data
        ds_power_pin.value(1)  # Turn the DS18B20 sensor's power ON
        utime.sleep_ms(10)  # Wait 10 milliseconds
        ds_sensor.convert_temp()
        utime.sleep_ms(750)
        ds_temp_c = ds_sensor.read_temp(ds_sensor.scan()[0])
        ds_power_pin.value(0)  # Turn the DS18B20 sensor's power OFF
        ds_temp_f = ds_temp_c * 9 / 5 + 32

        # Print sensor data
        print('Air - Temperature: %3.1f F, Humidity: %3.1f %%' % (temp_f, hum))
        print('Rain Sensor: %s' % rain_status)
        print('Soil Moisture: %3.1f %%' % soil_moisture_percentage)
        print('Soil Temperature: %3.1f F' % ds_temp_f)
    except OSError as e:
        print('Failed to read sensor.')

# Main function
while True:
    if wlan.isconnected():
        read_sensors()
        utime.sleep(10)  # Pause for 10 minutes (600 seconds)
    else:
        print("Reconnecting to WiFi...")
        wlan = wifi.connect_wifi()