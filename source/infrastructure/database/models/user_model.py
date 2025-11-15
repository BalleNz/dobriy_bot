from typing import Type

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.core.schemas.user import UserSchema
from source.infrastructure.database.models.base_model import BaseModel, S
from source.infrastructure.database.models.profile_model import Profile


class User(BaseModel):
    __tablename__ = "users"

    max_id: Mapped[str] = mapped_column(String, comment="max id", unique=True)
    username: Mapped[str] = mapped_column(String, comment="username")
    first_name: Mapped[str] = mapped_column(String, default=None, comment="Имя")
    last_name: Mapped[str] = mapped_column(String, default=None, comment="Фамилия")

    privacy_share_profile: Mapped[str] = mapped_column(String, comment="настройка приватности")

    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user_moods",
        lazy="selectin"
    )

    # total payment

    def schema_class(cls) -> Type[S]:
        return UserSchema
