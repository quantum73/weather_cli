import pytest

from services.coordinates import get_coordinates, PlugSource, _parse_coordinate
from utils.exceptions import CantGetCoordinates
from utils.schemas import Coordinates


class TestCoordinates:

    def test_get_coordinates(self):
        coordinates = get_coordinates(coordinates_source=PlugSource)

        assert isinstance(coordinates, Coordinates)
        assert coordinates.longitude == PlugSource.longitude
        assert coordinates.latitude == PlugSource.latitude

    def test_parse_coordinate(self):
        coordinate = _parse_coordinate(coordinate_value="1.5")

        assert isinstance(coordinate, float)
        assert coordinate == 1.5

    def test_parse_coordinate_by_bad_data(self):
        with pytest.raises(CantGetCoordinates):
            _parse_coordinate(coordinate_value="1,5")
