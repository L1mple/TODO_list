from fastapi import FastAPI


def create_app() -> FastAPI:
    """Init FastAPI instance."""
    app = FastAPI()
    return app
