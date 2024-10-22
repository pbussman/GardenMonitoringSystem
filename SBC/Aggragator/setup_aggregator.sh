#!/bin/bash

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install required packages for WiFi hotspot
sudo apt install -y hostapd dnsmasq netfilter-persistent iptables-persistent

# Configure DHCP and DNS
echo "interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant" | sudo tee -a /etc/dhcpcd.conf

sudo service dhcpcd restart

sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
echo "interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h" | sudo tee /etc/dnsmasq.conf

# Configure Hostapd
echo "interface=wlan0
driver=nl80211
ssid=GardenNetwork
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=YourPassword
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP" | sudo tee /etc/hostapd/hostapd.conf

sudo sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

# Enable and start services
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo systemctl restart dnsmasq

# Install and configure Mosquitto MQTT broker
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

echo "listener 1883
allow_anonymous true" | sudo tee -a /etc/mosquitto/mosquitto.conf

sudo systemctl restart mosquitto

# Install Python and required libraries
sudo apt install -y python3-pip
pip3 install paho-mqtt psycopg2-binary

# Create data aggregator script
echo "import paho.mqtt.client as mqtt
import psycopg2
import json

# MQTT settings
broker = 'localhost'
port = 1883
topic = 'garden/sensors'

# Database settings
db_host = '192.168.1.100'  # IP address of the central controller
db_name = 'garden_db'
db_user = 'your_db_user'
db_password = 'your_db_password'

# Connect to the database
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)
cur = conn.cursor()

# MQTT callback function
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    temp_f = data['temperature_f']
    humidity = data['humidity']
    rain_status = data['rain_status']
    soil_moisture = data['soil_moisture_percentage']
    soil_temp_f = data['soil_temperature_f']
    
    # Insert data into the database
    cur.execute(
        'INSERT INTO sensor_data (temperature_f, humidity, rain_status, soil_moisture, soil_temperature_f) VALUES (%s, %s, %s, %s, %s)',
        (temp_f, humidity, rain_status, soil_moisture, soil_temp_f)
    )
    conn.commit()

# MQTT client setup
client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port, 60)
client.subscribe(topic)
client.loop_forever()" > data_aggregator.py

echo "Setup complete. You can now run the data aggregator script with 'python3 data_aggregator.py'."
