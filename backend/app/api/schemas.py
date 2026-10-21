from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')

    status: Literal['pass']
    app_name: str
    version: str
    environment: Literal['development', 'test', 'production']
    uptime_seconds: float = Field(ge=0, description='Seconds since application startup')
