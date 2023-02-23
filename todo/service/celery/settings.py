from pydantic import BaseSettings, Field, SecretStr


class CelerySettings(BaseSettings):
    """Settings for MongoDB connection."""

    NAME: str = Field(default="tasks")
    HOST: str = Field(default="rabbitmq")
    PORT: int = Field(default=5672)
    USERNAME: str = Field(default="admin")
    PASSWORD: SecretStr = Field(default="pa55w0rd")
    DATABASE: str = Field(default="todo")

    class Config:
        """Settings for env files."""

        env_prefix = "CELERY_"
        frozen = True

    def connection_str(self) -> str:
        """Constructor for mongodb connection string."""
        return (
            "pyamqp://"
            f"{self.USERNAME}:{self.PASSWORD.get_secret_value()}"
            f"@{self.HOST}:{self.PORT}"
        )
