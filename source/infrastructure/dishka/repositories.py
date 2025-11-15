
from dishka import Provider, provide, Scope

from source.infrastructure.database.repo.profile_repo import ProfileRepository
from source.infrastructure.database.repo.user_repo import UserRepository




class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    user_repository = provide(UserRepository)
    profile_repository = provide(ProfileRepository)