import time
import logging
from datetime import datetime
from database.manager import DatabaseManager
from weather.fetcher import WeatherFetcher
from mqtt.handler import MQTTHandler
from utils.time_utils import calculate_sleep_duration
import secrets

# Set up logging
logging.basicConfig(level=logging.INFO, filename='pi5_log.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize components
db_manager = DatabaseManager()
weather_fetcher = WeatherFetcher(api_key=secrets.WEATHER_API_KEY, location=secrets.WEATHER_LOCATION)
mqtt_handler = MQTTHandler(
    client_id='DataBase',
    server=secrets.MQTT_SERVER,
    username=secrets.MQTT_USERNAME,
    password=secrets.MQTT_PASSWORD,
    db_manager=db_manager,
    weather_fetcher=weather_fetcher
)

# Run the MQTT client with sleep logic
while True:
    try:
        weather_data = weather_fetcher.fetch_weather_data()
        if weather_data:
            sunrise = weather_data['sunrise']
            sunset = weather_data['sunset']
            sleep_duration = calculate_sleep_duration(sunrise, sunset)
            if sleep_duration:
                logging.info(f"Going to sleep for {sleep_duration / 3600:.2f} hours")
                mqtt_handler.stop()
                time.sleep(sleep_duration)
            else:
                mqtt_handler.start()
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
