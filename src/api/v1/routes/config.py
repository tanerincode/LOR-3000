from core.config import get_settings
from fastapi import APIRouter
from oven.manager import PromptOven

router = APIRouter()


@router.get("")
def read_config() -> dict:
    settings = get_settings()
    oven = PromptOven()
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "primary": settings.primary,
        "fallbacks": settings.fallbacks,
        "format_options": ["raw", "markdown", "json"],
        "max_tokens": settings.max_tokens,
        "prompts_loaded": oven.names(),
    }
