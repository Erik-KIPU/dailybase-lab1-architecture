from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from backend.app.config.settings import Settings
from backend.app.main import create_app
from backend.app.services.health import HealthService


class FakeClock:
    value = 100.0

    def now(self):
        return self.value


def test_service_uptime_uses_injected_clock():
    clock = FakeClock()
    service = HealthService('test', '1.2.3', 'test', clock)
    clock.value = 112.5
    snapshot = service.check()
    assert snapshot.uptime_seconds == 12.5
    assert snapshot.app_name == 'test'


def test_health_endpoint_and_live_schema():
    settings = Settings(_env_file=None, app_name='Health Test', app_version='2.0.0', app_env='test')
    with TestClient(create_app(settings)) as client:
        first = client.get('/api/v1/health')
        second = client.get('/api/v1/health')
        assert first.status_code == 200
        assert first.headers['content-type'] == 'application/json'
        assert first.headers['cache-control'] == 'no-store'
        data = first.json()
        assert set(data) == {'status','app_name','version','environment','uptime_seconds'}
        assert data['status'] == 'pass'
        assert data['app_name'] == 'Health Test'
        assert data['version'] == '2.0.0'
        assert data['environment'] == 'test'
        assert 0 <= data['uptime_seconds'] <= second.json()['uptime_seconds']
        schema = client.get('/openapi.json').json()
        assert set(schema['paths']) == {'/api/v1/health'}
        assert client.get('/api/v1/students').status_code == 404


def test_dotenv_and_environment_precedence(tmp_path, monkeypatch):
    for name in ['APP_NAME','APP_VERSION','APP_ENV','HTTP_HOST','HTTP_PORT']:
        monkeypatch.delenv(name, raising=False)
    dotenv = tmp_path / '.env'
    dotenv.write_text('APP_NAME="Имя из файла"\nHTTP_PORT=8123\nAPP_ENV=test\n', encoding='utf-8')
    config = Settings(_env_file=dotenv)
    assert config.app_name == 'Имя из файла'
    assert config.http_port == 8123
    monkeypatch.setenv('HTTP_PORT', '8124')
    assert Settings(_env_file=dotenv).http_port == 8124


@pytest.mark.parametrize('port', ['0', '65536', 'invalid'])
def test_invalid_port_fails_fast(monkeypatch, port):
    monkeypatch.setenv('HTTP_PORT', port)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_environment_fails_fast(monkeypatch):
    monkeypatch.setenv('APP_ENV', 'unknown')
    with pytest.raises(ValidationError):
        Settings(_env_file=None)
