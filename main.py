from services.coordinates import get_coordinates
from services.printing import pretty_print_weather
from services.weather_api import get_weather_by_coordinates
from utils.schemas import Coordinates, Weather


def main() -> None:
    coordinates: Coordinates = get_coordinates()
    weather: Weather = get_weather_by_coordinates(coordinates=coordinates)
    pretty_print_weather(weather=weather)


if __name__ == '__main__':
    main()
