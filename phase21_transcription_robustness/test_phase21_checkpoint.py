#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from validate_phase21_checkpoint import load_json, validate


HERE = Path(__file__).resolve().parent
REPO = HERE.parent


class Phase21CheckpointTests(unittest.TestCase):
    def test_repository_checkpoint_passes(self) -> None:
        validate(REPO)

    def test_all_authorization_guards_are_false(self) -> None:
        value = load_json(HERE / "PHASE21_DECISION_SUPERSESSION_v1.json")
        names = (
            "final_test_opening_authorized",
            "hypothesis_ranking_performed",
            "new_voynich_model_fitting_authorized",
            "unrestricted_model_search_authorized",
            "voynich_challenger_validation_scoring_authorized",
            "voynich_final_test_used",
        )
        self.assertTrue(all(value[name] is False for name in names))

    def test_evidence_status_corrections_are_locked(self) -> None:
        value = load_json(HERE / "PHASE21_DECISION_SUPERSESSION_v1.json")
        self.assertEqual(value["legacy_class_mi_status"],
                         "RETIRED_HISTORICAL_UNREPRODUCIBLE")
        self.assertEqual(value["phase18_status"],
                         "WEAK_ONE_SIDED_MODEL_SPECIFIC_BOUND")
        self.assertEqual(value["phase21_generator_ladder_status"],
                         "CANCELLED_AS_EVIDENTIAL_LADDER")

    def test_only_it2a_is_independent_challenger(self) -> None:
        sources = load_json(HERE / "SOURCE_PROVENANCE_CANDIDATES_v1.json")["sources"]
        independent = sorted(name for name, value in sources.items()
                             if value.get("independent_replication_role") is True)
        self.assertEqual(independent, ["IT2a"])

    def test_payload_gate_is_closed(self) -> None:
        value = load_json(HERE / "SOURCE_PROVENANCE_CANDIDATES_v1.json")
        self.assertFalse(value["acquisition_gate"]["all_required_payload_hashes_frozen"])
        self.assertFalse(value["acquisition_gate"]["challenger_validation_scoring_allowed"])

    def test_no_phase21_validation_result_exists(self) -> None:
        self.assertEqual(list(HERE.glob("*VALIDATION_RESULT*.json")), [])


if __name__ == "__main__":
    unittest.main()
