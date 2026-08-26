#!/usr/bin/env python3
"""Preregistered Phase-18 open-vocabulary residual-capacity estimator."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

import numpy as np


SEED = 20260826
SCHEMA = "PHASE18_RESIDUAL_CAPACITY_v1"
POSITIVE_SCHEMA = "PHASE18_POSITIVE_CALIBRATION_v1"
FAMILIES = ("UNIGRAM_OPEN", "LAYOUT_OPEN", "PREV_SHAPE_LAYOUT_OPEN",
            "PREV_ID_LAYOUT_OPEN")
ALPHA = 8.0
BETA = 0.5
MIN_DICTIONARY_COUNT = 2
BOOTSTRAPS = 2000
PERMUTATIONS = 1000
TEXT_BANDWIDTH_THRESHOLD = 1.0
ESC = "<ESC>"
END_BYTE = 256
BOS_BYTE = 257


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


def split_records(corpus: dict, split: str) -> list[dict]:
    return [r for r in corpus["records"] if r["split"] == split]


def internal_train_split(records: list[dict]) -> tuple[list[dict], list[dict]]:
    pages = sorted({(r["document"], r["page"]) for r in records},
                   key=lambda x: (stable_u64(f"{SEED}:capacity:{x[0]}:{x[1]}"), x))
    if len(pages) < 5:
        lines = sorted(records, key=lambda r: stable_u64(f"{SEED}:{r['line_id']}"))
        cut = max(1, min(len(lines) - 1, round(0.8 * len(lines))))
        return lines[:cut], lines[cut:]
    n_dev = max(1, round(0.2 * len(pages)))
    dev_pages = set(pages[-n_dev:])
    fit = [r for r in records if (r["document"], r["page"]) not in dev_pages]
    dev = [r for r in records if (r["document"], r["page"]) in dev_pages]
    if not fit or not dev:
        raise ValueError("empty internal TRAIN split")
    return fit, dev


def position_bucket(index: int, length: int) -> str:
    return str(min(4, int(5 * index / max(1, length))))


def line_length_bucket(length: int) -> str:
    return "S" if length <= 5 else ("M" if length <= 10 else
                                     ("L" if length <= 15 else "XL"))


def token_length_bucket(token: str) -> str:
    n = len(token)
    return "1-2" if n <= 2 else ("3-4" if n <= 4 else
                                  ("5-6" if n <= 6 else "7+"))


def context_levels(family: str, tokens: list[str], index: int) -> list[tuple]:
    layout = ("LAYOUT", position_bucket(index, len(tokens)),
              line_length_bucket(len(tokens)))
    if family == "UNIGRAM_OPEN":
        return []
    if family == "LAYOUT_OPEN":
        return [layout]
    prev = "<BOS>" if index == 0 else tokens[index - 1]
    shape = ("SHAPE", *layout[1:], token_length_bucket(prev), prev[:1], prev[-1:])
    if family == "PREV_SHAPE_LAYOUT_OPEN":
        return [layout, shape]
    if family == "PREV_ID_LAYOUT_OPEN":
        exact = ("PREV_ID", *layout[1:], prev)
        return [layout, shape, exact]
    raise ValueError(f"unknown family: {family}")


class ByteBigramCode:
    def __init__(self) -> None:
        self.counts: dict[int, Counter] = defaultdict(Counter)
        self.totals: Counter = Counter()

    def fit(self, tokens: list[str]) -> "ByteBigramCode":
        for token in tokens:
            prev = BOS_BYTE
            for symbol in list(token.encode("utf-8")) + [END_BYTE]:
                self.counts[prev][symbol] += 1
                self.totals[prev] += 1
                prev = symbol
        return self

    def bits(self, token: str) -> float:
        total_bits = 0.0
        prev = BOS_BYTE
        alphabet = END_BYTE + 1
        for symbol in list(token.encode("utf-8")) + [END_BYTE]:
            probability = ((self.counts[prev][symbol] + BETA) /
                           (self.totals[prev] + BETA * alphabet))
            total_bits -= math.log2(probability)
            prev = symbol
        return total_bits


class SurfaceCode:
    def __init__(self, family: str) -> None:
        if family not in FAMILIES:
            raise ValueError(f"unknown family: {family}")
        self.family = family
        self.dictionary: set[str] = set()
        self.base = Counter()
        self.base_total = 0
        self.context_counts: dict[tuple, Counter] = defaultdict(Counter)
        self.context_totals: Counter = Counter()
        self.byte_code = ByteBigramCode()

    def fit(self, records: list[dict]) -> "SurfaceCode":
        frequencies = Counter(t for r in records for t in r["tokens"])
        self.dictionary = {t for t, n in frequencies.items() if n >= MIN_DICTIONARY_COUNT}
        self.byte_code.fit([t for r in records for t in r["tokens"]])
        for record in records:
            tokens = record["tokens"]
            for i, token in enumerate(tokens):
                symbol = token if token in self.dictionary else ESC
                self.base[symbol] += 1
                self.base_total += 1
                for context in context_levels(self.family, tokens, i):
                    self.context_counts[context][symbol] += 1
                    self.context_totals[context] += 1
        if not self.base_total:
            raise ValueError("empty training corpus")
        return self

    def symbol_probability(self, symbol: str, levels: list[tuple]) -> float:
        vocabulary_size = len(self.dictionary) + 1
        probability = ((self.base[symbol] + BETA) /
                       (self.base_total + BETA * vocabulary_size))
        for context in levels:
            probability = ((self.context_counts[context][symbol] + ALPHA * probability) /
                           (self.context_totals[context] + ALPHA))
        return probability

    def token_bits(self, tokens: list[str], index: int) -> tuple[float, bool]:
        token = tokens[index]
        escaped = token not in self.dictionary
        symbol = ESC if escaped else token
        probability = self.symbol_probability(symbol, context_levels(self.family, tokens, index))
        bits = -math.log2(max(probability, 1e-300))
        if escaped:
            bits += self.byte_code.bits(token)
        return bits, escaped

    def score(self, records: list[dict]) -> dict:
        line_bits, line_tokens = [], []
        escaped = 0
        for record in records:
            bits = 0.0
            for i in range(len(record["tokens"])):
                item_bits, item_escaped = self.token_bits(record["tokens"], i)
                bits += item_bits
                escaped += int(item_escaped)
            if record["tokens"]:
                line_bits.append(bits)
                line_tokens.append(len(record["tokens"]))
        total_tokens = sum(line_tokens)
        if not total_tokens:
            raise ValueError("empty scoring corpus")
        return {"total_bits": float(sum(line_bits)), "tokens": total_tokens,
                "bits_per_token": float(sum(line_bits) / total_tokens),
                "escaped_tokens": escaped, "escape_rate": escaped / total_tokens,
                "line_bits": line_bits, "line_tokens": line_tokens}


def select_family(train_records: list[dict]) -> tuple[str, list[dict]]:
    fit, dev = internal_train_split(train_records)
    rows = []
    for family in FAMILIES:
        model = SurfaceCode(family).fit(fit)
        score = model.score(dev)
        rows.append({"family": family, "fit_lines": len(fit), "selection_lines": len(dev),
                     "selection_tokens": score["tokens"],
                     "selection_bits_per_token": score["bits_per_token"],
                     "selection_escape_rate": score["escape_rate"]})
    selected = min(rows, key=lambda row: (row["selection_bits_per_token"], row["family"]))
    return selected["family"], rows


def bootstrap_ci(line_bits: list[float], line_tokens: list[int]) -> list[float]:
    bits = np.asarray(line_bits, dtype=float)
    tokens = np.asarray(line_tokens, dtype=float)
    rng = np.random.default_rng(SEED)
    values = np.empty(BOOTSTRAPS, dtype=float)
    for i in range(BOOTSTRAPS):
        idx = rng.integers(0, len(bits), len(bits))
        values[i] = bits[idx].sum() / tokens[idx].sum()
    return [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))]


def verify_corpus_hash(corpus: dict) -> None:
    body = dict(corpus)
    expected = body.pop("corpus_sha256", None)
    if expected != canonical_hash(body):
        raise ValueError("canonical corpus hash mismatch")


def analyze(corpus: dict, label: str) -> dict:
    verify_corpus_hash(corpus)
    train = split_records(corpus, "train")
    validation = split_records(corpus, "validation")
    selected, selection = select_family(train)
    model = SurfaceCode(selected).fit(train)
    score = model.score(validation)
    line_array = np.asarray(score["line_bits"], dtype=float)
    output = {
        "schema": SCHEMA,
        "date": "2026-08-26",
        "label": label,
        "corpus_name": corpus["name"],
        "corpus_sha256": corpus["corpus_sha256"],
        "estimand": "lossless residual selection codelength; upper bound on hidden bandwidth",
        "model_contract": {
            "families": list(FAMILIES), "alpha": ALPHA, "base_beta": BETA,
            "minimum_dictionary_count": MIN_DICTIONARY_COUNT,
            "oov_code": "ESC + frozen UTF-8 byte-bigram spelling code",
            "selection": "deterministic 80/20 page split inside TRAIN",
            "seed": SEED,
        },
        "candidate_selection": selection,
        "selected_family": selected,
        "train_counts": {"lines": len(train),
                         "tokens": sum(len(r["tokens"]) for r in train)},
        "validation_counts": {"lines": len(validation), "tokens": score["tokens"]},
        "residual_capacity": {
            "total_bits": score["total_bits"],
            "bits_per_token": score["bits_per_token"],
            "bootstrap_95_ci_bits_per_token": bootstrap_ci(score["line_bits"], score["line_tokens"]),
            "mean_bits_per_line": float(line_array.mean()),
            "median_bits_per_line": float(np.median(line_array)),
            "p95_bits_per_line": float(np.quantile(line_array, 0.95)),
            "escaped_tokens": score["escaped_tokens"],
            "escape_rate": score["escape_rate"],
        },
        "bootstraps": BOOTSTRAPS,
        "final_test_used": False,
        "interpretation_limit": "Capacity is an upper bound, not evidence that residual choices carry content.",
    }
    output["result_sha256"] = canonical_hash(output)
    return output


class FrozenLabelCode:
    """Small-label hierarchical code used only for the aligned positive probe."""
    def __init__(self, use_surface: bool) -> None:
        self.use_surface = use_surface
        self.labels: set[str] = set()
        self.base = Counter()
        self.total = 0
        self.context = defaultdict(Counter)
        self.context_total = Counter()

    def key(self, record: dict, index: int) -> tuple:
        layout = (position_bucket(index, len(record["tokens"])),
                  line_length_bucket(len(record["tokens"])))
        return (record["tokens"][index], *layout) if self.use_surface else layout

    def fit(self, records: list[dict]) -> "FrozenLabelCode":
        for record in records:
            if len(record["tokens"]) != len(record["hidden_onsets"]):
                raise ValueError("positive alignment mismatch")
            for i, label in enumerate(record["hidden_onsets"]):
                self.labels.add(label)
                self.base[label] += 1
                self.total += 1
                key = self.key(record, i)
                self.context[key][label] += 1
                self.context_total[key] += 1
        return self

    def log_probabilities(self, records: list[dict]) -> tuple[np.ndarray, np.ndarray]:
        labels = sorted(self.labels)
        label_index = {label: i for i, label in enumerate(labels)}
        rows, targets = [], []
        k = len(labels)
        for record in records:
            if len(record["tokens"]) != len(record["hidden_onsets"]):
                raise ValueError("positive alignment mismatch")
            for i, label in enumerate(record["hidden_onsets"]):
                if label not in label_index:
                    raise ValueError(f"unseen validation onset: {label}")
                base = np.asarray([(self.base[x] + BETA) / (self.total + BETA * k)
                                   for x in labels], dtype=float)
                key = self.key(record, i)
                probs = np.asarray([(self.context[key][x] + ALPHA * base[j]) /
                                    (self.context_total[key] + ALPHA)
                                    for j, x in enumerate(labels)], dtype=float)
                rows.append(np.log2(np.maximum(probs, 1e-300)))
                targets.append(label_index[label])
        return np.vstack(rows), np.asarray(targets, dtype=int)


def positive_probe(corpus: dict) -> dict:
    train = split_records(corpus, "train")
    validation = split_records(corpus, "validation")
    baseline = FrozenLabelCode(False).fit(train)
    probe = FrozenLabelCode(True).fit(train)
    baseline_logp, targets = baseline.log_probabilities(validation)
    probe_logp, targets2 = probe.log_probabilities(validation)
    if not np.array_equal(targets, targets2):
        raise AssertionError("probe target mismatch")
    rows = np.arange(len(targets))
    observed = float(np.mean(probe_logp[rows, targets] - baseline_logp[rows, targets]))
    rng = np.random.default_rng(SEED)
    null = np.empty(PERMUTATIONS, dtype=float)
    for i in range(PERMUTATIONS):
        permuted = rng.permutation(targets)
        null[i] = np.mean(probe_logp[rows, permuted] - baseline_logp[rows, permuted])
    p = (1 + int(np.sum(null >= observed))) / (PERMUTATIONS + 1)
    return {
        "target": "normalized source-word onset",
        "validation_tokens": len(targets),
        "layout_only_cross_entropy_bits_per_token": float(-np.mean(baseline_logp[rows, targets])),
        "surface_probe_cross_entropy_bits_per_token": float(-np.mean(probe_logp[rows, targets])),
        "recoverable_information_lower_bound_bits_per_token": observed,
        "permutations": PERMUTATIONS,
        "one_sided_permutation_p": p,
        "null_gain_mean": float(null.mean()),
        "null_gain_p99": float(np.quantile(null, 0.99)),
    }


def edit_distance_one(a: str, b: str) -> bool:
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) > len(b):
        a, b = b, a
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    i = j = differences = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1; j += 1
        else:
            differences += 1; j += 1
            if differences > 1:
                return False
    return True


def surface_descriptors(corpus: dict) -> dict:
    validation = split_records(corpus, "validation")
    tokens = [t for r in validation for t in r["tokens"]]
    hidden = [t for r in validation for t in r["hidden_words"]]
    adjacent = [(a, b) for r in validation for a, b in zip(r["tokens"], r["tokens"][1:])]
    return {
        "surface_types": len(set(tokens)), "hidden_word_types": len(set(hidden)),
        "hidden_to_surface_type_ratio": len(set(hidden)) / max(1, len(set(tokens))),
        "mean_surface_token_codepoints": sum(map(len, tokens)) / len(tokens),
        "exact_adjacent_rate": sum(a == b for a, b in adjacent) / max(1, len(adjacent)),
        "nonidentical_edit_distance_one_adjacent_rate":
            sum(edit_distance_one(a, b) for a, b in adjacent) / max(1, len(adjacent)),
    }


def calibrate_positive(corpus: dict, label: str) -> dict:
    if corpus.get("schema") != "PHASE18_ALIGNED_LINE_CORPUS_v1":
        raise ValueError("unexpected positive-control schema")
    capacity = analyze(corpus, label)
    probe = positive_probe(corpus)
    residual = capacity["residual_capacity"]["bits_per_token"]
    recovered = probe["recoverable_information_lower_bound_bits_per_token"]
    conditions = {
        "validation_at_least_5000_tokens": probe["validation_tokens"] >= 5000,
        "recoverable_information_at_least_1_bit_per_token": recovered >= TEXT_BANDWIDTH_THRESHOLD,
        "permutation_p_at_most_0_01": probe["one_sided_permutation_p"] <= 0.01,
        "residual_bound_covers_recoverable_information": residual + 1e-9 >= recovered,
        "final_test_unused": not capacity["final_test_used"],
    }
    output = {
        "schema": POSITIVE_SCHEMA,
        "date": "2026-08-26",
        "label": label,
        "corpus_sha256": corpus["corpus_sha256"],
        "capacity_result": capacity,
        "known_hidden_content_probe": probe,
        "surface_descriptors": surface_descriptors(corpus),
        "gate_conditions": conditions,
        "positive_calibration_passed": all(conditions.values()),
        "voynich_authorized": all(conditions.values()),
        "final_test_used": False,
    }
    output["result_sha256"] = canonical_hash(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    analyze_parser = sub.add_parser("analyze")
    analyze_parser.add_argument("--corpus", required=True)
    analyze_parser.add_argument("--label", required=True)
    analyze_parser.add_argument("--out", required=True)
    positive_parser = sub.add_parser("calibrate-positive")
    positive_parser.add_argument("--corpus", required=True)
    positive_parser.add_argument("--label", required=True)
    positive_parser.add_argument("--out", required=True)
    args = parser.parse_args()
    corpus = json.loads(Path(args.corpus).read_text(encoding="utf-8"))
    result = (analyze(corpus, args.label) if args.command == "analyze"
              else calibrate_positive(corpus, args.label))
    write_json(Path(args.out), result)
    print(json.dumps({"out": args.out, "schema": result["schema"],
                      "result_sha256": result["result_sha256"],
                      "positive_calibration_passed": result.get("positive_calibration_passed")},
                     indent=2))


if __name__ == "__main__":
    main()

