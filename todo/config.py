from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    """Settings for env files."""

    MONGODB_URL: MongoDsn
    MONGODB_ADMINPASSWORD: str
    MONGODB_ADMINUSERNAME: str

    class Config:
        env_file = "config/debug.env"
