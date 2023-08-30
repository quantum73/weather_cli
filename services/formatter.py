from utils.schemas import Weather


def format_weather(*, weather: Weather) -> str:
    return (
        f"Дата и время: {weather.now_datetime}\n"
        f"Место: {weather.geo_name}\n"
        f"Температура: {weather.temperature}°C\n"
        f"На улице: {weather.weather_title.value}"
    )
