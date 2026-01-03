from config.base import BaseConfig


class SupersetConfig(BaseConfig):
    SUPERSET_SECRET_KEY: str
    SUPERSET_LOAD_EXAMPLES: bool = False
