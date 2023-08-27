from utils.schemas import Coordinates


def get_coordinates() -> Coordinates:
    latitude, longitude = 55.670640, 37.760934
    # TODO: Some third-party program call
    return Coordinates(longitude=longitude, latitude=latitude)
