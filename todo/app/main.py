from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """Example endpoint just to add app to docker."""
    return {"message": "Hello World"}
