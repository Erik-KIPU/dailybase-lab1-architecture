from backend.app.domain.health import Clock, HealthSnapshot


class HealthService:
    def __init__(self, app_name: str, version: str, environment: str, clock: Clock):
        self._app_name = app_name
        self._version = version
        self._environment = environment
        self._clock = clock
        self._started_at = clock.now()

    def check(self) -> HealthSnapshot:
        return HealthSnapshot(
            status='pass',
            app_name=self._app_name,
            version=self._version,
            environment=self._environment,
            uptime_seconds=round(max(0.0, self._clock.now() - self._started_at), 3),
        )
