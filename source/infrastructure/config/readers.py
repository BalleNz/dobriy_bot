from environs import Env

from source.infrastructure.config.models import MaxConfig


def get_max_client(env: Env) -> MaxConfig:
    return MaxConfig(
        token=env.str("ACCESS_TOKEN"),
                     base_url=env.str("API_BASE"))