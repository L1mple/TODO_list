from fastapi import FastAPI


def create_api() -> FastAPI:
    """Init FastAPI instance."""
    api = FastAPI()
    return api
