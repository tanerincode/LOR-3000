from abc import ABC, abstractmethod
from typing import Tuple


class Provider(ABC):
    name: str

    @abstractmethod
    def generate(self, prompt: str, *, output_format: str = "markdown") -> Tuple[str, str]:
        """Return (content, provider_name)."""
        raise NotImplementedError
