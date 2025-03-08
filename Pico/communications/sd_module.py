import os
import sys
from sdcard import SDCard
from machine import SPI, Pin

# SD Card Initialization
def init_sd():
    """Initialize and mount the SD card."""
    spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(8))
    cs = Pin(5, Pin.OUT)
    sd = SDCard(spi, cs)
    os.mount(sd, "/sd")
    print("SD card initialized and mounted!")

    # Add SD card path to system path for dynamic imports
    sys.path.append("/sd")
    return "/sd"
