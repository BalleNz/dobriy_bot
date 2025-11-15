from pydantic import (
    BaseModel,
    SecretStr,
    PostgresDsn
)


class MaxConfig(BaseModel):
    token: SecretStr
    base_url: str

class DatabaseConfig(BaseModel):
    user: str
    password: SecretStr
    path: str
    host: str = "db"
    port: int = 5432
    driver: str = "asyncpg"
    system: str = "postgresql"

    def build_connection_url(self) -> str:
        dsn: PostgresDsn = PostgresDsn.build(
            scheme=f"{self.system}+{self.driver}",
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password.get_secret_value(),
            path=self.path
        )
        return dsn.unicode_string()

class DobroConfig(BaseModel):
    base_url: str
