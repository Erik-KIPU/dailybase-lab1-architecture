from typing import Annotated

from fastapi import APIRouter, Depends, Response

from backend.app.api.dependencies import get_health_service
from backend.app.api.schemas import HealthResponse
from backend.app.services.health import HealthService

router = APIRouter(prefix='/api/v1', tags=['Health'])


@router.get('/health', response_model=HealthResponse, operation_id='get_health',
            summary='Проверка работоспособности процесса')
def health(response: Response,
           service: Annotated[HealthService, Depends(get_health_service)]) -> HealthResponse:
    response.headers['Cache-Control'] = 'no-store'
    snapshot = service.check()
    return HealthResponse(
        status=snapshot.status,
        app_name=snapshot.app_name,
        version=snapshot.version,
        environment=snapshot.environment,
        uptime_seconds=snapshot.uptime_seconds,
    )
