import os
from pathlib import Path
from typing import TypeAlias, Mapping, MutableMapping, Any

from dotenv import dotenv_values

ConfigMap: TypeAlias = Mapping[str, str | None] | MutableMapping[str, Any]

ENV_PATH = Path("./.env")
config: ConfigMap = os.environ if not ENV_PATH.exists() else dotenv_values(ENV_PATH)

HEADERS = {
    "Content-Type": "application/json",
}
DATETIME_FORMAT = "%H:%M %d.%m.%Y"
API_KEY = config.get("OPEN_WEATHER_API_KEY")
if API_KEY is None:
    raise EnvironmentError("Environment variable API_KEY is not set")

WEATHER_API_URL = (
        "https://api.openweathermap.org/data/2.5/weather?"
        "lat={latitude}&lon={longitude}&lang=ru"
        "&appid=" + API_KEY + "&units=metric"
)
