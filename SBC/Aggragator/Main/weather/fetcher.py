import requests
import logging

class WeatherFetcher:
    def __init__(self, api_key, location):
        self.api_key = api_key
        self.location = location

    def fetch_weather_data(self):
        try:
            url = f'http://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={self.location}&days=1'
            response = requests.get(url)
            weather_data = response.json()

            current = weather_data['current']
            forecast = weather_data['forecast']['forecastday'][0]['day']
            astro = weather_data['forecast']['forecastday'][0]['astro']

            return {
                'temperature_f': current['temp_f'],
                'humidity': current['humidity'],
                'precipitation_inches': current['precip_in'],
                'heat_index_f': current['heatindex_f'],
                'will_it_rain': forecast['daily_will_it_rain'],
                'chance_of_rain': forecast['daily_chance_of_rain'],
                'sunrise': astro['sunrise'],
                'sunset': astro['sunset'],
                'wind_speed_mph': current['wind_mph']
            }
        except requests.RequestException as e:
            logging.error(f"Fetch weather data error: {e}")
            return None
