import unittest

from phase23_paragraph_closure.paragraph_closure_scan import auc, balanced_accuracy, decompose


class ParagraphClosureTests(unittest.TestCase):
    def test_decompose_uses_frozen_terminal_set(self):
        self.assertEqual(decompose("qokam"), ("qoka", "m"))
        self.assertEqual(decompose("qokad"), ("qokad", "Ø"))

    def test_auc_ties(self):
        self.assertEqual(auc([1, 0], [0.5, 0.5]), 0.5)
        self.assertEqual(balanced_accuracy([1, 0], [1.0, -1.0]), 1.0)


if __name__ == "__main__":
    unittest.main()
