# Garden Monitoring and Control System

## Overview
The Garden Monitoring and Control System is designed to optimize garden maintenance by leveraging the power of a Raspberry Pi Single Board Computer (SBC) and multiple Raspberry Pi Pico microcontrollers. This system aims to automate and enhance the monitoring and control of various environmental parameters in a garden, ensuring optimal conditions for plant growth.

## Objectives
- **Automate Garden Maintenance**: Use intelligent control decisions to manage watering schedules and select appropriate water sources.
- **Real-Time Monitoring**: Collect and analyze data from various sensors to monitor air temperature, humidity, soil temperature, soil moisture, ambient light, and rain detection.
- **Efficient Communication**: Utilize MQTT protocol for seamless communication between the Raspberry Pi Pico microcontrollers and the Raspberry Pi SBC.

## Components
1. **Raspberry Pi SBC**:
   - Acts as the primary controller.
   - Makes intelligent decisions based on sensor data.
   - Manages MQTT broker for communication.

2. **Raspberry Pi Pico Microcontrollers**:
   - Host various sensors throughout the garden.
   - Collect and transmit sensor data to the Raspberry Pi SBC.

3. **Sensors**:
   - **DHT22**: Measures air temperature and humidity.
   - **DS18B20**: Measures soil temperature.
   - **Capacitive Soil Moisture Sensor**: Measures soil moisture levels.
   - **Rain Sensor**: Detects rain.
   - **Ambient Light Sensor**: Measures light intensity (optional).

## Features
- **Intelligent Watering**: Automatically determines when and how much to water the garden based on real-time data.
- **Data Logging**: Logs sensor data for historical analysis and trend monitoring.
- **Alerts and Notifications**: Sends alerts for critical conditions (e.g., low soil moisture, high temperature).
- **Modular Design**: Easily add or remove sensors and microcontrollers as needed.

## Setup Instructions
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/Garden-Monitoring-System.git
    cd Garden-Monitoring-System
    ```

2. **Configure the Raspberry Pi Pico**:
   - Copy `Pico/secrets.py.example` to `Pico/secrets.py` and fill in your WiFi credentials.
   - Upload the code in the `Pico/` directory to your Raspberry Pi Pico.

3. **Set Up the Raspberry Pi SBC**:
   - Follow the instructions in `SBC/mqtt_broker_setup.md` to set up the MQTT broker.
   - Install the required Python packages:
       ```bash
       pip install -r SBC/requirements.txt
       ```

4. **Run the Main Controller**:
    ```bash
    python SBC/main_controller.py
    ```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request to contribute to this project.

## License
This project is licensed under the MIT License.
