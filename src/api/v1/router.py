from api.v1.routes.chat import router as chat_router
from api.v1.routes.config import router as config_router
from api.v1.routes.prompts import router as prompts_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(config_router, prefix="/config", tags=["config"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(prompts_router, prefix="/prompts", tags=["prompts"])
