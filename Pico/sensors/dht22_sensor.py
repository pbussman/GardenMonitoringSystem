from machine import Pin
import dht

class DHT22Sensor:
    def __init__(self, pin_number, power_pin=None):
        self.sensor = dht.DHT22(Pin(pin_number))
        self.power_pin = Pin(power_pin, Pin.OUT) if power_pin else None

    def read(self):
        try:
            if self.power_pin:
                self.power_pin.value(1)  # Turn on the sensor
                utime.sleep(2)  # Wait for the sensor to stabilize
            self.sensor.measure()
            temp_c = self.sensor.temperature()
            hum = self.sensor.humidity()
            temp_f = temp_c * 9 / 5 + 32
            if self.power_pin:
                self.power_pin.value(0)  # Turn off the sensor
            return {'temperature_c': temp_c, 'temperature_f': temp_f, 'humidity': hum}
        except OSError as e:
            print('Failed to read DHT22 sensor.')
            return None
