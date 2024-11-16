# Garden Monitoring and Control System

## Overview
The **Garden Monitoring and Control System** leverages the power of a Raspberry Pi 5 and multiple Raspberry Pi Pico microcontrollers to optimize garden maintenance. This system automates and enhances the monitoring and control of various environmental parameters, ensuring optimal conditions for plant growth. Additionally, it uses machine learning to predict and automate watering schedules based on historical data.

## Objectives
- **Automate Garden Maintenance**: Implement intelligent control decisions to manage watering schedules and select appropriate water sources.
- **Real-Time Monitoring**: Collect and analyze data from sensors to monitor air temperature, humidity, soil temperature, soil moisture, ambient light, and rain detection.
- **Efficient Communication**: Utilize the MQTT protocol for seamless communication between the Raspberry Pi Pico microcontrollers and the Raspberry Pi 5.
- **Predictive Analytics**: Use machine learning to predict watering needs based on historical sensor and weather data.

## Components
1. **Raspberry Pi 5**:
   - Acts as the primary controller.
   - Fetches comprehensive weather data from the WeatherAPI, including current conditions, forecast, and astronomical data.
   - Publishes sunrise and sunset times to the Raspberry Pi Pico microcontrollers via MQTT.
   - Manages the MQTT broker for communication.
   - Logs data and system events.
   - Trains and deploys machine learning models for predictive analytics.

2. **Raspberry Pi Pico Microcontrollers**:
   - Host various sensors throughout the garden.
   - Collect and transmit sensor data to the Raspberry Pi 5.
   - Receive sunrise and sunset times from the Raspberry Pi 5 to manage sleep cycles.

3. **Sensors**:
   - **DHT22**: Measures air temperature and humidity.
   - **DS18B20**: Measures soil temperature.
   - **Capacitive Soil Moisture Sensor**: Measures soil moisture levels.
   - **Rain Sensor**: Detects rain.
   - **Ambient Light Sensor (VEML7700)**: Measures light intensity.

## Features
- **Intelligent Watering**: Automatically determines when and how much to water the garden based on real-time data and machine learning predictions.
- **Data Logging**: Logs sensor data for historical analysis and trend monitoring.
- **Alerts and Notifications**: Sends alerts for critical conditions (e.g., low soil moisture, high temperature).
- **Modular Design**: Easily add or remove sensors and microcontrollers as needed.
- **Power Management**: Raspberry Pi Pico microcontrollers sleep during the night and wake up 5 minutes before sunrise, based on times received from the Raspberry Pi 5.
- **Predictive Analytics**: Uses a Random Forest classifier to predict watering needs based on historical sensor and weather data.

## Setup Instructions
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/Garden-Monitoring-System.git
    cd Garden-Monitoring-System
    ```

2. **Configure the Raspberry Pi Pico**:
   - Copy `Pico/secrets.py.example` to `Pico/secrets.py` and fill in your WiFi credentials.
   - Upload the code in the `Pico/` directory to your Raspberry Pi Pico.

3. **Set Up the Raspberry Pi 5**:
   - Follow the instructions in `Pi5/mqtt_broker_setup.md` to set up the MQTT broker.
   - Install the required Python packages:
       ```bash
       pip install -r Pi5/requirements.txt
       ```

4. **Run the Main Controller**:
    ```bash
    python Pi5/main.py
    ```

5. **Train the Machine Learning Model**:
   - Run the script to train the Random Forest classifier:
       ```bash
       python Pi5/train_model.py
       ```
   - This will save the trained model as `garden_watering_model.pkl`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request to contribute to this project.

## License
This project is licensed under the MIT License.
