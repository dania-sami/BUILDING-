import unittest
from scripts.analysis import load_data, summarize, regression, solve_linear

class AnalysisTests(unittest.TestCase):
    def test_data_load(self):
        self.assertEqual(len(load_data()), 240)
    def test_summary_counts(self):
        self.assertEqual(sum(x["n"] for x in summarize(load_data())), 240)
    def test_regression(self):
        self.assertIn("lighting", regression(load_data())["coefficients"])
    def test_solver(self):
        self.assertEqual([round(x) for x in solve_linear([[2,0],[0,4]],[6,8])], [3,2])

if __name__ == "__main__":
    unittest.main()
