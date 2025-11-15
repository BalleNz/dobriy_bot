from dishka import Provider, provide, Scope

from source.application.profile.get_by_id import GetUserProfileById
from source.application.profile.merge import MergeUserProfile
from source.application.profile.create_or_update import CreateOrUpdateProfile

from source.application.user.create_or_update import CreateOrUpdateUser



class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    # [ profile ]
    merge_profile = provide(MergeUserProfile)
    get_profile = provide(GetUserProfileById)
    profile_create_or_update = provide(CreateOrUpdateProfile)

    # [ user ]
    user_create_or_update = provide(CreateOrUpdateUser)