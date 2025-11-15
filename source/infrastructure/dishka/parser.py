from dishka import Provider, provide, Scope

from source.infrastructure.parser.dobro import DobroApiClient

class ParsersProvider(Provider):
    scope = Scope.APP

    @provide
    def get_dobro(self) -> DobroApiClient:
        return DobroApiClient()