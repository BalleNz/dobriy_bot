from dishka import Provider, provide, Scope

from source.infrastructure.config import MaxConfig
from source.infrastructure.max.api_client import MaxBotClient

class BotProvider(Provider):
    scope = Scope.APP

    @provide
    def get_bot(self, config: MaxConfig) -> MaxBotClient:
        return MaxBotClient(
            token=config.token.get_secret_value(),
            base_url=config.base_url
        )