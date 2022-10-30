from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings for env files."""

    MONGODB_URL: str
    MONGODB_ADMINPASSWORD: str
    MONGODB_ADMINUSERNAME: str

    class Config:
        """Env file location."""

        env_file = ".env"
        env_file_encoding = "utf-8"
