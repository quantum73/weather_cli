from services.coordinates import get_coordinates, PlugSource
from utils.schemas import Coordinates


class TestCoordinates:

    def test_get_coordinates(self):
        coordinates = get_coordinates(coordinates_source=PlugSource)

        assert isinstance(coordinates, Coordinates)
        assert coordinates.longitude == PlugSource.longitude
        assert coordinates.latitude == PlugSource.latitude
