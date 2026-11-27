import unittest
from benchmark import posterior, value, evaluate, scenario, run

class BenchmarkTests(unittest.TestCase):
    def test_posterior(self):
        self.assertGreater(posterior(.1,True,.8,.15),.1)
        self.assertLess(posterior(.1,False,.8,.15),.1)
    def test_no_information(self):
        self.assertAlmostEqual(value(.1,5,.5,.5),0)
    def test_budget(self):
        rows=scenario(42,1000)
        for policy in ("fixed","risk","voi"):
            result=evaluate(rows,100,policy)
            self.assertEqual(result["observations_purchased"],100)
            self.assertEqual(sum(result[k] for k in ("fp","fn","tp","tn")),1000)
    def test_reproducibility(self):
        self.assertEqual(run(),run())

if __name__ == "__main__":
    unittest.main()
