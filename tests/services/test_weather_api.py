import pytest

from services import weather_api
from utils.enums import WeatherTitle
from utils.exceptions import ApiException
from utils.schemas import Celsius


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
        with pytest.raises(ApiException) as api_err:
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
        with pytest.raises(ApiException) as api_err:
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
        with pytest.raises(ApiException) as api_err:
            weather_api._get_geo_name(data=example_data)

        assert str(api_err.value) == self.EXPECTED_BAD_JSON_ERROR_MESSAGE

    # TODO: test _formatting_response_from_api
    # TODO: test _get_json_data_from_weather_api
    # TODO: test get_weather_by_coordinates
