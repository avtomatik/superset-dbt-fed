from config.base import BaseConfig


class WarehouseDBConfig(BaseConfig):
    WAREHOUSE_HOST: str
    WAREHOUSE_PORT: int
    WAREHOUSE_DBNAME: str
    WAREHOUSE_USER: str
    WAREHOUSE_PASSWORD: str

    @property
    def psycopg_dsn(self) -> str:
        return (
            f"postgresql://{self.WAREHOUSE_USER}:{self.WAREHOUSE_PASSWORD}@"
            f"{self.WAREHOUSE_HOST}:{self.WAREHOUSE_PORT}/{self.WAREHOUSE_DBNAME}"
        )

    @property
    def sqlalchemy_uri(self) -> str:
        return (
            f"postgresql+psycopg://{self.WAREHOUSE_USER}:{self.WAREHOUSE_PASSWORD}@"
            f"{self.WAREHOUSE_HOST}:{self.WAREHOUSE_PORT}/{self.WAREHOUSE_DBNAME}"
        )
