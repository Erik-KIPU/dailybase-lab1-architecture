from dataclasses import dataclass
from typing import Literal, Protocol


class Clock(Protocol):
    """A monotonic time source, supplied by the outer infrastructure layer."""

    def now(self) -> float: ...


@dataclass(frozen=True)
class HealthSnapshot:
    status: Literal['pass']
    app_name: str
    version: str
    environment: str
    uptime_seconds: float
