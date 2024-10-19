# GardenControl
Project Description: Garden Monitoring and Control System
The goal of this project is to build a comprehensive garden monitoring and control system using a Raspberry Pi Single Board Computer (SBC) and microcontrollers. The SBC will serve as the primary controller, making intelligent decisions such as selecting the appropriate water source and determining the optimal times to water the garden beds.

Microcontrollers will be deployed throughout the garden to host various sensors, which will collect data on:

Air Temperature and Humidity: Using sensors like the DHT22 to monitor the atmospheric conditions.
Soil Temperature and Moisture: Utilizing sensors such as the DS18B20 for soil temperature and capacitive soil moisture sensors for moisture levels.
Ambient Light: Measuring light intensity to assess the garden’s exposure to sunlight.
Rain Detection: Using rain sensors to detect precipitation and adjust watering schedules accordingly.
The data collected by the microcontrollers will be communicated back to the Raspberry Pi SBC via MQTT, enabling real-time monitoring and control. This system aims to optimize garden maintenance, ensuring plants receive the right amount of water and care based on current environmental conditions.
