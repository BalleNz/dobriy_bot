from dishka import Provider, provide, Scope

from source.application.profile.get_by_id import GetUserProfileById
from source.application.profile.merge import MergeUserProfile


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    # [ profile ]
    merge_profile = provide(MergeUserProfile)
    get_profile = provide(GetUserProfileById)