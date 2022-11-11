from pydantic import BaseSettings, Field, SecretStr


class MongoSettings(BaseSettings):
    """Settings for MongoDB connection."""

    HOST: str = Field(default="localhost")
    PORT: int = Field(default=27017)
    USERNAME: str = Field(default="admin")
    PASSWORD: SecretStr = Field(default="pa55w0rd")
    DATABASE: str = Field(default="todo")

    class Config:  # noqa
        env_prefix = "MONGO_"
        frozen = True

    def connection_str(self) -> str:  # noqa
        return (
            "mongodb://"
            f"{self.USERNAME}:{self.PASSWORD.get_secret_value()}"
            f"@{self.HOST}:{self.PORT}"
        )
