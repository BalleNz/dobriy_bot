
from dishka import Provider, provide, Scope


class RepositoryProvider(Provider):
    scope = Scope.REQUEST