#!/usr/bin/env python3
import copy
import unittest

import evaluate_capacity as evaluator


def fixtures(upper: float = 2.0):
    positive = {
        "schema": "PHASE18_POSITIVE_CALIBRATION_v1",
        "positive_calibration_passed": True,
        "final_test_used": False,
        "corpus_sha256": "p",
        "result_sha256": "pr",
        "capacity_result": {"selected_family": "LAYOUT_OPEN",
                            "residual_capacity": {"bits_per_token": 3.0}},
        "known_hidden_content_probe": {
            "recoverable_information_lower_bound_bits_per_token": 2.0,
            "one_sided_permutation_p": 0.001,
        },
    }
    voynich = {
        "schema": "PHASE18_RESIDUAL_CAPACITY_v1",
        "final_test_used": False,
        "corpus_sha256": "5fdf577932f21b6da59b7ae12f5bb5451d9bb5b574d81c1affd8b646364b9997",
        "result_sha256": "vr",
        "selected_family": "UNIGRAM_OPEN",
        "validation_counts": {"lines": 10, "tokens": 100},
        "residual_capacity": {"bits_per_token": 1.5,
                              "bootstrap_95_ci_bits_per_token": [1.0, upper],
                              "escape_rate": 0.1},
    }
    return positive, voynich


class DecisionTests(unittest.TestCase):
    def test_large_upper_bound_does_not_reject_or_rank(self):
        result = evaluator.evaluate(*fixtures(2.0))
        self.assertFalse(result["content_rich_H_C_rejected"])
        self.assertFalse(result["hypothesis_ranking_performed"])

    def test_upper_bound_below_threshold_rejects(self):
        result = evaluator.evaluate(*fixtures(0.9))
        self.assertTrue(result["content_rich_H_C_rejected"])

    def test_failed_positive_blocks_decision(self):
        positive, voynich = fixtures()
        positive["positive_calibration_passed"] = False
        with self.assertRaises(ValueError):
            evaluator.evaluate(positive, voynich)

    def test_final_test_use_blocks_decision(self):
        positive, voynich = fixtures()
        voynich["final_test_used"] = True
        with self.assertRaises(ValueError):
            evaluator.evaluate(positive, voynich)


if __name__ == "__main__":
    unittest.main()

