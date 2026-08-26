#!/usr/bin/env python3
"""Validate the Phase-21 decision-only checkpoint without scoring Voynich."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(repo: Path) -> None:
    phase = repo / "phase21_transcription_robustness"
    decision = load_json(phase / "PHASE21_DECISION_SUPERSESSION_v1.json")
    claims = load_json(phase / "CLAIM_STATUS_REVISION_v1.json")
    sources = load_json(phase / "SOURCE_PROVENANCE_CANDIDATES_v1.json")
    freeze = load_json(phase / "PHASE21_PRERESULT_FREEZE_v1.json")

    superseded = repo / decision["supersedes"]["path"]
    if sha256_file(superseded) != decision["supersedes"]["raw_sha256"]:
        raise ValueError("superseded Phase-20 decision hash mismatch")
    ledger = repo / claims["supersedes_claim_ledger"]["path"]
    if sha256_file(ledger) != claims["supersedes_claim_ledger"]["sha256"]:
        raise ValueError("superseded claim-ledger hash mismatch")

    required_false = [
        "final_test_opening_authorized",
        "hypothesis_ranking_performed",
        "new_voynich_model_fitting_authorized",
        "unrestricted_model_search_authorized",
        "voynich_challenger_validation_scoring_authorized",
        "voynich_final_test_used",
    ]
    if any(decision[name] is not False for name in required_false):
        raise ValueError("authorization guard failed")
    if decision["phase21_generator_ladder_status"] != "CANCELLED_AS_EVIDENTIAL_LADDER":
        raise ValueError("generator ladder is not cancelled")
    if decision["legacy_class_mi_status"] != "RETIRED_HISTORICAL_UNREPRODUCIBLE":
        raise ValueError("legacy class-MI is not retired")
    if decision["phase18_status"] != "WEAK_ONE_SIDED_MODEL_SPECIFIC_BOUND":
        raise ValueError("Phase-18 status was not downgraded")

    source_values = sources["sources"]
    if source_values["IT2a"]["independent_replication_role"] is not True:
        raise ValueError("IT2a must be the independent challenger")
    for name in ("RF1b_EVA", "ZL3b", "GC2a"):
        if source_values[name]["independent_replication_role"] is not False:
            raise ValueError(f"{name} must not count as independent")
    if sources["acquisition_gate"]["challenger_validation_scoring_allowed"] is not False:
        raise ValueError("source gate improperly authorizes scoring")

    for relative, expected in freeze["files"].items():
        if sha256_file(phase / relative) != expected:
            raise ValueError(f"Phase-21 preregistration hash mismatch: {relative}")
    if any(freeze["guards"].values()):
        raise ValueError("preresult freeze guard failed")

    forbidden_results = list(phase.glob("*VALIDATION_RESULT*.json"))
    if forbidden_results:
        raise ValueError(f"premature Phase-21 result present: {forbidden_results[0].name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    validate(Path(args.repo))
    print("PHASE21 CHECKPOINT: PASS")
    print("challenger validation scoring: DENIED")
    print("final-test access: DENIED")


if __name__ == "__main__":
    main()
