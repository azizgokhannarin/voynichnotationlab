#!/usr/bin/env python3
"""Frozen Phase-19 binary line-state HMM and matched calibration."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np


SEED = 20260826
SCHEMA_CALIBRATION = "PHASE19_LATENT_STATE_CALIBRATION_v1"
SCHEMA_RESULT = "PHASE19_LATENT_STATE_RESULT_v1"
EXPECTED_CORPUS = "5fdf577932f21b6da59b7ae12f5bb5451d9bb5b574d81c1affd8b646364b9997"
TOP_TYPES = 32
POSITION_BUCKETS = 5
LINE_LENGTH_BUCKETS = 4
CONTEXTS = POSITION_BUCKETS * LINE_LENGTH_BUCKETS
VOCABULARY = TOP_TYPES + 1
OTHER = TOP_TYPES
BETA = 0.5
EMISSION_PRIOR = 8.0
TRANSITION_PRIOR = 1.0
EM_STARTS = 2
EM_ITERATIONS = 30
EM_TOLERANCE = 1e-7
NULL_REPLICATES = 100
BOOTSTRAPS = 2000
POSITIVE_PERSISTENCE = 0.90
POSITIVE_ODDS_MULTIPLIER = 6.0


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def stable_u64(text: str) -> int:
    return int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")


def verify_corpus(corpus: dict) -> None:
    body = dict(corpus)
    expected = body.pop("corpus_sha256", None)
    if expected != canonical_hash(body):
        raise ValueError("canonical corpus hash mismatch")
    if expected != EXPECTED_CORPUS:
        raise ValueError("unexpected frozen Voynich corpus")


def position_bucket(index: int, length: int) -> int:
    return min(POSITION_BUCKETS - 1,
               int(POSITION_BUCKETS * index / max(1, length)))


def length_bucket(length: int) -> int:
    return 0 if length <= 5 else (1 if length <= 10 else
                                  (2 if length <= 15 else 3))


def visible_context(index: int, length: int) -> int:
    return length_bucket(length) * POSITION_BUCKETS + position_bucket(index, length)


def frozen_inventory(corpus: dict) -> list[str]:
    counts = Counter(t for r in corpus["records"] if r["split"] == "train"
                     for t in r["tokens"])
    return [token for token, _ in sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:TOP_TYPES]]


def encode_pages(corpus: dict, split: str, inventory: list[str]) -> list[dict]:
    index = {token: i for i, token in enumerate(inventory)}
    grouped: dict[tuple[str, str], list[dict]] = {}
    for record in corpus["records"]:
        if record["split"] != split:
            continue
        grouped.setdefault((record["document"], record["page"]), []).append(record)
    pages = []
    for key in sorted(grouped):
        lines = []
        for record in sorted(grouped[key], key=lambda r: (r["order"], r["line_id"])):
            n = len(record["tokens"])
            lines.append({
                "line_id": record["line_id"],
                "contexts": np.asarray([visible_context(i, n) for i in range(n)], dtype=np.int16),
                "symbols": np.asarray([index.get(token, OTHER) for token in record["tokens"]],
                                      dtype=np.int16),
            })
        pages.append({"page": key[1], "lines": lines})
    return pages


def token_count(pages: list[dict]) -> int:
    return sum(len(line["symbols"]) for page in pages for line in page["lines"])


def line_count(pages: list[dict]) -> int:
    return sum(len(page["lines"]) for page in pages)


def line_count_matrices(pages: list[dict]) -> tuple[np.ndarray, list[tuple[int, int]]]:
    lines = [line for page in pages for line in page["lines"]]
    counts = np.zeros((len(lines), CONTEXTS, VOCABULARY), dtype=float)
    cursor = 0
    spans = []
    line_i = 0
    for page in pages:
        start = line_i
        for line in page["lines"]:
            np.add.at(counts[line_i], (line["contexts"], line["symbols"]), 1.0)
            line_i += 1
        spans.append((start, line_i))
    return counts, spans


def logsumexp(values: np.ndarray, axis=None) -> np.ndarray:
    maximum = np.max(values, axis=axis, keepdims=True)
    result = maximum + np.log(np.sum(np.exp(values - maximum), axis=axis, keepdims=True))
    if axis is None:
        return np.asarray(result.squeeze())
    return np.squeeze(result, axis=axis)


def fit_k1(counts: np.ndarray) -> np.ndarray:
    totals = counts.sum(axis=0)
    return (totals + BETA) / (totals.sum(axis=1, keepdims=True) + BETA * VOCABULARY)


def line_log_emissions(counts: np.ndarray, emissions: np.ndarray) -> np.ndarray:
    # emissions: states x contexts x vocabulary
    return np.einsum("lcv,zcv->lz", counts, np.log(np.maximum(emissions, 1e-300)))


def forward_page(log_emission: np.ndarray, initial: np.ndarray,
                 transition: np.ndarray) -> tuple[float, np.ndarray]:
    log_initial = np.log(np.maximum(initial, 1e-300))
    log_transition = np.log(np.maximum(transition, 1e-300))
    alpha = np.empty_like(log_emission)
    alpha[0] = log_initial + log_emission[0]
    for t in range(1, len(alpha)):
        alpha[t] = log_emission[t] + logsumexp(alpha[t - 1][:, None] + log_transition, axis=0)
    return float(logsumexp(alpha[-1])), alpha


def forward_backward(log_emission: np.ndarray, initial: np.ndarray,
                     transition: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    ll, alpha = forward_page(log_emission, initial, transition)
    log_transition = np.log(np.maximum(transition, 1e-300))
    beta = np.zeros_like(log_emission)
    for t in range(len(beta) - 2, -1, -1):
        beta[t] = logsumexp(log_transition + log_emission[t + 1][None, :] +
                            beta[t + 1][None, :], axis=1)
    gamma = np.exp(alpha + beta - ll)
    xi = np.zeros((2, 2), dtype=float)
    for t in range(len(alpha) - 1):
        value = (alpha[t][:, None] + log_transition + log_emission[t + 1][None, :] +
                 beta[t + 1][None, :] - ll)
        xi += np.exp(value)
    return ll, gamma, xi


def initialize_emissions(base: np.ndarray, start: int) -> np.ndarray:
    groups = np.asarray([stable_u64(f"phase19-init:{start}:{i}") % 2
                         for i in range(VOCABULARY)], dtype=int)
    result = np.empty((2, CONTEXTS, VOCABULARY), dtype=float)
    for state in range(2):
        weights = np.where(groups == state, 1.4, 1 / 1.4)
        result[state] = base * weights[None, :]
        result[state] /= result[state].sum(axis=1, keepdims=True)
    return result


def fit_k2(counts: np.ndarray, spans: list[tuple[int, int]]) -> dict:
    base = fit_k1(counts)
    best = None
    tokens = max(1.0, counts.sum())
    for start in range(EM_STARTS):
        emissions = initialize_emissions(base, start)
        initial = np.asarray([0.5, 0.5], dtype=float)
        transition = np.asarray([[0.75, 0.25], [0.25, 0.75]], dtype=float)
        previous = -float("inf")
        iterations = 0
        for iteration in range(EM_ITERATIONS):
            log_em = line_log_emissions(counts, emissions)
            gamma_all = np.zeros((len(counts), 2), dtype=float)
            xi_total = np.zeros((2, 2), dtype=float)
            initial_total = np.zeros(2, dtype=float)
            ll_total = 0.0
            for left, right in spans:
                ll, gamma, xi = forward_backward(log_em[left:right], initial, transition)
                ll_total += ll
                gamma_all[left:right] = gamma
                initial_total += gamma[0]
                xi_total += xi
            weighted = np.einsum("lz,lcv->zcv", gamma_all, counts)
            emissions = weighted + EMISSION_PRIOR * base[None, :, :]
            emissions /= emissions.sum(axis=2, keepdims=True)
            initial = initial_total + TRANSITION_PRIOR
            initial /= initial.sum()
            transition = xi_total + TRANSITION_PRIOR
            transition /= transition.sum(axis=1, keepdims=True)
            iterations = iteration + 1
            if iteration and abs(ll_total - previous) / tokens <= EM_TOLERANCE:
                break
            previous = ll_total
        final_ll = score_k2(counts, spans, initial, transition, emissions)[0]
        candidate = {"initial": initial, "transition": transition, "emissions": emissions,
                     "train_log_likelihood_nats": final_ll, "iterations": iterations,
                     "start": start}
        if best is None or final_ll > best["train_log_likelihood_nats"]:
            best = candidate
    assert best is not None
    return best


def score_k1(counts: np.ndarray, probabilities: np.ndarray) -> tuple[float, np.ndarray]:
    per_line = np.einsum("lcv,cv->l", counts,
                         np.log(np.maximum(probabilities, 1e-300)))
    return float(per_line.sum()), per_line


def score_k2(counts: np.ndarray, spans: list[tuple[int, int]], initial: np.ndarray,
             transition: np.ndarray, emissions: np.ndarray) -> tuple[float, np.ndarray]:
    log_em = line_log_emissions(counts, emissions)
    per_page = np.empty(len(spans), dtype=float)
    for i, (left, right) in enumerate(spans):
        per_page[i] = forward_page(log_em[left:right], initial, transition)[0]
    return float(per_page.sum()), per_page


def fit_and_score(train_pages: list[dict], validation_pages: list[dict]) -> dict:
    train_counts, train_spans = line_count_matrices(train_pages)
    validation_counts, validation_spans = line_count_matrices(validation_pages)
    k1 = fit_k1(train_counts)
    k2 = fit_k2(train_counts, train_spans)
    ll1, line_ll1 = score_k1(validation_counts, k1)
    ll2, page_ll2 = score_k2(validation_counts, validation_spans, k2["initial"],
                              k2["transition"], k2["emissions"])
    page_ll1 = np.asarray([line_ll1[left:right].sum() for left, right in validation_spans])
    tokens = int(validation_counts.sum())
    gain = (ll2 - ll1) / (math.log(2) * tokens)
    return {"gain_bits_per_token": float(gain), "validation_tokens": tokens,
            "k1_log_likelihood_nats": ll1, "k2_log_likelihood_nats": ll2,
            "page_gain_bits": ((page_ll2 - page_ll1) / math.log(2)).tolist(),
            "page_tokens": [int(validation_counts[left:right].sum())
                            for left, right in validation_spans],
            "k2": k2, "k1": k1}


def simulated_pages(template: list[dict], base: np.ndarray, rng: np.random.Generator,
                    injected_state: bool) -> list[dict]:
    groups = np.asarray([stable_u64(f"phase19-positive:{i}") % 2
                         for i in range(VOCABULARY)], dtype=int)
    state_probs = np.empty((2, CONTEXTS, VOCABULARY), dtype=float)
    for state in range(2):
        weights = np.where(groups == state, POSITIVE_ODDS_MULTIPLIER,
                           1 / POSITIVE_ODDS_MULTIPLIER)
        state_probs[state] = base * weights[None, :]
        state_probs[state] /= state_probs[state].sum(axis=1, keepdims=True)
    result = []
    for page in template:
        lines = []
        state = int(rng.integers(0, 2))
        for source_line in page["lines"]:
            if injected_state and lines and rng.random() > POSITIVE_PERSISTENCE:
                state = 1 - state
            elif not injected_state:
                state = 0
            contexts = source_line["contexts"].copy()
            probabilities = state_probs[state] if injected_state else base
            symbols = np.asarray([rng.choice(VOCABULARY, p=probabilities[c])
                                  for c in contexts], dtype=np.int16)
            lines.append({"line_id": source_line["line_id"], "contexts": contexts,
                          "symbols": symbols, "true_state": state})
        result.append({"page": page["page"], "lines": lines})
    return result


def viterbi_accuracy(pages: list[dict], model: dict) -> float:
    counts, spans = line_count_matrices(pages)
    log_em = line_log_emissions(counts, model["emissions"])
    log_initial = np.log(np.maximum(model["initial"], 1e-300))
    log_transition = np.log(np.maximum(model["transition"], 1e-300))
    predictions, truth = [], []
    for page, (left, right) in zip(pages, spans):
        emission = log_em[left:right]
        delta = np.empty_like(emission)
        back = np.zeros((len(emission), 2), dtype=np.int8)
        delta[0] = log_initial + emission[0]
        for t in range(1, len(emission)):
            values = delta[t - 1][:, None] + log_transition
            back[t] = np.argmax(values, axis=0)
            delta[t] = emission[t] + np.max(values, axis=0)
        path = np.zeros(len(emission), dtype=int)
        path[-1] = int(np.argmax(delta[-1]))
        for t in range(len(path) - 2, -1, -1):
            path[t] = back[t + 1, path[t + 1]]
        predictions.extend(path.tolist())
        truth.extend(line["true_state"] for line in page["lines"])
    accuracy = np.mean(np.asarray(predictions) == np.asarray(truth))
    return float(max(accuracy, 1 - accuracy))


def ordered_blocks(pages: list[dict], blocks: int = 5) -> list[list[dict]]:
    ordered = sorted(pages, key=lambda p: (stable_u64(f"{SEED}:prequential:{p['page']}"),
                                           p["page"]))
    return [list(x) for x in np.array_split(np.asarray(ordered, dtype=object), blocks)]


def prequential_gain(pages: list[dict]) -> dict:
    blocks = ordered_blocks(pages)
    training = list(blocks[0])
    total_gain_bits = 0.0
    total_tokens = 0
    rows = []
    for block_index in range(1, len(blocks)):
        scored = fit_and_score(training, list(blocks[block_index]))
        gain_bits = scored["gain_bits_per_token"] * scored["validation_tokens"]
        total_gain_bits += gain_bits
        total_tokens += scored["validation_tokens"]
        rows.append({"block": block_index + 1, "train_pages": len(training),
                     "score_pages": len(blocks[block_index]),
                     "score_tokens": scored["validation_tokens"],
                     "gain_bits_per_token": scored["gain_bits_per_token"]})
        training.extend(blocks[block_index])
    return {"coded_tokens": total_tokens, "gain_bits": total_gain_bits,
            "gain_bits_per_token": total_gain_bits / total_tokens, "blocks": rows}


def bootstrap_gain(page_gain_bits: list[float], page_tokens: list[int]) -> list[float]:
    gains = np.asarray(page_gain_bits, dtype=float)
    tokens = np.asarray(page_tokens, dtype=float)
    rng = np.random.default_rng(SEED)
    values = np.empty(BOOTSTRAPS, dtype=float)
    for i in range(BOOTSTRAPS):
        index = rng.integers(0, len(gains), len(gains))
        values[i] = gains[index].sum() / tokens[index].sum()
    return [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))]


def calibration(corpus: dict) -> dict:
    verify_corpus(corpus)
    inventory = frozen_inventory(corpus)
    train = encode_pages(corpus, "train", inventory)
    validation = encode_pages(corpus, "validation", inventory)
    train_counts, _ = line_count_matrices(train)
    base = fit_k1(train_counts)
    null_gains = []
    for replicate in range(NULL_REPLICATES):
        synthetic_train = simulated_pages(train, base,
                                          np.random.default_rng(SEED + 1000 + 2 * replicate), False)
        synthetic_validation = simulated_pages(validation, base,
                                               np.random.default_rng(SEED + 1001 + 2 * replicate), False)
        null_gains.append(fit_and_score(synthetic_train, synthetic_validation)["gain_bits_per_token"])
        if (replicate + 1) % 10 == 0:
            print(f"zero-state null {replicate + 1}/{NULL_REPLICATES}", file=sys.stderr,
                  flush=True)

    positive_train = simulated_pages(train, base, np.random.default_rng(SEED + 90001), True)
    positive_validation = simulated_pages(validation, base,
                                          np.random.default_rng(SEED + 90002), True)
    positive = fit_and_score(positive_train, positive_validation)
    positive_prequential = prequential_gain(positive_train)
    accuracy = viterbi_accuracy(positive_validation, positive["k2"])
    null_array = np.asarray(null_gains)
    null_q99 = float(np.quantile(null_array, 0.99, method="higher"))
    p = (1 + int(np.sum(null_array >= positive["gain_bits_per_token"]))) / (NULL_REPLICATES + 1)
    conditions = {
        "one_hundred_zero_state_nulls_completed": len(null_gains) == NULL_REPLICATES,
        "zero_state_median_not_positive": float(np.median(null_array)) <= 0.0,
        "zero_state_q99_at_most_0_02_bits_per_token": null_q99 <= 0.02,
        "positive_gain_at_least_0_05_bits_per_token": positive["gain_bits_per_token"] >= 0.05,
        "positive_exceeds_all_nulls_at_p_at_most_0_01": p <= 0.01,
        "positive_prequential_gain_positive": positive_prequential["gain_bits_per_token"] > 0.0,
        "positive_viterbi_accuracy_at_least_0_80": accuracy >= 0.80,
        "final_test_unused": True,
    }
    output = {
        "schema": SCHEMA_CALIBRATION,
        "date": "2026-08-26",
        "corpus_sha256": corpus["corpus_sha256"],
        "instrument": instrument_spec(),
        "inventory": inventory,
        "train_counts": {"pages": len(train), "lines": line_count(train),
                         "tokens": token_count(train)},
        "validation_geometry_counts": {"pages": len(validation),
                                       "lines": line_count(validation),
                                       "tokens": token_count(validation)},
        "zero_state_null": {"replicates": NULL_REPLICATES,
                            "gains_bits_per_token": null_gains,
                            "median": float(np.median(null_array)),
                            "q95": float(np.quantile(null_array, 0.95)),
                            "q99_higher": null_q99,
                            "maximum": float(np.max(null_array))},
        "injected_state_positive": {
            "persistence": POSITIVE_PERSISTENCE,
            "odds_multiplier": POSITIVE_ODDS_MULTIPLIER,
            "heldout_gain_bits_per_token": positive["gain_bits_per_token"],
            "empirical_one_sided_p": p,
            "viterbi_accuracy_label_swap_invariant": accuracy,
            "prequential_mdl": positive_prequential,
        },
        "gate_conditions": conditions,
        "calibration_passed": all(conditions.values()),
        "voynich_validation_authorized": all(conditions.values()),
        "final_test_used": False,
    }
    output["calibration_sha256"] = canonical_hash(output)
    return output


def instrument_spec() -> dict:
    return {"top_exact_train_types": TOP_TYPES, "other_symbol": True,
            "visible_contexts": CONTEXTS, "line_states": 2,
            "emission_prior_to_k1": EMISSION_PRIOR,
            "transition_prior": TRANSITION_PRIOR, "em_starts": EM_STARTS,
            "em_iterations_max": EM_ITERATIONS, "em_tolerance_nats_per_token": EM_TOLERANCE,
            "null_replicates": NULL_REPLICATES, "bootstraps": BOOTSTRAPS, "seed": SEED}


def verify_calibration(value: dict, corpus: dict) -> None:
    body = dict(value)
    expected = body.pop("calibration_sha256", None)
    if expected != canonical_hash(body):
        raise ValueError("calibration hash mismatch")
    if not value.get("calibration_passed") or not value.get("voynich_validation_authorized"):
        raise ValueError("latent-state instrument is not calibrated")
    if value.get("corpus_sha256") != corpus.get("corpus_sha256"):
        raise ValueError("calibration/corpus mismatch")
    if value.get("final_test_used"):
        raise ValueError("calibration used final-test")


def analyze(corpus: dict, calibration_value: dict) -> dict:
    verify_corpus(corpus)
    verify_calibration(calibration_value, corpus)
    inventory = calibration_value["inventory"]
    train = encode_pages(corpus, "train", inventory)
    validation = encode_pages(corpus, "validation", inventory)
    scored = fit_and_score(train, validation)
    prequential = prequential_gain(train)
    interval = bootstrap_gain(scored["page_gain_bits"], scored["page_tokens"])
    null_q99 = calibration_value["zero_state_null"]["q99_higher"]
    conditions = {
        "heldout_gain_exceeds_null_q99": scored["gain_bits_per_token"] > null_q99,
        "bootstrap_95_lower_bound_positive": interval[0] > 0.0,
        "prequential_mdl_gain_positive": prequential["gain_bits_per_token"] > 0.0,
    }
    k2 = scored["k2"]
    output = {
        "schema": SCHEMA_RESULT,
        "date": "2026-08-26",
        "corpus_sha256": corpus["corpus_sha256"],
        "calibration_sha256": calibration_value["calibration_sha256"],
        "instrument": instrument_spec(),
        "inventory": inventory,
        "train_counts": {"pages": len(train), "lines": line_count(train),
                         "tokens": token_count(train)},
        "validation_counts": {"pages": len(validation), "lines": line_count(validation),
                              "tokens": token_count(validation)},
        "primary": {"heldout_gain_bits_per_token": scored["gain_bits_per_token"],
                    "page_bootstrap_95_ci": interval,
                    "zero_state_null_q99": null_q99,
                    "k1_log_likelihood_nats": scored["k1_log_likelihood_nats"],
                    "k2_log_likelihood_nats": scored["k2_log_likelihood_nats"]},
        "secondary_prequential_mdl": prequential,
        "fitted_k2_descriptor": {
            "initial": k2["initial"].tolist(),
            "transition": k2["transition"].tolist(),
            "training_iterations": k2["iterations"],
            "selected_deterministic_start": k2["start"],
            "k1_free_parameters": CONTEXTS * (VOCABULARY - 1),
            "k2_free_parameters": 2 * CONTEXTS * (VOCABULARY - 1) + 3,
        },
        "robust_signal_conditions": conditions,
        "robust_binary_line_state_detected": all(conditions.values()),
        "interpretation": (
            "Only the matched K=1 zero-state surface mechanism is rejected; latent state is not language evidence."
            if all(conditions.values()) else
            "No robust transferable binary line-state signal is detected under the frozen three-part rule."
        ),
        "hypothesis_state": "H_C, H_D and H_G remain open and unranked.",
        "hypothesis_ranking_performed": False,
        "final_test_used": False,
    }
    output["result_sha256"] = canonical_hash(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    cal = sub.add_parser("calibrate")
    cal.add_argument("--corpus", required=True)
    cal.add_argument("--out", required=True)
    run = sub.add_parser("analyze")
    run.add_argument("--corpus", required=True)
    run.add_argument("--calibration", required=True)
    run.add_argument("--out", required=True)
    args = parser.parse_args()
    corpus = json.loads(Path(args.corpus).read_text(encoding="utf-8"))
    if args.command == "calibrate":
        result = calibration(corpus)
    else:
        calibration_value = json.loads(Path(args.calibration).read_text(encoding="utf-8"))
        result = analyze(corpus, calibration_value)
    write_json(Path(args.out), result)
    print(json.dumps({"out": args.out, "schema": result["schema"],
                      "calibration_passed": result.get("calibration_passed"),
                      "robust_binary_line_state_detected":
                          result.get("robust_binary_line_state_detected"),
                      "sha256": result.get("calibration_sha256", result.get("result_sha256"))},
                     indent=2))


if __name__ == "__main__":
    main()

