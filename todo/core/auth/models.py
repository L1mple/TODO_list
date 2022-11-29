from pydantic import BaseModel


class Token(BaseModel):
    """Domain model for AuthToken."""

    access_token: str
    token_type: str
