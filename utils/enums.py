from enum import Enum


class WeatherTitle(str, Enum):
    thunderstorm = "гроза"
    drizzle = "изморось"
    rain = "дождь"
    snow = "снег"
    mist = "туман"
    smoke = "дым"
    haze = "дымка"
    dust = "пыль"
    fog = "туман"
    sand = "песок"
    ash = "пепел"
    squall = "шквалы"
    tornado = "торнадо"
    clear = "ясное небо"
    clouds = "облачно"
    unknown = "неизвестно"

    @classmethod
    def get(cls, key) -> "WeatherTitle":
        _data = {item.name: item for item in cls}
        value = _data.get(key, cls.unknown)
        return value


class CoordinatesInputType(str, Enum):
    plug = "plug"
    console = "console"

    @classmethod
    def to_str(cls) -> str:
        return ', '.join([item.value for item in cls])

    @classmethod
    def choices(cls):
        return [item.value for item in cls]
