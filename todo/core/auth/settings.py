from pydantic import BaseSettings, Field, SecretStr


class AuthSettings(BaseSettings):
    """Settings for Authentification."""

    SECRET_KEY: SecretStr = Field(default="5ecret_k3y")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    class Config:
        """Settings for env files."""

        env_prefix = "AUTH_"
        frozen = True
