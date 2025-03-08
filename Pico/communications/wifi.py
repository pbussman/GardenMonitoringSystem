import network
import logging
import utime
from machine import Pin

# Connect to WiFi
def connect_wifi(secrets):
    """Connect to WiFi using credentials from secrets."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        logging.info("Waiting for WiFi connection...")
        utime.sleep(1)

    if wlan.isconnected():
        logging.info("WiFi connected: %s", wlan.ifconfig()[0])
        pin = Pin("LED", Pin.OUT)
        pin.value(1)  # Turn on onboard LED to indicate success
    else:
        logging.error("Failed to connect to WiFi")
    return wlan

# Reconnect to WiFi with retries
def reconnect_wifi(secrets):
    """Retry WiFi connection with exponential backoff."""
    for attempt in range(5):
        wlan = connect_wifi(secrets)
        if wlan.isconnected():
            logging.info(f"WiFi reconnected successfully on attempt {attempt + 1}")
            return wlan
        logging.warning(f"Reconnection attempt {attempt + 1} failed. Retrying...")
        utime.sleep(2 ** attempt)
    logging.error("Unable to reconnect to WiFi after multiple attempts.")
    return None
