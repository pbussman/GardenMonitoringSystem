import network
import utime
from machine import Pin
import secrets
import logging

# Initialize onboard LED for status indication
pin = Pin("LED", Pin.OUT)

def connect_wifi():
    """Connect to WiFi using credentials from secrets.py."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    try:
        wlan.connect(secrets.SSID, secrets.PASSWORD)
        max_wait = 10
        while max_wait > 0:
            status = wlan.status()
            if status < 0 or status >= 3:
                break
            max_wait -= 1
            logging.info("Waiting for WiFi connection...")
            utime.sleep(1)

        if wlan.isconnected():
            logging.info("WiFi connection successful")
            logging.info("IP Address: %s", wlan.ifconfig()[0])
            pin.value(1)  # Turn on onboard LED to indicate success
        else:
            logging.error("WiFi connection failed. Status: %s", wlan.status())
            pin.value(0)  # Turn off onboard LED to indicate failure

    except Exception as e:
        logging.error("Exception during WiFi connection: %s", e)
        pin.value(0)  # Turn off onboard LED if an exception occurs

    return wlan

# Example usage:
if __name__ == "__main__":
    wlan = connect_wifi()
    if not wlan.isconnected():
        logging.error("Unable to establish WiFi connection.")
