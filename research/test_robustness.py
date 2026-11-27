import unittest
from robustness import SCENARIOS, POLICIES, generate, evaluate, select, update, run

class RobustnessTests(unittest.TestCase):
    def test_missing(self):
        self.assertEqual(update(.15, ((None, "A"), (None, "B"))), .15)

    def test_duplicate(self):
        one = update(.15, ((True, "A"),))
        two = ((True, "A"), (True, "A"))
        self.assertEqual(update(.15, two, True), one)
        self.assertGreater(update(.15, two), one)
        self.assertEqual(update(.15, ((None, "A"), (True, "A")), True), one)

    def test_equal_budgets_and_counts(self):
        for scenario in SCENARIOS:
            public, hidden = generate(42, scenario, 100)
            for policy in POLICIES:
                m = evaluate(public, hidden, 10, policy)
                self.assertEqual(m["attempted_slots"], 20)
                self.assertLessEqual(m["available_slots"], 20)
                self.assertEqual(sum(m[k] for k in ("fp","fn","tp","tn")), 100)

    def test_allocation_uses_only_public_inputs(self):
        public, _ = generate(42, "nominal", 100)
        self.assertEqual(select(public, 10, "voi"), select(public, 10, "voi_deduplicated"))
        with self.assertRaises(ValueError):
            select(public, 101, "voi")

    def test_reproducibility(self):
        self.assertEqual(run(seeds=(1,2), n=100, budget=10),
                         run(seeds=(1,2), n=100, budget=10))

if __name__ == "__main__":
    unittest.main()
