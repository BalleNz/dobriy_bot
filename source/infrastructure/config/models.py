from pydantic import (
    BaseModel,
    SecretStr,
)


class MaxConfig(BaseModel):
    token: SecretStr
    base_url: str
