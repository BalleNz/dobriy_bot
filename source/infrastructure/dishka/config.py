from dishka import Provider, provide, Scope
from source.infrastructure.config import MaxConfig, get_max_config
from source.infrastructure.config import DobroConfig, get_dobro_config
from source.infrastructure.config import DatabaseConfig, get_database_config


from environs import Env


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_max_config(self, env: Env) -> MaxConfig:
        return get_max_config(env)
    
    @provide
    def get_dobro_config(self, env: Env) -> DobroConfig:
        return get_dobro_config(env)
    
    @provide
    def get_db_config(self, env: Env) -> DatabaseConfig:
        return get_database_config(env)
    
    @provide
    def get_env(self) -> Env:
        env = Env()
        env.read_env()
        return env