import pytest


@pytest.fixture(scope="module")
def correct_weather_data_from_api():
    weather_data = {
        "coord": {
            "lon": 37.7604,
            "lat": 55.6738
        },
        "weather": [
            {
                "id": 803,
                "main": "Clouds",
                "description": "облачно с прояснениями",
                "icon": "04d"
            }
        ],
        "base": "stations",
        "main": {
            "temp": 19.8,
            "feels_like": 19.12,
            "temp_min": 19.14,
            "temp_max": 20.66,
        },
        "name": "Люблино",
    }
    return weather_data


@pytest.fixture(scope="module")
def bad_weather_data_from_api():
    weather_data = {
        "weather": [
            {
                "id": 803,
                "foo": "Clouds",
                "_": "облачно с прояснениями",
                "bar": "04d"
            }
        ],
        42: 73,
    }
    return weather_data
