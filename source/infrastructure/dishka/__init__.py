from dishka import make_async_container, AsyncContainer

from source.infrastructure.dishka.bot import BotProvider
from source.infrastructure.dishka.config import ConfigProvider
from source.infrastructure.dishka.parser import ParsersProvider
from source.infrastructure.dishka.db import DatabaseProvider
from source.infrastructure.dishka.interactors import InteractorsProvider
from source.infrastructure.dishka.repositories import RepositoryProvider



def make_dishka_container() -> AsyncContainer:
    return make_async_container(
        *[
            ConfigProvider(),
            BotProvider(),
            ParsersProvider(),
            DatabaseProvider(),
            InteractorsProvider(),
            RepositoryProvider()
        ]
    )