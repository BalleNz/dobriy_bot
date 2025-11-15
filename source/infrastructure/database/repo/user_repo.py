import logging

from sqlalchemy import Select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from source.core.schemas.user import UserSchema
from source.infrastructure.database.models.user_model import User
from source.infrastructure.database.repo.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def get_schema_by_max_id(self, max_id: str) -> UserSchema | None:
        stmt: Select = select(self.model).where(self.model.max_id == max_id)
        result = await self.session.execute(stmt)
        model: User = result.scalar_one_or_none()
        return model.get_schema() if model is not None else None

    async def get_model_by_max_id(self, max_id: str) -> User | None:
        stmt: Select = select(self.model).where(self.model.max_id == max_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


