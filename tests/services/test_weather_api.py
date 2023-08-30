import pytest

from config import GETTING_KEY_ERROR_MESSAGE
from services import weather_api
from services.weather_api import _formatting_response_from_api
from utils.enums import WeatherTitle
from utils.exceptions import ApiServiceError
from utils.schemas import Celsius, Weather


class TestWeatherAPI:
    EXPECTED_API_ERROR_MESSAGE = "Something wrong with weather API :("
    EXPECTED_GETTING_JSON_ERROR_MESSAGE = "Bad JSON data"
    EXPECTED_BAD_JSON_ERROR_MESSAGE = "Error in retrieving data from JSON"

    def test_get_temperature(self):
        example_data = {"main": {"temp": 15.9}}
        temperature = weather_api._get_temperature(data=example_data)

        assert isinstance(temperature, Celsius)
        assert temperature == 16

    def test_get_temperature_by_wrong_data(self):
        example_data = {"main": {"temperature": 15.9}}
        with pytest.raises(ApiServiceError) as api_err:
            weather_api._get_temperature(data=example_data)

        assert str(api_err.value) == self.EXPECTED_BAD_JSON_ERROR_MESSAGE

    def test_get_weather_title(self):
        example_data = {"weather": [{"main": "Clouds"}]}
        weather_title = weather_api._get_weather_title(data=example_data)

        assert isinstance(weather_title, WeatherTitle)
        assert weather_title == WeatherTitle.clouds

    def test_get_weather_title_with_unknown_title(self):
        example_data = {"weather": [{"main": "Unexpected title"}]}
        weather_title = weather_api._get_weather_title(data=example_data)

        assert isinstance(weather_title, WeatherTitle)
        assert weather_title == WeatherTitle.unknown

    def test_get_weather_title_by_wrong_data(self):
        example_data = {"weather": {"main": "Clouds"}}
        with pytest.raises(ApiServiceError) as api_err:
            weather_api._get_weather_title(data=example_data)

        assert str(api_err.value) == self.EXPECTED_BAD_JSON_ERROR_MESSAGE

    def test_get_geo_name(self):
        example_data = {"name": "moscow"}
        geo_name = weather_api._get_geo_name(data=example_data)

        assert isinstance(geo_name, str)
        assert geo_name.istitle()
        assert geo_name == "Moscow"

    def test_get_geo_name_by_wrong_data(self):
        example_data = {"foo": "bar"}
        with pytest.raises(ApiServiceError) as api_err:
            weather_api._get_geo_name(data=example_data)

        assert str(api_err.value) == self.EXPECTED_BAD_JSON_ERROR_MESSAGE

    # TODO: test get_weather_by_coordinates
    # TODO: test _get_json_data_from_weather_api
    def test_formatting_response_from_api(self):
        target_weather_data = {
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
        weather = _formatting_response_from_api(weather_data=target_weather_data)

        assert isinstance(weather, Weather)
        assert weather.temperature
        assert weather.weather_title
        assert weather.geo_name
        assert weather.now_datetime

    def test_formatting_response_from_api_with_bad_data(self):
        bad_weather_data = {
            "weather": [
                {
                    "id": 803,
                    "foo": "Clouds",
                    "_": "облачно с прояснениями",
                    "bar": "04d"
                }
            ],
        }
        with pytest.raises(ApiServiceError) as api_err:
            _formatting_response_from_api(weather_data=bad_weather_data)

        assert str(api_err.value) == GETTING_KEY_ERROR_MESSAGE
