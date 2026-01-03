from config.base import BaseConfig


class FredConfig(BaseConfig):
    FRED_BASE_URL: str
    FRED_API_KEY: str
    FRED_SERIES_ID: str
