from utils.schemas import Weather


def format_weather(*, weather: Weather) -> str:
    delimiter = "-" * 40
    return (
        f"{delimiter}\n"
        f"Дата и время: {weather.now_datetime}\n"
        f"Место: {weather.geo_name}\n"
        f"Температура: {weather.temperature}°C\n"
        f"На улице: {weather.weather_title.value}\n"
        f"{delimiter}"
    )
