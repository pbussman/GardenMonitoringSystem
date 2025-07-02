import time
import logging
from datetime import datetime
from database.manager import DatabaseManager
from weather.fetcher import WeatherFetcher
from mqtt.handler import MQTTHandler
from utils.time_utils import calculate_sleep_duration
import secrets

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    filename='pi5_log.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize components
db_manager = DatabaseManager()
weather_fetcher = WeatherFetcher(
    api_key=secrets.WEATHER_API_KEY,
    location=secrets.WEATHER_LOCATION
)
mqtt_handler = None
mqtt_running = False

# Weather fetch with retry
def get_weather_with_retry(max_attempts=3, delay=10):
    for attempt in range(1, max_attempts + 1):
        try:
            weather = weather_fetcher.fetch_weather_data()
            if weather:
                return weather
        except Exception as e:
            logging.warning(f"Weather fetch attempt {attempt} failed: {e}")
            time.sleep(delay)
    logging.error("Exceeded max weather fetch attempts")
    return None

while True:
    try:
        weather_data = get_weather_with_retry()
        if weather_data:
            sunrise = weather_data['sunrise']
            sunset = weather_data['sunset']
            sleep_duration = calculate_sleep_duration(sunrise, sunset)

            if sleep_duration:
                if mqtt_running and mqtt_handler:
                    logging.info("Stopping MQTT handler before sleep.")
                    mqtt_handler.stop()
                    mqtt_running = False

                logging.info(f"Sleeping for {sleep_duration / 3600:.2f} hours")
                time.sleep(sleep_duration)
            else:
                if not mqtt_running:
                    logging.info("Starting MQTT handler after sleep.")
                    mqtt_handler = MQTTHandler(
                        client_id='DataBase',
                        server=secrets.MQTT_SERVER,
                        username=secrets.MQTT_USERNAME,
                        password=secrets.MQTT_PASSWORD,
                        db_manager=db_manager,
                        weather_fetcher=weather_fetcher
                    )
                    mqtt_handler.start()
                    mqtt_running = True
        else:
            logging.warning("Weather data unavailable. Keeping MQTT running by default.")
            if not mqtt_running:
                mqtt_handler = MQTTHandler(
                    client_id='DataBase',
                    server=secrets.MQTT_SERVER,
                    username=secrets.MQTT_USERNAME,
                    password=secrets.MQTT_PASSWORD,
                    db_manager=db_manager,
                    weather_fetcher=weather_fetcher
                )
                mqtt_handler.start()
                mqtt_running = True

        # Optional: Log heartbeat every top of the hour
        if datetime.now().minute == 0:
            logging.info("System heartbeat: active and monitoring.")

    except Exception as e:
        logging.error(f"Critical error in main loop: {e}")
        if mqtt_running and mqtt_handler:
            mqtt_handler.stop()
            mqtt_running = False
        time.sleep(60)  # brief cooldown before retry
