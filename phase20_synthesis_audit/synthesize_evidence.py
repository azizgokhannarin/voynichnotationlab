#!/usr/bin/env python3
"""Create a hash-locked Phase-13–19 evidence matrix and stop-rule decision."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def load_sources(repo: Path, manifest: dict) -> dict[str, dict]:
    values = {}
    for relative, expected in manifest["sources"].items():
        path = repo / relative
        actual = sha256_file(path)
        if actual != expected:
            raise ValueError(f"source decision hash mismatch: {relative}: {actual}")
        values[relative] = json.loads(path.read_text(encoding="utf-8"))
    return values


def require_final_test_sealed(values: dict[str, dict]) -> None:
    for path, value in values.items():
        flags = [value.get(name) for name in
                 ("final_test_used", "voynich_final_test_used", "control_final_test_used")
                 if name in value]
        if any(flag is not False for flag in flags):
            raise ValueError(f"final-test guard failed: {path}")


def build(values: dict[str, dict]) -> tuple[dict, dict]:
    require_final_test_sealed(values)
    get = lambda suffix: next(v for k, v in values.items() if k.endswith(suffix))
    p13 = get("FOUR_LANGUAGE_CONFIRMATION.json")
    p14 = get("GENERATION_VS_LATENT_CONTENT_DECISION.json")
    p15r = get("INSTRUMENT_RECALIBRATION_DECISION.json")
    p15n = get("FULLSIZE_NEGATIVE_CONTROL_DECISION.json")
    p16 = get("RAW_TOKEN_RECURRENCE_DECISION_v1.json")
    p17 = get("STRUCTURED_DATA_CONTROL_DECISION_v1.json")
    p18 = get("RESIDUAL_CAPACITY_DECISION_v1.json")
    p19 = get("LATENT_STATE_DECISION_v1.json")

    if p13["decision"] != "STOP_DIRECT_LANGUAGE_SEARCH_AT_FROZEN_UNIT_FIXED_BOUNDARY_LEVEL":
        raise ValueError("unexpected Phase-13 closure")
    if p14["findings"]["simple_generator_metrics_inside_95pct"] >= p14["findings"]["simple_generator_metrics_compared"]:
        raise ValueError("Phase-14 simple generator was not rejected")
    if not p15n["corpus"]["power_gate"] == "PASS":
        raise ValueError("full-size negative-control power gate failed")
    if not p16["control_gate"]["pass"]:
        raise ValueError("Phase-16 control gate failed")
    if p17["hypothesis_ranking_performed"] or p18["hypothesis_ranking_performed"] or p19["hypothesis_ranking_performed"]:
        raise ValueError("upstream hypothesis ranking detected")

    rows = [
        {"id": "E13_DIRECT_MAPPING", "phase": 13,
         "evidence_class": "BOUNDED_SUBCLASS_CLOSURE",
         "result": "Direct fixed-unit, fixed-boundary, bounded-homophony language mapping is unsupported across German, Italian, French and Latin.",
         "closes": ["H_C_direct_fixed_boundary_low_homophony"],
         "does_not_close": ["H_C_strong_renderer", "H_D", "H_G"]},
        {"id": "E14_SIMPLE_GENERATOR", "phase": 14,
         "evidence_class": "BOUNDED_SUBCLASS_CLOSURE",
         "result": f"Simple line-reset first-order generator matched only {p14['findings']['simple_generator_metrics_inside_95pct']}/{p14['findings']['simple_generator_metrics_compared']} held-out metrics.",
         "closes": ["H_G_simple_first_order_line_reset"],
         "does_not_close": ["H_G_bounded_copy_modify_innovation", "H_C", "H_D"]},
        {"id": "E15_CLASS_LOCALITY", "phase": 15,
         "evidence_class": "CALIBRATED_NONDISCRIMINATOR",
         "result": p15r["consequence"],
         "closes": ["class_locality_as_H_C_vs_H_G_discriminator"],
         "does_not_close": ["H_C", "H_G"]},
        {"id": "E15_REAL_DIPLOMATIC_CONTROL", "phase": 15,
         "evidence_class": "CALIBRATED_NONDISCRIMINATOR",
         "result": "Full-size abbreviated diplomatic Latin also shows line-local predictive advantage and negligible cross-line gain; legacy class-MI is non-comparable.",
         "closes": ["line_local_predictive_advantage_as_content_type_discriminator"],
         "does_not_close": ["H_C", "H_D", "H_G"]},
        {"id": "E16_RAW_RECURRENCE", "phase": 16,
         "evidence_class": "SURFACE_OBSERVATION_ONLY",
         "result": p16["decision"],
         "closes": [], "does_not_close": ["H_C", "H_D", "H_G"]},
        {"id": "E17_STRUCTURED_DATA", "phase": 17,
         "evidence_class": "CALIBRATED_NONDISCRIMINATOR",
         "result": p17["decision"],
         "closes": ["recurrence_phenotype_as_rejection_of_broad_H_D"],
         "does_not_close": ["H_D", "H_C", "H_G"],
         "quantitative_match": p17["quantitative_effect_size_match_claimed"]},
        {"id": "E18_RESIDUAL_CAPACITY", "phase": 18,
         "evidence_class": "CALIBRATED_DISCRIMINATOR",
         "result": p18["decision"],
         "closes": [], "does_not_close": ["H_C_content_rich", "H_D", "H_G"],
         "capacity_bits_per_token": p18["voynich"]["residual_capacity_bits_per_token"]},
        {"id": "E19_BINARY_LINE_STATE", "phase": 19,
         "evidence_class": "BOUNDED_SUBCLASS_CLOSURE",
         "result": p19["decision"],
         "closes": ["robust_binary_line_state_under_32_plus_OTHER_model"],
         "does_not_close": ["all_latent_state", "H_C", "H_D", "H_G"]},
        {"id": "E20_BOUNDED_GENERATOR", "phase": 20,
         "evidence_class": "OPEN_UNTESTED_DISCRIMINATOR",
         "result": "The preregistered line-final/copy-modify/vocabulary-innovation generator ladder was deferred and has not been evaluated against the calibrated full battery.",
         "closes": [], "does_not_close": ["H_G_bounded_copy_modify_innovation"]},
        {"id": "E20_HD_ORDERING", "phase": 20,
         "evidence_class": "OPEN_UNTESTED_DISCRIMINATOR",
         "result": "No calibrated test has aligned Voynich token transitions with a numeral/record ordering or increment relation.",
         "closes": [], "does_not_close": ["H_D_record_or_enumerative"]},
    ]

    hypotheses = {
        "H_C": {"state": "OPEN_UNRANKED",
                "closed_subclasses": ["direct fixed-unit/fixed-boundary bounded-homophony mapping"],
                "surviving_reason": "Strong many-to-one renderer remains compatible and certified residual capacity is above the text-bandwidth falsification threshold."},
        "H_D": {"state": "OPEN_UNRANKED", "closed_subclasses": [],
                "surviving_reason": "A real structured dataset reproduces the qualitative allocation-without-order phenotype, but quantitative and medieval record-template matches are absent."},
        "H_G": {"state": "OPEN_UNRANKED",
                "closed_subclasses": ["simple first-order line-reset generator", "robust binary line-state extension under the frozen model"],
                "surviving_reason": "The pre-specified bounded copy/modify, line-final and innovation generator has not been run."},
        "H_T": {"state": "OPEN_CONFOUND", "closed_subclasses": [],
                "surviving_reason": "Transcription, palaeography and production effects remain possible causes of layout/state structure."},
    }

    matrix = {"schema": "PHASE20_CROSS_PHASE_EVIDENCE_MATRIX_v1", "date": "2026-08-26",
              "source_phases": list(range(13, 20)), "rows": rows,
              "hypotheses": hypotheses, "hypothesis_ranking_performed": False,
              "voynich_final_test_used": False}
    matrix["matrix_sha256"] = canonical_hash(matrix)

    stop_components = {
        "pipeline_controls_certified": True,
        "bounded_copy_modify_generator_matches_full_heldout_battery": False,
        "residual_capacity_below_text_bandwidth": bool(p18["content_rich_H_C_rejected"]),
        "quantitative_match_to_attested_nonlinguistic_record_genre": bool(
            p17["quantitative_effect_size_match_claimed"]),
    }
    stop_satisfied = all(stop_components.values())
    bounded_generator_authorized = bool(
        p14["findings"]["simple_generator_metrics_inside_95pct"] <
        p14["findings"]["simple_generator_metrics_compared"] and
        not p19["larger_state_space_authorized"])
    final_test_authorized = False
    decision_code = ("STOP_INTERNAL_EVIDENCE" if stop_satisfied else
                     ("OPEN_FINAL_TEST" if final_test_authorized else
                      "CONTINUE_BOUNDED_ONLY" if bounded_generator_authorized else
                      "PAUSE_NO_AUTHORIZED_TEST"))
    decision = {
        "schema": "PHASE20_IDENTIFIABILITY_STOP_DECISION_v1", "date": "2026-08-26",
        "matrix_sha256": matrix["matrix_sha256"],
        "stop_rule_components": stop_components,
        "stop_rule_satisfied": stop_satisfied,
        "internal_identifiability_ceiling_reached": False,
        "decision_code": decision_code,
        "bounded_generator_benchmark_authorized": bounded_generator_authorized,
        "authorized_modules": (["line_final_realization", "copy_modify_adjacency",
                                "productive_vocabulary_innovation"]
                               if bounded_generator_authorized else []),
        "latent_state_module_authorized": False,
        "unrestricted_model_search_authorized": False,
        "final_test_opening_authorized": final_test_authorized,
        "final_test_blocker": "No newly frozen model currently makes a Validation-unused directional confirmatory prediction.",
        "hypothesis_state": "H_C, H_D and H_G remain open and unranked; H_T remains an open confound.",
        "hypothesis_ranking_performed": False,
        "voynich_final_test_used": False,
        "next": "Phase 21: preregister the bounded line-final/copy-modify/vocabulary-innovation generator ladder with parameter-matched controls and TRAIN/VALIDATION only.",
    }
    decision["decision_sha256"] = canonical_hash(decision)
    return matrix, decision


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--matrix-out", required=True)
    parser.add_argument("--decision-out", required=True)
    args = parser.parse_args()
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    values = load_sources(Path(args.repo), manifest)
    matrix, decision = build(values)
    write_json(Path(args.matrix_out), matrix)
    write_json(Path(args.decision_out), decision)
    print(json.dumps({"matrix_sha256": matrix["matrix_sha256"],
                      "decision_sha256": decision["decision_sha256"],
                      "decision_code": decision["decision_code"],
                      "final_test_opening_authorized":
                          decision["final_test_opening_authorized"]}, indent=2))


if __name__ == "__main__":
    main()

