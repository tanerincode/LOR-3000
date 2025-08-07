from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import yaml

from oven.schemas import PromptRecord


def load_prompts_from_file(path: str | Path) -> Dict[str, PromptRecord]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    if file_path.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(file_path.read_text(encoding="utf-8"))
    elif file_path.suffix.lower() == ".json":
        data = json.loads(file_path.read_text(encoding="utf-8"))
    else:
        raise ValueError("Unsupported prompt file format; use YAML or JSON")

    if not isinstance(data, dict):
        raise ValueError("Prompt file must be a mapping of name -> record")

    prompts: Dict[str, PromptRecord] = {}
    for name, record in data.items():
        if not isinstance(record, dict):
            raise ValueError(f"Prompt record for '{name}' must be a mapping")
        prompts[name] = PromptRecord(name=name, **record)
    return prompts


