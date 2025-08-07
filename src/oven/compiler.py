from __future__ import annotations

from string import Template
from typing import Mapping

from oven.schemas import PromptRecord


def compile_prompt(record: PromptRecord, variables: Mapping[str, str] | None = None) -> str:
    base = record.system
    if not variables:
        return base
    # Use safe substitution to avoid KeyErrors for missing vars
    return Template(base).safe_substitute(**variables)


