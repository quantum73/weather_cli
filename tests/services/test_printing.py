from services.printing import pretty_print_weather
from utils.enums import WeatherTitle
from utils.schemas import Weather


def test_pretty_print_weather(capfd):
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
    target_output = target_output.strip()

    pretty_print_weather(weather=weather)
    out, err = capfd.readouterr()
    out, err = out.strip(), err.strip()

    assert len(err) == 0
    assert len(out) > 0
    assert out == target_output
