from caseconverter import camelcase  # noqa
from pydantic import EmailStr
from toolz import keymap

from todo.api.common.contracts import JSONContract
from todo.core.user.models import User
from todo.core.common.models import IdentityUID

class UserJSONResponse(JSONContract):
    """JSONRespponse for User."""

    uid: str

    username: str
    email: EmailStr
    full_name: str | None
    active: bool
    admin: bool
    identity: IdentityUID

    @staticmethod
    def from_entity(entity: User) -> "UserJSONResponse":
        """Convert User to JSONResponse."""
        return UserJSONResponse(**keymap(camelcase, entity.dict()))
