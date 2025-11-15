import logging

from sqlalchemy import Select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from source.infrastructure.database.models.base_model import M, S
from source.infrastructure.database.models.profile_model import Profile
from source.infrastructure.database.models.user_model import User
from source.infrastructure.database.repo.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class ProfileRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def get_profile(self, max_id: str):
        """получить профиль по макс айди"""
        stmt: Select = select(self.model).where(self.model.max_id == max_id)
        result = await self.session.execute(stmt)
        model: Profile = result.scalar_one_or_none()
        return model.get_schema() if model is not None else None

    async def update_profile(self, model_schema: S):
        """получить профиль по макс айди"""
        model: M = self.model.from_pydantic(model_schema)
        await self.session.merge(model)
