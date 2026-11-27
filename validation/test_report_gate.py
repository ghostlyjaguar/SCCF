"""Deliberate false-report simulations using synthetic evidence only."""
import copy
import unittest
from report_gate import assess

REV = "example-revision"
EVIDENCE = {
    "revision": REV,
    "files": {"example.py": "blob1"},
    "pull_request": {"number": 4, "head_revision": REV, "merged": False},
    "runs": {"100": {"revision": REV, "status": "completed", "conclusion": "success",
                     "output_inspected": True,
                     "metrics": {"cases": {"value": 240000, "unit": "cases"}}}},
    "warnings": ["Example dependency warning"],
}
TEST = {"kind": "test_passed", "revision": REV, "run_id": "100"}
METRIC = {**TEST, "kind": "metric", "name": "cases", "value": 240000, "unit": "cases"}

class ReportGateTests(unittest.TestCase):
    def verify(self, claim, expected, mutate=None):
        evidence = copy.deepcopy(EVIDENCE)
        if mutate:
            mutate(evidence)
        result = assess(claim, evidence)
        self.assertEqual(result["accepted"], expected, result)
        self.assertEqual(result["warnings"], EVIDENCE["warnings"])
        self.assertEqual(bool(result["reasons"]), not expected)

    def test_success_with_warning(self):
        self.verify(TEST, True)

    def test_queued(self):
        self.verify(TEST, False, lambda e: e["runs"]["100"].update(status="queued", conclusion=None))

    def test_failed(self):
        self.verify(TEST, False, lambda e: e["runs"]["100"].update(conclusion="failure"))

    def test_missing_run(self):
        self.verify(TEST, False, lambda e: e["runs"].clear())

    def test_missing_logs(self):
        self.verify(TEST, False, lambda e: e["runs"]["100"].update(output_inspected=False))

    def test_stale_run(self):
        self.verify(TEST, False, lambda e: e["runs"]["100"].update(revision="old"))

    def test_wrong_metric(self):
        self.verify({**METRIC, "value": 960000}, False)

    def test_wrong_unit(self):
        self.verify({**METRIC, "unit": "runs"}, False)

    def test_missing_metric(self):
        self.verify(METRIC, False, lambda e: e["runs"]["100"]["metrics"].clear())

    def test_correct_metric(self):
        self.verify(METRIC, True)

    def test_nonfinite_metric(self):
        self.verify({**METRIC, "value": float("nan")}, False)

    def test_unmerged(self):
        self.verify({"kind": "merged", "revision": REV, "number": 4}, False)

    def test_merged(self):
        self.verify({"kind": "merged", "revision": REV, "number": 4}, True,
                    lambda e: e["pull_request"].update(merged=True))

    def test_file_absent(self):
        self.verify({"kind": "committed", "revision": REV, "path": "missing.py", "blob": "blob1"}, False)

    def test_wrong_blob(self):
        self.verify({"kind": "committed", "revision": REV, "path": "example.py", "blob": "wrong"}, False)

    def test_verified_file(self):
        self.verify({"kind": "committed", "revision": REV, "path": "example.py", "blob": "blob1"}, True)

    def test_unknown_claim(self):
        self.verify({"kind": "deployed", "revision": REV}, False)

    def test_wrong_revision(self):
        self.verify({**TEST, "revision": "different"}, False)

if __name__ == "__main__":
    unittest.main()
