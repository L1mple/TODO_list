from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


class CryptService:
    """Crypt settings."""

    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthScheme:
    """Class for DI OAuth2PasswordBearer."""

    def __init__(self, token_url: str) -> None:
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)
