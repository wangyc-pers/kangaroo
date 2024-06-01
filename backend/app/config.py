from typing import Union, Optional

from pydantic import AnyUrl, MySQLDsn, PostgresDsn, UrlConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated

SQLiteDsn = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["sqlite"])]
RedisDsn = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["redis"])]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )
    # Default
    DEBUG: bool = True
    LOG_FILE: str = "./logs/siteby.log"

    # Database
    SQLALCHEMY_DB_URL: Union[MySQLDsn, PostgresDsn, SQLiteDsn] = "sqlite:///./test.db"

    # SnowFlake setting
    SNOWFLAKE_WORKER_ID: int = 1
    SNOWFLAKE_DATA_CENTER_ID: int = 1

    # Redis
    REDIS_URL: Optional[RedisDsn] = None


settings = Settings()
