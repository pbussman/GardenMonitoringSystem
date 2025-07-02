import time
import logging
from datetime import datetime
from database.manager import DatabaseManager
from weather.fetcher import WeatherFetcher
from mqtt.handler import MQTTHandler
from ml.decision_engine import get_irrigation_advice
from utils.time_utils import calculate_sleep_duration
import secrets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename='pi5_log.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

db_manager = DatabaseManager()
weather_fetcher = WeatherFetcher(secrets.WEATHER_API_KEY, secrets.WEATHER_LOCATION)
mqtt_handler = None
mqtt_running = False

def fetch_weather_with_retry(retries=3):
    for attempt in range(retries):
        try:
            return weather_fetcher.fetch_weather_data()
        except Exception as e:
            logging.warning(f"Weather fetch failed (attempt {attempt+1}): {e}")
            time.sleep(10)
    return None

while True:
    try:
        weather = fetch_weather_with_retry()
        if weather:
            sunrise = weather['sunrise']
            sunset = weather['sunset']
            sleep_duration = calculate_sleep_duration(sunrise, sunset)

            if sleep_duration:
                if mqtt_running:
                    mqtt_handler.stop()
                    mqtt_running = False
                    logging.info("Stopped MQTT handler for night sleep.")
                logging.info(f"Sleeping for {sleep_duration/3600:.2f} hours.")
                time.sleep(sleep_duration)
                continue

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

        # Example: collect latest data and publish advice
        for zone in db_manager.get_active_zones():
            readings = db_manager.get_recent_sensor_readings(zone)
            advice = get_irrigation_advice(zone, readings)
            mqtt_handler.publish_advice(zone, advice)

        mqtt_handler.process_command_queue()

        # Heartbeat
        if datetime.now().minute == 0:
            logging.info("System heartbeat.")

        time.sleep(60)

    except Exception as e:
        logging.error(f"Main loop error: {e}")
        if mqtt_running:
            mqtt_handler.stop()
            mqtt_running = False
        time.sleep(60)
