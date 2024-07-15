import requests
from datetime import datetime
from config.config import *

API_KEY = WEATHER_API_KEY  # Replace with your actual API key
CITY = CITY_NAME

def get_weather():
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric"  # For Celsius
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        # Current temperature and weather description
        temp = data['main']['temp']
        description = data['weather'][0]['description']

        # Sunrise and sunset times
        sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.fromtimestamp(data['sys']['sunset'])

        # Additional information
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        print(f"Current weather in {CITY}:")
        print(f"Temperature: {temp}°C")
        print(f"Conditions: {description}")
        print(f"Sunrise: {sunrise.strftime('%I:%M %p')}")
        print(f"Sunset: {sunset.strftime('%I:%M %p')}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        print("Failed to retrieve weather data")

if __name__ == "__main__":
    get_weather()