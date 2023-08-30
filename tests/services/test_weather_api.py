import pytest
from requests import Response
from requests.exceptions import ConnectionError

from config import GETTING_KEY_ERROR_MESSAGE
from services import weather_api
from utils.enums import WeatherTitle
from utils.exceptions import ApiServiceError
from utils.schemas import Celsius, Weather, Coordinates


class TestWeatherAPI:
    EXPECTED_API_ERROR_MESSAGE = "Something wrong with weather API :("
    EXPECTED_BAD_JSON_ERROR_MESSAGE = "Bad JSON data"

    def test_get_temperature(self, correct_weather_data_from_api):
        temperature = weather_api._get_temperature(data=correct_weather_data_from_api)

        assert isinstance(temperature, Celsius)
        assert temperature == 20

    def test_get_temperature_by_wrong_data(self, bad_weather_data_from_api):
        with pytest.raises(ApiServiceError) as api_err:
            weather_api._get_temperature(data=bad_weather_data_from_api)

        assert str(api_err.value) == GETTING_KEY_ERROR_MESSAGE

    def test_get_weather_title(self, correct_weather_data_from_api):
        weather_title = weather_api._get_weather_title(data=correct_weather_data_from_api)

        assert isinstance(weather_title, WeatherTitle)
        assert weather_title == WeatherTitle.clouds

    def test_get_weather_title_with_unknown_title(self):
        example_data = {"weather": [{"main": "Unexpected title"}]}
        weather_title = weather_api._get_weather_title(data=example_data)

        assert isinstance(weather_title, WeatherTitle)
        assert weather_title == WeatherTitle.unknown

    def test_get_weather_title_by_wrong_data(self, bad_weather_data_from_api):
        with pytest.raises(ApiServiceError) as api_err:
            weather_api._get_weather_title(data=bad_weather_data_from_api)

        assert str(api_err.value) == GETTING_KEY_ERROR_MESSAGE

    def test_get_geo_name(self, correct_weather_data_from_api):
        geo_name = weather_api._get_geo_name(data=correct_weather_data_from_api)

        assert isinstance(geo_name, str)
        assert geo_name.istitle()
        assert geo_name == "Люблино"

    def test_get_geo_name_by_wrong_data(self, bad_weather_data_from_api):
        with pytest.raises(ApiServiceError) as api_err:
            weather_api._get_geo_name(data=bad_weather_data_from_api)

        assert str(api_err.value) == GETTING_KEY_ERROR_MESSAGE

    def test_get_weather_by_coordinates(self, mocker, correct_weather_data_from_api):
        mock_return_value = correct_weather_data_from_api
        mocker.patch('services.weather_api._get_json_data_from_weather_api', return_value=mock_return_value)

        coordinates = Coordinates(latitude=55.6738, longitude=37.7604)
        weather = weather_api.get_weather_by_coordinates(coordinates=coordinates)

        assert isinstance(weather, Weather)
        assert weather.temperature == 20
        assert weather.weather_title == "облачно"
        assert weather.geo_name == "Люблино"

    def test_get_json_data_from_weather_api(self, mocker, correct_weather_data_from_api):
        MockResponse = mocker.patch('requests.Response')
        mock_response_instance = MockResponse.return_value
        mock_response_instance.json.return_value = correct_weather_data_from_api
        mocker.patch('requests.get', return_value=mock_response_instance)

        coordinates = Coordinates(latitude=55.6738, longitude=37.7604)
        json_data = weather_api._get_json_data_from_weather_api(coordinates=coordinates)

        assert isinstance(json_data, dict)
        assert json_data == correct_weather_data_from_api

    def test_get_json_data_from_weather_api_with_bad_json(self, mocker):
        mocker.patch('requests.get', return_value=Response())

        coordinates = Coordinates(latitude=55.6738, longitude=37.7604)
        with pytest.raises(ApiServiceError) as api_err:
            weather_api._get_json_data_from_weather_api(coordinates=coordinates)

        assert str(api_err.value) == self.EXPECTED_BAD_JSON_ERROR_MESSAGE

    def test_get_json_data_from_weather_api_with_request_error(self, mocker):
        mocker.patch('requests.get', side_effect=ConnectionError())

        coordinates = Coordinates(latitude=55.6738, longitude=37.7604)
        with pytest.raises(ApiServiceError) as api_err:
            weather_api._get_json_data_from_weather_api(coordinates=coordinates)

        assert str(api_err.value) == self.EXPECTED_API_ERROR_MESSAGE

    def test_formatting_response_from_api(self, correct_weather_data_from_api):
        weather = weather_api._formatting_response_from_api(weather_data=correct_weather_data_from_api)

        assert isinstance(weather, Weather)
        assert weather.temperature == 20
        assert weather.weather_title == "облачно"
        assert weather.geo_name == "Люблино"

    def test_formatting_response_from_api_with_bad_data(self, bad_weather_data_from_api):
        with pytest.raises(ApiServiceError) as api_err:
            weather_api._formatting_response_from_api(weather_data=bad_weather_data_from_api)

        assert str(api_err.value) == GETTING_KEY_ERROR_MESSAGE
