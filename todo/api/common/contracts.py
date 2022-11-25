from caseconverter import camelcase  # noqa
from pydantic import BaseModel


class JSONContract(BaseModel):
    """Base contract for managing json-loved camel case."""

    class Config:  # noqa
        alias_generator = camelcase
