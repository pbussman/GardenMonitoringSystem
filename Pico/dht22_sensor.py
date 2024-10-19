from machine import Pin
import dht

class DHT22Sensor:
    def __init__(self, pin_number):
        self.sensor = dht.DHT22(Pin(pin_number))

    def read(self):
        try:
            self.sensor.measure()
            temp_c = self.sensor.temperature()
            hum = self.sensor.humidity()
            temp_f = temp_c * 9 / 5 + 32
            return {'temperature_c': temp_c, 'temperature_f': temp_f, 'humidity': hum}
        except OSError as e:
            print('Failed to read DHT22 sensor.')
            return None
