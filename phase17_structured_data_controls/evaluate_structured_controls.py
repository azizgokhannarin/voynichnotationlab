#!/usr/bin/env python3
"""Apply the preregistered Phase-17 phenotype rule to frozen Phase-16 results."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_NAMES = (
    "RETAIL_TALLY_ORDERED_v1",
    "RETAIL_TALLY_UNORDERED_v1",
    "MUSHROOM_RAW_ORDERED_v1",
    "MUSHROOM_RAW_PERMUTED_v1",
    "MUSHROOM_QUALIFIED_ORDERED_v1",
)


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def metric(result: dict, family: str, name: str) -> dict:
    return result["null_families"][family]["metrics"][name]


def positive_significant(value: dict) -> bool:
    ratio = value["observed_to_null_ratio"]
    return bool(value["significant_holm_0_01"] and ratio is not None and ratio > 1.0)


def phenotype(result: dict) -> dict:
    line_metrics = [metric(result, "line_shuffle", name) for name in (
        "line_identity_gap1", "line_identity_gap2_4", "line_identity_gap5_16")]
    conditions = {
        "document_page_repeat_positive_significant": positive_significant(
            metric(result, "document_shuffle", "page_repeat_mass")),
        "document_line_repeat_positive_significant": positive_significant(
            metric(result, "document_shuffle", "line_repeat_mass")),
        "page_line_repeat_positive_significant": positive_significant(
            metric(result, "page_shuffle", "line_repeat_mass")),
        "no_line_shuffle_gap_significant": not any(
            item["significant_holm_0_01"] for item in line_metrics),
    }
    return {"conditions": conditions, "full_phenotype_match": all(conditions.values())}


def compact_profile(result: dict) -> dict:
    keys = (
        ("document_shuffle", "page_repeat_mass"),
        ("document_shuffle", "line_repeat_mass"),
        ("page_shuffle", "line_repeat_mass"),
        ("line_shuffle", "line_identity_gap1"),
        ("line_shuffle", "line_identity_gap2_4"),
        ("line_shuffle", "line_identity_gap5_16"),
    )
    return {
        f"{family}:{name}": {
            "ratio": metric(result, family, name)["observed_to_null_ratio"],
            "z": metric(result, family, name)["z"],
            "holm_p": metric(result, family, name)["holm_adjusted_p"],
            "significant": metric(result, family, name)["significant_holm_0_01"],
        }
        for family, name in keys
    }


def evaluate(paths: list[Path]) -> dict:
    results = {}
    for path in paths:
        result = json.loads(path.read_text(encoding="utf-8"))
        if result["schema"] != "PHASE16_RAW_TOKEN_RECURRENCE_v1":
            raise ValueError(f"unexpected result schema: {path}")
        if result["label"] not in EXPECTED_NAMES:
            raise ValueError(f"unexpected control label: {result['label']}")
        if result["final_test_used"] or result["permutations"] != 2000:
            raise ValueError(f"power/final-test gate failed: {path}")
        if result["validation_counts"]["tokens"] != 7596:
            raise ValueError(f"token power gate failed: {path}")
        if result["label"] in results:
            raise ValueError(f"duplicate control: {result['label']}")
        results[result["label"]] = result
    if set(results) != set(EXPECTED_NAMES):
        raise ValueError(f"missing controls: {set(EXPECTED_NAMES) - set(results)}")

    controls = {}
    for name in EXPECTED_NAMES:
        controls[name] = {
            "corpus_sha256": results[name]["corpus_sha256"],
            "result_sha256": results[name]["result_sha256"],
            "validation_counts": results[name]["validation_counts"],
            "phenotype": phenotype(results[name]),
            "profile": compact_profile(results[name]),
        }
    matches = [name for name, value in controls.items()
               if value["phenotype"]["full_phenotype_match"]]
    output = {
        "schema": "PHASE17_STRUCTURED_DATA_CONTROL_DECISION_v1",
        "date": "2026-08-26",
        "instrument": "frozen Phase-16 exact-identity recurrence/burstiness",
        "permutations_per_null": 2000,
        "family_alpha": 0.01,
        "controls": controls,
        "full_phenotype_matches": matches,
        "any_full_phenotype_match": bool(matches),
        "decision": ("At least one known structured-data control reproduces the frozen "
                     "qualitative four-condition allocation-without-order phenotype; broad "
                     "H_D is not rejected by phenotype shape."
                     if matches else
                     "None of the five bounded structured-data controls reproduces the full "
                     "phenotype; only these encodings fail and broad H_D remains open."),
        "hypothesis_ranking_performed": False,
        "phenotype_match_scope": "Boolean direction/significance pattern only; quantitative effect-size matching is not claimed.",
        "quantitative_effect_size_match_claimed": False,
        "hypothesis_state": "H_C, H_D and H_G remain open and unranked.",
        "voynich_final_test_used": False,
        "next": "Residual information capacity with lossy-renderer positive calibration.",
    }
    output["decision_sha256"] = canonical_hash(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", action="append", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    decision = evaluate([Path(value) for value in args.result])
    write_json(Path(args.out), decision)
    print(json.dumps({"out": args.out, "matches": decision["full_phenotype_matches"],
                      "decision_sha256": decision["decision_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
