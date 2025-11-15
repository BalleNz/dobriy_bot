from dishka import make_async_container, AsyncContainer

from source.infrastructure.dishka.bot import BotProvider
from source.infrastructure.dishka.config import ConfigProvider


def make_dishka_container() -> AsyncContainer:
    return make_async_container(
        *[
            ConfigProvider(),
            BotProvider(),
        ]
    )