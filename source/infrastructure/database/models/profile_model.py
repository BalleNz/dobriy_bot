from datetime import datetime
from typing import Type

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.core.schemas.profile import ProfileSchema
from source.infrastructure.database.models.base_model import BaseModel, S


class Profile(BaseModel):
    __tablename__ = "profile_settings"

    max_id: Mapped[str] = mapped_column(String, comment="max_bot id", unique=True)

    interests: Mapped[str] = mapped_column(String, comment="интересы")
    birthday: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, server_default=None)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def schema_class(cls) -> Type[S]:
        return ProfileSchema
