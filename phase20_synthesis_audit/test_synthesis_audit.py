#!/usr/bin/env python3
import copy
import unittest

import synthesize_evidence as synthesis


def fixtures():
    values = {
        "p13/FOUR_LANGUAGE_CONFIRMATION.json": {
            "decision": "STOP_DIRECT_LANGUAGE_SEARCH_AT_FROZEN_UNIT_FIXED_BOUNDARY_LEVEL",
            "final_test_used": False},
        "p14/GENERATION_VS_LATENT_CONTENT_DECISION.json": {
            "final_test_used": False,
            "findings": {"simple_generator_metrics_inside_95pct": 4,
                         "simple_generator_metrics_compared": 18}},
        "p15/INSTRUMENT_RECALIBRATION_DECISION.json": {
            "final_test_used": False,
            "consequence": "Class-space locality cannot discriminate."},
        "p15/FULLSIZE_NEGATIVE_CONTROL_DECISION.json": {
            "voynich_final_test_used": False, "control_final_test_used": False,
            "corpus": {"power_gate": "PASS"}},
        "p16/RAW_TOKEN_RECURRENCE_DECISION_v1.json": {
            "decision": "allocation signal", "control_gate": {"pass": True}},
        "p17/STRUCTURED_DATA_CONTROL_DECISION_v1.json": {
            "decision": "H_D not rejected", "hypothesis_ranking_performed": False,
            "quantitative_effect_size_match_claimed": False,
            "voynich_final_test_used": False},
        "p18/RESIDUAL_CAPACITY_DECISION_v1.json": {
            "decision": "H_C not rejected", "content_rich_H_C_rejected": False,
            "hypothesis_ranking_performed": False, "voynich_final_test_used": False,
            "voynich": {"residual_capacity_bits_per_token": 12.0}},
        "p19/LATENT_STATE_DECISION_v1.json": {
            "decision": "no robust state", "larger_state_space_authorized": False,
            "hypothesis_ranking_performed": False, "voynich_final_test_used": False},
    }
    return values


class SynthesisAuditTests(unittest.TestCase):
    def test_current_chain_authorizes_only_bounded_continuation(self):
        matrix, decision = synthesis.build(fixtures())
        self.assertEqual(decision["decision_code"], "CONTINUE_BOUNDED_ONLY")
        self.assertFalse(decision["stop_rule_satisfied"])
        self.assertTrue(decision["bounded_generator_benchmark_authorized"])
        self.assertFalse(decision["final_test_opening_authorized"])
        self.assertFalse(matrix["hypothesis_ranking_performed"])

    def test_stop_requires_all_four_components(self):
        _, decision = synthesis.build(fixtures())
        self.assertEqual(sum(decision["stop_rule_components"].values()), 1)
        self.assertFalse(decision["internal_identifiability_ceiling_reached"])

    def test_final_test_guard_is_enforced(self):
        values = fixtures()
        values["p19/LATENT_STATE_DECISION_v1.json"]["voynich_final_test_used"] = True
        with self.assertRaises(ValueError):
            synthesis.build(values)

    def test_upstream_ranking_is_rejected(self):
        values = fixtures()
        values["p17/STRUCTURED_DATA_CONTROL_DECISION_v1.json"]["hypothesis_ranking_performed"] = True
        with self.assertRaises(ValueError):
            synthesis.build(values)

    def test_simple_generator_success_removes_bounded_authorization(self):
        values = fixtures()
        values["p14/GENERATION_VS_LATENT_CONTENT_DECISION.json"]["findings"]["simple_generator_metrics_inside_95pct"] = 18
        with self.assertRaises(ValueError):
            synthesis.build(values)


if __name__ == "__main__":
    unittest.main()

