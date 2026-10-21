from pathlib import Path

from fastapi.testclient import TestClient
from openapi_schema_validator import OAS30Validator
import yaml

from backend.app.config.settings import Settings
from backend.app.main import create_app


def test_real_response_matches_design_contract():
    root = Path(__file__).resolve().parents[1]
    spec = yaml.safe_load((root / 'openapi.yaml').read_text(encoding='utf-8'))
    contract = spec['components']['schemas']['HealthResponse']
    with TestClient(create_app(Settings(_env_file=None))) as client:
        result = client.get('/api/v1/health')
    assert result.status_code == 200
    OAS30Validator(contract).validate(result.json())
