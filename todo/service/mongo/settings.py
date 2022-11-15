from pydantic import BaseSettings, Field, SecretStr


class MongoSettings(BaseSettings):
    """Settings for MongoDB connection."""

    HOST: str = Field(default="mongo")
    PORT: int = Field(default=27017)
    USERNAME: str = Field(default="admin")
    PASSWORD: SecretStr = Field(default="pa55w0rd")
    DATABASE: str = Field(default="todo")

    class Config:
        """Settings for env files."""

        env_prefix = "MONGO_"
        frozen = True

    def connection_str(self) -> str:
        """Constructor for mongodb connection string."""
        return (
            "mongodb://"
            f"{self.USERNAME}:{self.PASSWORD.get_secret_value()}"
            f"@{self.HOST}:{self.PORT}"
        )
