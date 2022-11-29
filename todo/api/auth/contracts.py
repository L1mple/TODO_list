from todo.api.common.contracts import JSONContract
from todo.core.auth.models import Token


class TokenJSONResponse(JSONContract):
    """JSONRespponse for Task."""

    access_token: str
    token_type: str

    @staticmethod
    def from_entity(entity: Token) -> "TokenJSONResponse":
        """Convert Task to JSONResponse."""
        return TokenJSONResponse(**entity.dict())
