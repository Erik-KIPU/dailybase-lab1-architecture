"""Validate the Lab 2 contract and its documentation without a running API."""
from pathlib import Path
import re
import yaml
from openapi_spec_validator import validate
from openapi_schema_validator import OAS30Validator

ROOT = Path(__file__).resolve().parents[1]
spec = yaml.safe_load((ROOT / 'openapi.yaml').read_text(encoding='utf-8'))
validate(spec)

def walk(value):
    if isinstance(value, dict):
        if '$ref' in value:
            assert value['$ref'].startswith('#/'), 'Only local references expected'
            target = spec
            for token in value['$ref'][2:].split('/'):
                target = target[token.replace('~1', '/').replace('~0', '~')]
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)

walk(spec)
ids = set()
operations = set()
for path, item in spec['paths'].items():
    for method, operation in item.items():
        if method == 'parameters':
            continue
        assert operation['operationId'] not in ids
        ids.add(operation['operationId'])
        operations.add((method.upper(), '/api/v1' + path))
        if '204' in operation['responses']:
            assert 'content' not in operation['responses']['204']
        if path.startswith('/auth/'):
            assert operation['security'] == []
        else:
            assert '401' in operation['responses']

doc = (ROOT / 'ARCHITECTURE.md').read_text(encoding='utf-8')
table = set(re.findall(r'\| (GET|POST|PUT|PATCH|DELETE) \| `([^`]+)`', doc))
assert operations == table, f'Table mismatch: {operations ^ table}'
assert len(operations) >= 8
for response in spec['components']['responses'].values():
    media = response['content']['application/json']
    OAS30Validator(spec['components']['schemas']['ErrorResponse']).validate(media['example'])

print(f'OK: OpenAPI {spec["openapi"]}, {len(operations)} operations, '
      f'{len(spec["components"]["schemas"])} schemas; references, table and error examples valid.')
