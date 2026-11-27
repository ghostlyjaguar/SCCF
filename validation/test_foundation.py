"""Synthetic policy tests; no operational detection or empirical validation."""
import copy
import unittest
from validate import ROOT, load, validate_entry, main
from jsonschema.exceptions import ValidationError

def assess(activities, link, alternatives):
    # Inputs are evidence assessments already made by an investigator.
    if link == "contradicted":
        return "contradicted"
    if activities < 2:
        return "insufficient_evidence"
    if link == "supported" and alternatives == "resolved":
        return "supported"
    return "hypothesis"

class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.schema = load(ROOT / "schemas/composition.schema.json")
        self.entry = load(ROOT / "taxonomy/compositions/SCCF-0001.json")

    def test_catalog(self):
        main()

    def test_policy_fixtures(self):
        for case in load(ROOT / "validation/fixtures.json"):
            with self.subTest(case=case["id"]):
                self.assertEqual(assess(case["activities"], case["link"], case["alternatives"]), case["expected"])

    def test_single_activity_invalid(self):
        entry = copy.deepcopy(self.entry)
        entry["roles"] = entry["roles"][:1]
        with self.assertRaises(ValidationError):
            validate_entry(entry, self.schema)

    def test_self_loop_invalid(self):
        entry = copy.deepcopy(self.entry)
        entry["graph"]["edges"][0]["target"] = "a"
        with self.assertRaises(ValueError):
            validate_entry(entry, self.schema)

    def test_dangling_edge_invalid(self):
        entry = copy.deepcopy(self.entry)
        entry["graph"]["edges"][0]["target"] = "missing"
        with self.assertRaises(ValueError):
            validate_entry(entry, self.schema)

    def test_acceptance_requires_review(self):
        entry = copy.deepcopy(self.entry)
        entry["status"] = "accepted"
        entry["review"] = None
        with self.assertRaises(ValidationError):
            validate_entry(entry, self.schema)

if __name__ == "__main__":
    unittest.main()
