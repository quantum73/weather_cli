from utils.schemas import Weather


def pretty_print_weather(*, weather: Weather) -> None:
    print(
        f"Дата и время: {weather.now_datetime}\n"
        f"Место: {weather.geo_name}\n"
        f"Температура: {weather.temperature}°C\n"
        f"На улице: {weather.weather_title}"
    )
