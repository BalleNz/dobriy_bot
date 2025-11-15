from datetime import datetime

from pydantic import BaseModel, Field


class ProfileSchema(BaseModel):
    max_id: str = Field(...)
    interests: str | None = Field(None)
    birthday: str = Field(None)
