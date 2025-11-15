from dishka import Provider, provide, Scope
from source.infrastructure.config import MaxConfig, get_max_client

from environs import Env


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_config(self, env: Env) -> MaxConfig:
        return get_max_client(env)
    
    @provide
    def get_env(self) -> Env:
        env = Env()
        env.read_env()
        return env