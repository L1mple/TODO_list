from pydantic import BaseSettings, Field, SecretStr


class CelerySettings(BaseSettings):
    """Settings for MongoDB connection."""

    NAME: str = Field(default="tasks")
    BROKER_HOST: str = Field(default="rabbitmq")
    BROKER_PORT: int = Field(default=5672)
    BROKER_USERNAME: str = Field(default="admin")
    BROKER_PASSWORD: SecretStr = Field(default="pa55w0rd")
    BROKER_DATABASE: str = Field(default="todo")
    RESULT_HOST: str = Field(default="redis")
    RESULT_PORT: int = Field(default=6379)
    RESULT_PASSWORD: SecretStr = Field(default="pa55w0rd")

    class Config:
        """Settings for env files."""

        env_prefix = "CELERY_"
        frozen = True

    def get_name(self) -> str:
        """Get name of worker."""
        return f"{self.NAME}"

    def broker_connection_str(self) -> str:
        """Constructor for rabbitmq connection string."""
        return (
            "pyamqp://"
            f"{self.BROKER_USERNAME}:{self.BROKER_PASSWORD.get_secret_value()}"
            f"@{self.BROKER_HOST}:{self.BROKER_PORT}"
        )

    def result_connection_str(self) -> str:
        """Constructor for redis connection string."""
        return (
            "redis://"
            f":{self.RESULT_PASSWORD.get_secret_value()}"
            f"@{self.RESULT_HOST}:{self.RESULT_PORT}/0"
        )
