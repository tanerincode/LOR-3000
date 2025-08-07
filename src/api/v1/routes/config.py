from core.config import get_settings
from fastapi import APIRouter

router = APIRouter()


@router.get("")
def read_config() -> dict:
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "providers": ["openai:gpt-4", "claude:opus"],
        "format_options": ["raw", "markdown", "json"],
    }
