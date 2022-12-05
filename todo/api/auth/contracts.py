from pydantic import BaseModel

from todo.core.auth.models import Token


class TokenJSONResponse(BaseModel):
    """JSONRespponse for Task."""

    access_token: str
    token_type: str

    @staticmethod
    def from_entity(entity: Token) -> "TokenJSONResponse":
        """Convert Task to JSONResponse."""
        return TokenJSONResponse(**entity.dict())
