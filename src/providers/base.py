from abc import ABC, abstractmethod
from typing import Tuple


class Provider(ABC):
    name: str

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        output_format: str = "markdown",
        system: str | None = None,
    ) -> Tuple[str, str]:
        """Return (content, provider_name)."""
        raise NotImplementedError
