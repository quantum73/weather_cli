from services.coordinates import get_coordinates
from services.formatter import format_weather
from services.weather_api import get_weather_by_coordinates
from utils.exceptions import CantGetCoordinates, ApiServiceError


def main() -> None:
    try:
        coordinates = get_coordinates()
    except CantGetCoordinates:
        print("Не удалось получить координаты")
        exit(1)

    try:
        weather = get_weather_by_coordinates(coordinates=coordinates)
    except ApiServiceError:
        print(f"Не удалось получить погоду по координатам {coordinates}")
        exit(1)

    print(format_weather(weather=weather))


if __name__ == '__main__':
    main()
