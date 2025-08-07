from api.v1.router import api_router
from core.config import get_settings
from fastapi import FastAPI

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/healthz")
def health() -> dict:
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1")
