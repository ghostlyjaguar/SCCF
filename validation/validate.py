import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
root = Path(__file__).resolve().parents[1]
schema = json.loads((root / 'schemas/composition.schema.json').read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=FormatChecker())
paths = sorted((root / 'taxonomy/compositions').glob('*.json'))
assert paths, 'No composition entries found'
seen = set()
for path in paths:
    entry = json.loads(path.read_text())
    validator.validate(entry)
    assert entry['id'] == path.stem, f'ID mismatch: {path}'
    assert entry['id'] not in seen, f'Duplicate ID: {path}'
    seen.add(entry['id'])
    print(f'PASS {entry["id"]}')
