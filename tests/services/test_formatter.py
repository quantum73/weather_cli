from services.formatter import format_weather
from utils.enums import WeatherTitle
from utils.schemas import Weather


def test_pretty_print_weather():
    weather = Weather(
        temperature=20,
        weather_title=WeatherTitle.clear,
        geo_name="Moscow"
    )
    target_output = (
        f"Дата и время: {weather.now_datetime}\n"
        f"Место: {weather.geo_name}\n"
        f"Температура: {weather.temperature}°C\n"
        f"На улице: {weather.weather_title.value}"
    )
    weather_as_str = format_weather(weather=weather)

    assert weather_as_str == target_output
