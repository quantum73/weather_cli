import requests
from requests import Response
from requests.exceptions import RequestException

from config import WEATHER_API_URL, HEADERS, GETTING_KEY_ERROR_MESSAGE
from utils.enums import WeatherTitle
from utils.exceptions import ApiServiceError
from utils.schemas import Coordinates, Weather, Celsius


def _get_temperature(*, data: dict) -> Celsius:
    try:
        return round(data["main"]["temp"])
    except KeyError:
        raise ApiServiceError(GETTING_KEY_ERROR_MESSAGE)


def _get_weather_title(*, data: dict) -> WeatherTitle:
    try:
        weather_title = data["weather"][0]["main"].lower()
    except (KeyError, IndexError):
        raise ApiServiceError(GETTING_KEY_ERROR_MESSAGE)

    return WeatherTitle.get(key=weather_title)


def _get_geo_name(*, data: dict) -> str:
    try:
        return data["name"].title()
    except KeyError:
        raise ApiServiceError(GETTING_KEY_ERROR_MESSAGE)


def _formatting_response_from_api(*, weather_data: dict) -> Weather:
    temperature = _get_temperature(data=weather_data)
    weather_title = _get_weather_title(data=weather_data)
    geo_name = _get_geo_name(data=weather_data)
    weather_obj = Weather(
        temperature=temperature,
        weather_title=weather_title,
        geo_name=geo_name,
    )
    return weather_obj


def _get_json_data_from_weather_api(*, coordinates: Coordinates) -> dict:
    url = WEATHER_API_URL.format(latitude=coordinates.latitude, longitude=coordinates.longitude)
    try:
        response: Response = requests.get(url, headers=HEADERS)
    except RequestException:
        raise ApiServiceError("Something wrong with weather API :(")

    try:
        json_data = response.json()
    except (requests.JSONDecodeError, UnicodeDecodeError):
        raise ApiServiceError("Bad JSON data")

    return json_data


def get_weather_by_coordinates(*, coordinates: Coordinates) -> Weather:
    weather_json_data = _get_json_data_from_weather_api(coordinates=coordinates)
    weather = _formatting_response_from_api(weather_data=weather_json_data)
    return weather
