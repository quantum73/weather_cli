from services.coordinates import get_coordinates
from services.printing import pretty_print_weather
from services.weather_api import get_weather_by_coordinates


def main() -> None:
    coordinates = get_coordinates()
    weather = get_weather_by_coordinates(coordinates=coordinates)
    pretty_print_weather(weather=weather)


if __name__ == '__main__':
    main()
