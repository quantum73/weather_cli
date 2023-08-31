import argparse
from argparse import Namespace as ArgparseNamespace

from services.coordinates import get_coordinates, CoordinatesSourceProtocol, PlugSource, ConsoleSource
from services.formatter import format_weather
from services.weather_api import get_weather_by_coordinates
from utils.enums import CoordinatesInputType
from utils.exceptions import CantGetCoordinates, ApiServiceError, ArgumentCLIError


def get_coordinates_source_from_input(*, cli_args: ArgparseNamespace) -> CoordinatesSourceProtocol:
    try:
        coordinates_input = cli_args.coordinates_input
    except AttributeError:
        raise ArgumentCLIError

    sources = {
        CoordinatesInputType.console.value: ConsoleSource,
        CoordinatesInputType.plug.value: PlugSource,
    }
    source = sources.get(coordinates_input)
    if source is None:
        raise ArgumentCLIError

    return source


def cli_parser() -> ArgparseNamespace:
    parser = argparse.ArgumentParser(description='Get weather by coordinates.')
    parser.add_argument(
        '--coordinates_input',
        type=str,
        help=f'Input coordinates source. Possible choices: {CoordinatesInputType.to_str()}.',
    )
    return parser.parse_args()


def main() -> None:
    try:
        cli_args = cli_parser()
        coordinates_source = get_coordinates_source_from_input(cli_args=cli_args)
    except ArgumentCLIError:
        print("Некорректный ввод аргументов или запуск без аргументов!")
        exit(1)
    except Exception:
        print("Непредвиденная ошибка :(")
        exit(1)

    try:
        coordinates = get_coordinates(coordinates_source=coordinates_source)
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
