from environs import Env

from source.infrastructure.config.models import MaxConfig
from source.infrastructure.config.models import DobroConfig
from source.infrastructure.config.models import DatabaseConfig



def get_max_config(env: Env) -> MaxConfig:
    return MaxConfig(
        token=env.str("ACCESS_TOKEN"),
                     base_url=env.str("API_BASE"))

def get_database_config(env: Env) -> DatabaseConfig:
    return DatabaseConfig(
        user=env.str("DB_USER"),
        password=env.str("DB_PASSWORD"),
        host=env.str("DB_HOST", "db"),
        port=env.int("DB_PORT", 5432),
        path=env.str("DB_NAME"),
        driver=env.str("DB_DRIVER", "asyncpg"),
        system=env.str("DB_SYSTEM", "postgresql"),
    )

def get_dobro_config(env: Env) -> MaxConfig:
    return DobroConfig(
                     base_url=env.str("VK_DOBRO_BASE"))