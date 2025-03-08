import os
from sdcard import SDCard
from machine import SPI, Pin

def init_sd():
    # Configure SD card SPI interface
    spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(8))
    cs = Pin(5, Pin.OUT)
    sd = SDCard(spi, cs)
    os.mount(sd, "/sd")  # Mount SD card at /sd
    print("SD card initialized and mounted!")
    return "/sd"

def log_event(file_path, message):
    with open(file_path, "a") as log_file:
        timestamp = time.localtime()
        log_file.write(f"{timestamp}: {message}\n")
    print(f"Logged: {message}")
