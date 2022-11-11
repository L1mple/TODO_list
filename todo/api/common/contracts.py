"""Module for storing HTTP Request/Response Contracts for all submodules.

Term "Contract" had been picked due to it philological nature. Contract means some
agreement and request/response models are actually some agreements between app and it's
clients.

Request classes have "Request" postfix, response - "Response"

It is also good idea to mention which format of request/response body we want to have
and mark it in the name. So for json request response it is also good to include "JSON"
prefix.
"""
from caseconverter import camelcase  # noqa
from pydantic import BaseModel


class JSONContract(BaseModel):
    """Base contract for managing json-loved camel case."""

    class Config:  # noqa
        alias_generator = camelcase
