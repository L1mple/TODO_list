from beanie import Document, PydanticObjectId

from todo.core.auth.models import Identity, IdentityUID


class IdentityMongoDb(Document):
    """Database model for Identity."""

    hashed_password: str

    class Settings:
        """Config for IdentityMongoDb."""

        name = "identities"

    def to_entity(self) -> Identity:
        """Convert Dbmodel to Domain."""
        return Identity(
            uid=IdentityUID(self.id),
            **self.dict(exclude={"id"}),  # Возможно тут надо написать {"_id"}
        )

    @staticmethod
    def from_identity_entity(entity: Identity) -> "IdentityMongoDb":
        """Convert Identity to IdentityMongoDb."""
        return IdentityMongoDb(
            _id=PydanticObjectId(entity.uid),
            **entity.dict(exclude={"uid"}),
        )
