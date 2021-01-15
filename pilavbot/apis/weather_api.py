import json

import requests

import config
from constants import *


def returnReqError(url, result):
    """Handler for the request errors.

    Args:
        url (str): URL which the request was made.
        result (requests.models.Response): Response of the request.
    """

    print("Request error!")
    print(f"Url: {url}")
    print(f"Status Code: {result.status_code}")
    print(f"JSON result type: {type(result.json())}")
    print(result.json())


def get_current_weather_data(city):
    """Get weather data using given city / location name.

    Args:
        city (str): Name of the city / location.

    Returns:
        dict: A dict which consists of following keys:
            weather_description, icon_url, city_country, temp, temp_feels_like, temp_max, temp_min, humidity, wind_speed.
    """

    def kelvin_to_celcius(temperature):
        return str(round(temperature - 273.15))

    def ms_to_kmh(wind_speed):
        return str(round(wind_speed * 18 / 5))

    api_key = config.CONFIG.weather_api_key
    if api_key is None:
        return None

    url = WEATHER_API_URL + "?appid=" + api_key + "&q=" + city
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    result = result.json()
    result_sys = result["sys"]
    result_main = result["main"]
    result_weather = result["weather"]
    result_wind = result["wind"]

    return {
        "weather_description": result_weather[0]["description"].capitalize(),
        "icon_url": WEATHER_ICON_URL + result_weather[0]["icon"] + ".png",
        "city_country": result_sys["country"],
        "temp": kelvin_to_celcius(result_main["temp"]),
        "temp_feels_like": kelvin_to_celcius(result_main["feels_like"]),
        "temp_max": kelvin_to_celcius(result_main["temp_max"]),
        "temp_min": kelvin_to_celcius(result_main["temp_min"]),
        "humidity": result_main["humidity"],
        "wind_speed": ms_to_kmh(result_wind["speed"]),
    }


def valid_city(city):
    """Check if the city is valid or not.

    Args:
        city (str): Name of the city / location.

    Returns:
        bool: If the city exists or not.
    """

    weather_data = get_current_weather_data(city)
    if weather_data is None:
        return False
    return True
