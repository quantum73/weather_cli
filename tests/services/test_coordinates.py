from services.coordinates import get_coordinates
from utils.schemas import Coordinates


class TestCoordinates:

    def test_get_coordinates(self):
        coordinates = get_coordinates()

        assert isinstance(coordinates, Coordinates)
        assert isinstance(coordinates.longitude, float)
        assert isinstance(coordinates.latitude, float)
