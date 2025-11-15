from source.infrastructure.database.models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Integer, UUID as PG_UUID

from source.infrastructure.database.models.profile_model import Profile


class User(BaseModel):
    __tablename__ = "users"

    max_id: Mapped[str] = mapped_column(String, comment="max id", unique=True)
    username: Mapped[str] = mapped_column(String, comment="username")
    first_name: Mapped[str] = mapped_column(String, comment="Имя")
    last_name: Mapped[str] = mapped_column(String, comment="Фамилия")

    privacy_share_profile: Mapped[str] = mapped_column(String, comment="настройка приватности")

    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user_moods",
        lazy="selectin"
    )

    # total payment
