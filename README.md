
# GardenControl
Project Description: Garden Monitoring and Control System<br>
The goal of this project is to build a comprehensive garden monitoring and control system using a Raspberry Pi Single Board Computer (SBC) and microcontrollers. The SBC will serve as the primary controller, making intelligent decisions such as selecting the appropriate water source and determining the optimal times to water the garden beds.

Microcontrollers will be deployed throughout the garden to host various sensors, which will collect data on:

Air Temperature and Humidity: Using sensors like the DHT22 to monitor the atmospheric conditions.<br>

Soil Temperature and Moisture: Utilizing sensors such as the DS18B20 for soil temperature and capacitive soil moisture sensors for moisture levels.<br>

Ambient Light: Measuring light intensity to assess the garden’s exposure to sunlight.<br>

Rain Detection: Using rain sensors to detect precipitation and adjust watering schedules accordingly.<br>

The data collected by the microcontrollers will be communicated back to the Raspberry Pi SBC via MQTT, enabling real-time monitoring and control. This system aims to optimize garden maintenance, ensuring plants receive the right amount of water and care based on current environmental conditions.

## Repository Structure
- **SBC/**: Contains code for the Raspberry Pi SBC.
- **Pico/**: Contains code for the Raspberry Pi Pico microcontrollers.
- **docs/**: Documentation, wiring diagrams, and setup instructions.

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
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
