from typing import Protocol

from utils.exceptions import CantGetCoordinates
from utils.schemas import Coordinates


def _parse_coordinate(*, coordinate_value: str | float | int) -> float:
    try:
        return float(coordinate_value)
    except ValueError:
        raise CantGetCoordinates


class CoordinatesSourceProtocol(Protocol):
    def get_coordinates(self) -> Coordinates:
        raise NotImplemented


class PlugSource(CoordinatesSourceProtocol):
    latitude = 55.673768
    longitude = 37.760422

    @classmethod
    def get_coordinates(cls) -> Coordinates:
        return Coordinates(longitude=cls.longitude, latitude=cls.latitude)


class ConsoleSource(CoordinatesSourceProtocol):

    @classmethod
    def get_coordinates(cls) -> Coordinates:
        lat = input("Enter your latitude: ")
        lon = input("Enter your longitude: ")
        latitude = _parse_coordinate(coordinate_value=lat)
        longitude = _parse_coordinate(coordinate_value=lon)
        return Coordinates(longitude=longitude, latitude=latitude)


def get_coordinates(coordinates_source: CoordinatesSourceProtocol = PlugSource) -> Coordinates:
    return coordinates_source.get_coordinates()
