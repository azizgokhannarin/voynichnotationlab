#!/usr/bin/env python3
"""Verify Phase-19 outputs and apply the frozen three-condition decision rule."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def verify_embedded(value: dict, field: str) -> None:
    body = dict(value)
    expected = body.pop(field, None)
    if expected != canonical_hash(body):
        raise ValueError(f"invalid embedded {field}")


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def evaluate(calibration: dict, result: dict) -> dict:
    if calibration.get("schema") != "PHASE19_LATENT_STATE_CALIBRATION_v1":
        raise ValueError("unexpected calibration schema")
    if result.get("schema") != "PHASE19_LATENT_STATE_RESULT_v1":
        raise ValueError("unexpected result schema")
    verify_embedded(calibration, "calibration_sha256")
    verify_embedded(result, "result_sha256")
    if not calibration.get("calibration_passed"):
        raise ValueError("uncertified calibration")
    if calibration.get("final_test_used") or result.get("final_test_used"):
        raise ValueError("sealed final-test partition was used")
    if result.get("calibration_sha256") != calibration.get("calibration_sha256"):
        raise ValueError("result/calibration mismatch")
    if result.get("corpus_sha256") != calibration.get("corpus_sha256"):
        raise ValueError("result/corpus mismatch")

    conditions = result["robust_signal_conditions"]
    recomputed = bool(conditions["heldout_gain_exceeds_null_q99"] and
                      conditions["bootstrap_95_lower_bound_positive"] and
                      conditions["prequential_mdl_gain_positive"])
    if recomputed != result.get("robust_binary_line_state_detected"):
        raise ValueError("stored robust-state decision mismatch")

    primary = result["primary"]
    prequential = result["secondary_prequential_mdl"]
    output = {
        "schema": "PHASE19_LATENT_STATE_DECISION_v1",
        "date": "2026-08-26",
        "calibration": {
            "passed": True,
            "calibration_sha256": calibration["calibration_sha256"],
            "zero_state_null_median_bits_per_token": calibration["zero_state_null"]["median"],
            "zero_state_null_q99_bits_per_token": calibration["zero_state_null"]["q99_higher"],
            "injected_state_gain_bits_per_token":
                calibration["injected_state_positive"]["heldout_gain_bits_per_token"],
            "injected_state_prequential_gain_bits_per_token":
                calibration["injected_state_positive"]["prequential_mdl"]["gain_bits_per_token"],
            "injected_state_viterbi_accuracy":
                calibration["injected_state_positive"]["viterbi_accuracy_label_swap_invariant"],
        },
        "voynich": {
            "result_sha256": result["result_sha256"],
            "heldout_gain_bits_per_token": primary["heldout_gain_bits_per_token"],
            "page_bootstrap_95_ci": primary["page_bootstrap_95_ci"],
            "prequential_mdl_gain_bits_per_token": prequential["gain_bits_per_token"],
            "transition_matrix": result["fitted_k2_descriptor"]["transition"],
            "robust_signal_conditions": conditions,
        },
        "robust_binary_line_state_detected": recomputed,
        "decision": (
            "A transferable binary line-state signal is detected against the matched zero-state null."
            if recomputed else
            "No robust transferable binary line-state signal is detected under the frozen model and three-condition rule."
        ),
        "scope": (
            "A negative result applies only to this binary line-state model over the frozen 32+OTHER raw-token representation; "
            "a positive result would reject only the matched K=1 mechanism."
        ),
        "hypothesis_state": "H_C, H_D and H_G remain open and unranked.",
        "hypothesis_ranking_performed": False,
        "larger_state_space_authorized": False,
        "voynich_final_test_used": False,
        "next": (
            "Cross-phase synthesis and identifiability/stop-rule audit before authorizing any new model or opening final-test pages."
        ),
    }
    output["decision_sha256"] = canonical_hash(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--calibration", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    calibration = json.loads(Path(args.calibration).read_text(encoding="utf-8"))
    result = json.loads(Path(args.result).read_text(encoding="utf-8"))
    decision = evaluate(calibration, result)
    write_json(Path(args.out), decision)
    print(json.dumps({"out": args.out, "decision_sha256": decision["decision_sha256"],
                      "robust_binary_line_state_detected":
                          decision["robust_binary_line_state_detected"]}, indent=2))


if __name__ == "__main__":
    main()

