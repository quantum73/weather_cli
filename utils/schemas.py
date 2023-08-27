from dataclasses import dataclass, field
from datetime import datetime

from config import DATETIME_FORMAT
from utils.enums import WeatherTitle

Celsius = int


def _get_now_datetime_as_string() -> str:
    str_now_datetime = datetime.now().strftime(DATETIME_FORMAT)
    return str_now_datetime


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_title: WeatherTitle
    geo_name: str | None = None
    now_datetime: str = field(default_factory=_get_now_datetime_as_string, init=False)
