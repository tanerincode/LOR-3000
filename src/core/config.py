from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "LOR-3000"
    environment: str = "development"

    # Providers
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    # Datastores
    database_url: str | None = None
    redis_url: str | None = None

    # Routing & Output
    primary: str = "openai:gpt-4"
    fallbacks: list[str] = ["claude:opus"]
    format: str = "markdown"
    max_tokens: int = 4000
    prompts_file: str | None = None

    @classmethod
    def settings_customise_sources(
        cls,
        _settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[Any, ...]:
        def external_file_source() -> dict[str, Any]:
            path = (
                os.getenv("APP_CONFIG_FILE")
                or os.getenv("LOR3_CONFIG_FILE")
                or os.getenv("CONFIG_FILE")
            )
            if not path:
                return {}
            file_path = Path(path)
            if not file_path.exists():
                return {}
            try:
                if file_path.suffix.lower() in {".yaml", ".yml"}:
                    try:
                        import yaml  # type: ignore
                    except Exception as exc:  # noqa: BLE001
                        raise RuntimeError("pyyaml is required to load YAML config files") from exc
                    with file_path.open("r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                else:
                    with file_path.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                if not isinstance(data, dict):
                    return {}
                return data
            except Exception:
                # On any parse error, ignore external file and rely on env/defaults
                return {}

        # Precedence (earlier wins): init > env > dotenv > external file > secrets
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            external_file_source,
            file_secret_settings,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


class PydanticBaseSettingsSourceCallable:  # Deprecated shim (no longer used)
    pass
