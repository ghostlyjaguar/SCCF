"""Structural validation only; never confers scientific acceptance."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def check(condition, message):
    if not condition:
        raise ValueError(message)

def validate_entry(entry, schema):
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(entry)
    graph = entry["graph"]
    ids = [n["id"] for n in graph["nodes"]]
    check(len(ids) == len(set(ids)), "duplicate node ID")
    check(sorted(n["role"] for n in graph["nodes"]) == sorted(entry["roles"]), "roles disagree with graph")
    connected = {i: set() for i in ids}
    seen = set()
    for edge in graph["edges"]:
        s, t = edge["source"], edge["target"]
        check(s in connected and t in connected and s != t, "invalid edge endpoints")
        key = (s, t, edge["relationship"])
        check(key not in seen, "duplicate functional edge")
        seen.add(key)
        connected[s].add(t)
        connected[t].add(s)
    check(any(edge["relationship"] == entry["relationship"] for edge in graph["edges"]), "primary relationship absent")
    reached, pending = set(), [ids[0]]
    while pending:
        node = pending.pop()
        if node not in reached:
            reached.add(node)
            pending.extend(connected[node] - reached)
    check(reached == set(ids), "disconnected roles")

def main():
    schema = load(ROOT / "schemas/composition.schema.json")
    Draft202012Validator.check_schema(schema)
    charter = load(ROOT / "foundation/charter.json")
    check([p["id"] for p in charter["principles"]] == [f"F-{i:02}" for i in range(1, 8)], "charter principle IDs changed")
    paths = sorted((ROOT / "taxonomy/compositions").glob("*.json"))
    check(bool(paths), "no composition entries")
    seen = set()
    for path in paths:
        entry = load(path)
        validate_entry(entry, schema)
        check(entry["id"] == path.stem, "filename/ID mismatch")
        check(entry["id"] not in seen, "duplicate class ID")
        seen.add(entry["id"])
        print(f'PASS {entry["id"]} ({entry["status"]}; structural only)')
    check("SCCF-0001" in seen, "founding ID missing")

if __name__ == "__main__":
    main()
