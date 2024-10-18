import network
import utime
from machine import Pin
import secrets  # Import the secrets module

# Initialize onboard LED for status
pin = Pin("LED", Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("Waiting for WiFi connection...")
        utime.sleep(1)

    if wlan.isconnected():
        print("WiFi connection made:", wlan.isconnected())
        print("IP Address:", wlan.ifconfig()[0])
        pin.value(1)  # Turn on onboard LED
    else:
        print("Failed to connect to WiFi")
        pin.value(0)  # Turn off onboard LED

    return wlan