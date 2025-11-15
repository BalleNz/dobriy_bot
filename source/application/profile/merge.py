from typing import TypeVar

from pydantic import BaseModel as BaseModelSchema

from source.application.base import Interactor
from source.core.schemas import UserSchema
from source.infrastructure.database.repo.profile_repo import ProfileRepository
from source.infrastructure.database.uow import UnitOfWork

S = TypeVar("S", bound=BaseModelSchema)


class MergeUserProfile(Interactor[UserSchema, S]):
    def __init__(self, repository: ProfileRepository, uow: UnitOfWork):
        self.repository = repository
        self.uow = uow

    async def __call__(self, user: UserSchema) -> None:
        try:
            async with self.uow:
                user = await self.repository.merge(
                    user
                )
                await self.uow.commit()
                return user
        except Exception as exc:
            pass