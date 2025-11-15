from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    max_id: str = Field(...)
    username: str = Field(...)
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
