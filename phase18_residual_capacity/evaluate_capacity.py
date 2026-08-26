#!/usr/bin/env python3
"""Apply the frozen Phase-18 calibration and Voynich decision rules."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


THRESHOLD = 1.0


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def evaluate(positive: dict, voynich: dict) -> dict:
    if positive.get("schema") != "PHASE18_POSITIVE_CALIBRATION_v1":
        raise ValueError("unexpected positive schema")
    if voynich.get("schema") != "PHASE18_RESIDUAL_CAPACITY_v1":
        raise ValueError("unexpected Voynich schema")
    if not positive.get("positive_calibration_passed"):
        raise ValueError("positive calibration did not pass; Voynich is not interpretable")
    if positive.get("final_test_used") or voynich.get("final_test_used"):
        raise ValueError("sealed final-test partition was used")
    if voynich.get("corpus_sha256") != "5fdf577932f21b6da59b7ae12f5bb5451d9bb5b574d81c1affd8b646364b9997":
        raise ValueError("unexpected Voynich canonical corpus")

    residual = voynich["residual_capacity"]
    upper = residual["bootstrap_95_ci_bits_per_token"][1]
    hc_rejected = upper < THRESHOLD
    output = {
        "schema": "PHASE18_RESIDUAL_CAPACITY_DECISION_v1",
        "date": "2026-08-26",
        "positive_calibration": {
            "passed": True,
            "corpus_sha256": positive["corpus_sha256"],
            "result_sha256": positive["result_sha256"],
            "selected_surface_family": positive["capacity_result"]["selected_family"],
            "residual_capacity_bits_per_token":
                positive["capacity_result"]["residual_capacity"]["bits_per_token"],
            "recoverable_hidden_onset_bits_per_token":
                positive["known_hidden_content_probe"]["recoverable_information_lower_bound_bits_per_token"],
            "permutation_p": positive["known_hidden_content_probe"]["one_sided_permutation_p"],
        },
        "voynich": {
            "corpus_sha256": voynich["corpus_sha256"],
            "result_sha256": voynich["result_sha256"],
            "selected_surface_family": voynich["selected_family"],
            "validation_lines": voynich["validation_counts"]["lines"],
            "validation_tokens": voynich["validation_counts"]["tokens"],
            "residual_capacity_bits_per_token": residual["bits_per_token"],
            "bootstrap_95_ci_bits_per_token": residual["bootstrap_95_ci_bits_per_token"],
            "escape_rate": residual["escape_rate"],
        },
        "text_bandwidth_falsification_threshold_bits_per_token": THRESHOLD,
        "content_rich_H_C_rejected": hc_rejected,
        "decision": (
            "The certified upper bound is below the preregistered text-bandwidth threshold; "
            "content-rich H_C is rejected at the frozen representation level."
            if hc_rejected else
            "The certified upper bound is not below the preregistered text-bandwidth threshold; "
            "Phase 18 does not reject content-rich H_C."
        ),
        "large_capacity_interpretation": (
            "A large residual upper bound is compatible with content, procedural innovation, "
            "noise and surface-model misspecification; it is not evidence for any one class."
        ),
        "hypothesis_state": "H_C, H_D and H_G remain open and unranked.",
        "hypothesis_ranking_performed": False,
        "voynich_final_test_used": False,
        "next": (
            "Preregister a small latent-state test calibrated against parameter-matched "
            "zero-state procedural null generators, with prequential/MDL reporting."
        ),
    }
    output["decision_sha256"] = canonical_hash(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--positive", required=True)
    parser.add_argument("--voynich", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    positive = json.loads(Path(args.positive).read_text(encoding="utf-8"))
    voynich = json.loads(Path(args.voynich).read_text(encoding="utf-8"))
    result = evaluate(positive, voynich)
    write_json(Path(args.out), result)
    print(json.dumps({"out": args.out, "decision_sha256": result["decision_sha256"],
                      "content_rich_H_C_rejected": result["content_rich_H_C_rejected"]}, indent=2))


if __name__ == "__main__":
    main()

