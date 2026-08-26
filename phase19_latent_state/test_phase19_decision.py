#!/usr/bin/env python3
import copy
import unittest

import evaluate_latent_state as evaluator


def fixtures(robust: bool = False):
    calibration = {
        "schema": "PHASE19_LATENT_STATE_CALIBRATION_v1",
        "calibration_passed": True,
        "final_test_used": False,
        "corpus_sha256": "c",
        "zero_state_null": {"median": -0.04, "q99_higher": -0.02},
        "injected_state_positive": {
            "heldout_gain_bits_per_token": 0.5,
            "prequential_mdl": {"gain_bits_per_token": 0.4},
            "viterbi_accuracy_label_swap_invariant": 0.95,
        },
    }
    calibration["calibration_sha256"] = evaluator.canonical_hash(calibration)
    conditions = {"heldout_gain_exceeds_null_q99": True,
                  "bootstrap_95_lower_bound_positive": robust,
                  "prequential_mdl_gain_positive": robust}
    result = {
        "schema": "PHASE19_LATENT_STATE_RESULT_v1",
        "final_test_used": False,
        "corpus_sha256": "c",
        "calibration_sha256": calibration["calibration_sha256"],
        "primary": {"heldout_gain_bits_per_token": 0.01,
                    "page_bootstrap_95_ci": [-0.01, 0.03]},
        "secondary_prequential_mdl": {"gain_bits_per_token": -0.02},
        "fitted_k2_descriptor": {"transition": [[0.9, 0.1], [0.1, 0.9]]},
        "robust_signal_conditions": conditions,
        "robust_binary_line_state_detected": robust,
    }
    result["result_sha256"] = evaluator.canonical_hash(result)
    return calibration, result


class Phase19DecisionTests(unittest.TestCase):
    def test_negative_rule_does_not_rank_or_expand(self):
        decision = evaluator.evaluate(*fixtures(False))
        self.assertFalse(decision["robust_binary_line_state_detected"])
        self.assertFalse(decision["hypothesis_ranking_performed"])
        self.assertFalse(decision["larger_state_space_authorized"])

    def test_all_three_conditions_are_required(self):
        decision = evaluator.evaluate(*fixtures(True))
        self.assertTrue(decision["robust_binary_line_state_detected"])

    def test_failed_calibration_blocks_decision(self):
        calibration, result = fixtures(False)
        calibration["calibration_passed"] = False
        calibration["calibration_sha256"] = evaluator.canonical_hash(
            {k: v for k, v in calibration.items() if k != "calibration_sha256"})
        result["calibration_sha256"] = calibration["calibration_sha256"]
        result["result_sha256"] = evaluator.canonical_hash(
            {k: v for k, v in result.items() if k != "result_sha256"})
        with self.assertRaises(ValueError):
            evaluator.evaluate(calibration, result)

    def test_final_test_use_blocks_decision(self):
        calibration, result = fixtures(False)
        result["final_test_used"] = True
        result["result_sha256"] = evaluator.canonical_hash(
            {k: v for k, v in result.items() if k != "result_sha256"})
        with self.assertRaises(ValueError):
            evaluator.evaluate(calibration, result)


if __name__ == "__main__":
    unittest.main()

