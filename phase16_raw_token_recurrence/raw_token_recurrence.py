#!/usr/bin/env python3
"""Frozen Phase-16 raw-token recurrence/burstiness instrument.

The instrument uses exact token identity and the Phase-15 physical line/page
corpora.  It never reads final-test records.  Three nested permutation families
separate document-to-page clustering, page-to-line clustering and within-line
order.  No class induction, spelling normalization or semantic information is
used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


SEED = 20260826
PERMUTATIONS = 2000
ALPHA = 0.01
SCHEMA = "PHASE16_RAW_TOKEN_RECURRENCE_v1"

METRICS = (
    "page_repeat_mass",
    "line_repeat_mass",
    "page_pair_concentration",
    "line_pair_concentration",
    "page_frequency_fano",
    "line_frequency_fano",
    "page_return_gap1",
    "page_return_gap2_4",
    "line_identity_gap1",
    "line_identity_gap2_4",
    "line_identity_gap5_16",
)

VARYING = {
    "document_shuffle": METRICS,
    "page_shuffle": (
        "line_repeat_mass",
        "line_pair_concentration",
        "line_frequency_fano",
        "line_identity_gap1",
        "line_identity_gap2_4",
        "line_identity_gap5_16",
    ),
    "line_shuffle": (
        "line_identity_gap1",
        "line_identity_gap2_4",
        "line_identity_gap5_16",
    ),
}


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def stable_u64(text: str) -> int:
    return int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def validate_corpus(corpus: dict) -> None:
    expected = corpus.get("corpus_sha256")
    if not expected:
        raise ValueError("corpus_sha256 is required")
    body = dict(corpus)
    body.pop("corpus_sha256", None)
    actual = canonical_hash(body)
    if actual != expected:
        raise ValueError(f"corpus canonical hash mismatch: {actual} != {expected}")


def validation_records(corpus: dict) -> list[dict]:
    validate_corpus(corpus)
    records = [r for r in corpus["records"] if r["split"] == "validation"]
    records.sort(key=lambda r: (r["document"], r["page"], r["order"], r["line_id"]))
    if not records:
        raise ValueError("VALIDATION is empty")
    if any(r["split"] != "validation" for r in records):
        raise AssertionError("final-test lock failure")
    return records


class Layout:
    """Integer-coded, immutable validation layout."""

    def __init__(self, records: list[dict]):
        vocabulary = sorted({t for r in records for t in r["tokens"]})
        token_id = {t: i for i, t in enumerate(vocabulary)}
        self.lines = [[token_id[t] for t in r["tokens"]] for r in records]
        self.line_meta = [(r["document"], r["page"]) for r in records]
        self.documents: dict[str, list[int]] = defaultdict(list)
        self.pages: dict[tuple[str, str], list[int]] = defaultdict(list)
        for i, (document, page) in enumerate(self.line_meta):
            self.documents[document].append(i)
            self.pages[(document, page)].append(i)
        self.page_order: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for key in sorted(self.pages):
            self.page_order[key[0]].append(key)
        self.vocabulary_size = len(vocabulary)
        self.document_identity_pairs = 0
        for indices in self.documents.values():
            counts = Counter(t for i in indices for t in self.lines[i])
            self.document_identity_pairs += sum(n * (n - 1) // 2 for n in counts.values())

    def counts(self) -> dict:
        return {
            "documents": len(self.documents),
            "pages": len(self.pages),
            "lines": len(self.lines),
            "tokens": sum(map(len, self.lines)),
            "types": self.vocabulary_size,
        }


def grouped_descriptors(counters: list[Counter], group_lengths: list[int],
                        possible_pairs: int) -> tuple[float, float, float]:
    """Occurrence-weighted count dispersion across fixed groups, types n>=4."""
    if not counters:
        return 0.0, 0.0, 0.0
    total = Counter()
    for counts in counters:
        total.update(counts)
    repeated = sum(sum(n - 1 for n in counts.values() if n > 1) for counts in counters)
    token_total = sum(group_lengths)
    excess = repeated / token_total if token_total else 0.0
    within_pairs = sum(sum(n * (n - 1) // 2 for n in counts.values())
                       for counts in counters)
    concentration = within_pairs / possible_pairs if possible_pairs else 0.0
    eligible = {t for t, n in total.items() if n >= 4}
    if not eligible:
        return excess, concentration, 0.0
    sumsq = Counter()
    for counts in counters:
        for t, n in counts.items():
            if t in eligible:
                sumsq[t] += n * n
    k = len(counters)
    weighted = weight = 0.0
    for t in eligible:
        mean = total[t] / k
        variance = sumsq[t] / k - mean * mean
        fano = variance / mean if mean else 0.0
        weighted += total[t] * fano
        weight += total[t]
    return excess, concentration, weighted / weight if weight else 0.0


def line_identity_rate(lines: list[list[int]], first_gap: int, last_gap: int) -> float:
    hits = pairs = 0
    for line in lines:
        upper = min(last_gap, len(line) - 1)
        for gap in range(first_gap, upper + 1):
            pairs += len(line) - gap
            hits += sum(a == b for a, b in zip(line[:-gap], line[gap:]))
    return hits / pairs if pairs else 0.0


def page_return_rate(page_order: dict[str, list[tuple[str, str]]],
                     page_counts: dict[tuple[str, str], Counter],
                     page_lengths: dict[tuple[str, str], int],
                     first_gap: int, last_gap: int) -> float:
    hits = pairs = 0
    for keys in page_order.values():
        upper = min(last_gap, len(keys) - 1)
        for gap in range(first_gap, upper + 1):
            for i in range(len(keys) - gap):
                left = page_counts[keys[i]]
                right = page_counts[keys[i + gap]]
                if len(left) > len(right):
                    left, right = right, left
                hits += sum(n * right.get(t, 0) for t, n in left.items())
                pairs += page_lengths[keys[i]] * page_lengths[keys[i + gap]]
    return hits / pairs if pairs else 0.0


def metric_vector(layout: Layout, lines: list[list[int]],
                  requested: tuple[str, ...] = METRICS) -> dict[str, float]:
    wanted = set(requested)
    result: dict[str, float] = {}
    page_names = {
        "page_repeat_mass", "page_pair_concentration", "page_frequency_fano",
        "page_return_gap1", "page_return_gap2_4",
    }
    line_names = {
        "line_repeat_mass", "line_pair_concentration", "line_frequency_fano",
    }
    page_counts = None
    page_lengths = None
    line_counts = None
    if wanted & page_names:
        page_counts = {}
        page_lengths = {}
        for key, idxs in layout.pages.items():
            counts = Counter(t for i in idxs for t in lines[i])
            page_counts[key] = counts
            page_lengths[key] = sum(map(len, (lines[i] for i in idxs)))
        page_values = grouped_descriptors(list(page_counts.values()),
                                          list(page_lengths.values()),
                                          layout.document_identity_pairs)
        for name, value in zip(("page_repeat_mass", "page_pair_concentration",
                                "page_frequency_fano"), page_values):
            if name in wanted:
                result[name] = value
    if wanted & line_names:
        line_counts = [Counter(line) for line in lines]
        line_values = grouped_descriptors(line_counts, list(map(len, lines)),
                                          layout.document_identity_pairs)
        for name, value in zip(("line_repeat_mass", "line_pair_concentration",
                                "line_frequency_fano"), line_values):
            if name in wanted:
                result[name] = value
    if "page_return_gap1" in wanted:
        result["page_return_gap1"] = page_return_rate(layout.page_order, page_counts,
                                                       page_lengths, 1, 1)
    if "page_return_gap2_4" in wanted:
        result["page_return_gap2_4"] = page_return_rate(layout.page_order, page_counts,
                                                         page_lengths, 2, 4)
    if "line_identity_gap1" in wanted:
        result["line_identity_gap1"] = line_identity_rate(lines, 1, 1)
    if "line_identity_gap2_4" in wanted:
        result["line_identity_gap2_4"] = line_identity_rate(lines, 2, 4)
    if "line_identity_gap5_16" in wanted:
        result["line_identity_gap5_16"] = line_identity_rate(lines, 5, 16)
    return result


def redistribute(pool: list[int], indices: list[int], template: list[list[int]]) -> list[list[int]]:
    out: list[list[int]] = []
    position = 0
    for i in indices:
        n = len(template[i])
        out.append(pool[position:position + n])
        position += n
    if position != len(pool):
        raise AssertionError("shuffle redistribution mismatch")
    return out


def shuffled_lines(layout: Layout, family: str, rng: random.Random) -> list[list[int]]:
    source = layout.lines
    out = [line[:] for line in source]
    if family == "line_shuffle":
        for line in out:
            rng.shuffle(line)
    elif family == "page_shuffle":
        for indices in layout.pages.values():
            pool = [t for i in indices for t in source[i]]
            rng.shuffle(pool)
            for i, line in zip(indices, redistribute(pool, indices, source)):
                out[i] = line
    elif family == "document_shuffle":
        for indices in layout.documents.values():
            pool = [t for i in indices for t in source[i]]
            rng.shuffle(pool)
            for i, line in zip(indices, redistribute(pool, indices, source)):
                out[i] = line
    else:
        raise ValueError(f"unknown null family: {family}")
    return out


def quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return float("nan")
    position = probability * (len(ordered) - 1)
    lo = int(math.floor(position))
    hi = int(math.ceil(position))
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - position) + ordered[hi] * (position - lo)


def holm_adjust(raw: dict[str, float]) -> dict[str, float]:
    ordered = sorted(raw, key=lambda name: (raw[name], name))
    adjusted: dict[str, float] = {}
    running = 0.0
    m = len(ordered)
    for rank, name in enumerate(ordered):
        value = min(1.0, (m - rank) * raw[name])
        running = max(running, value)
        adjusted[name] = running
    return adjusted


def summarize_null(observed: dict[str, float], samples: dict[str, list[float]],
                   varying: tuple[str, ...], permutations: int) -> dict:
    raw_p: dict[str, float] = {}
    summary = {}
    for name in METRICS:
        values = samples[name]
        mean = statistics.fmean(values)
        sd = statistics.stdev(values) if len(values) > 1 else 0.0
        z = (observed[name] - mean) / sd if sd else 0.0
        centered = abs(observed[name] - mean)
        p = (1 + sum(abs(value - mean) >= centered for value in values)) / (permutations + 1)
        if name in varying:
            raw_p[name] = p
        summary[name] = {
            "observed": observed[name],
            "null_mean": mean,
            "null_variance": sd * sd,
            "z": z,
            "observed_to_null_ratio": observed[name] / mean if mean else None,
            "p_two_sided_plus_one": p if name in varying else None,
            "quantiles": {
                "q005": quantile(values, 0.005),
                "q025": quantile(values, 0.025),
                "q500": quantile(values, 0.500),
                "q975": quantile(values, 0.975),
                "q995": quantile(values, 0.995),
            },
            "varies_under_null": name in varying,
        }
    adjusted = holm_adjust(raw_p)
    for name in METRICS:
        summary[name]["holm_adjusted_p"] = adjusted.get(name)
        summary[name]["significant_holm_0_01"] = (
            adjusted.get(name) is not None and adjusted[name] <= ALPHA
        )
    return summary


def analyze(corpus: dict, label: str, permutations: int = PERMUTATIONS) -> dict:
    records = validation_records(corpus)
    layout = Layout(records)
    observed = metric_vector(layout, layout.lines)
    families = {}
    for family in ("document_shuffle", "page_shuffle", "line_shuffle"):
        seed = stable_u64(f"{SEED}:{corpus['corpus_sha256']}:{family}")
        rng = random.Random(seed)
        samples = {name: [] for name in METRICS}
        for _ in range(permutations):
            vector = metric_vector(layout, shuffled_lines(layout, family, rng), VARYING[family])
            for name in METRICS:
                # Non-varying metrics are retained as exact invariant descriptors,
                # but are excluded from multiplicity correction by the erratum.
                samples[name].append(vector.get(name, observed[name]))
        families[family] = {
            "seed": seed,
            "permutations": permutations,
            "holm_family_size": len(VARYING[family]),
            "metrics": summarize_null(observed, samples, VARYING[family], permutations),
        }
    all_counts = Counter(r["split"] for r in corpus["records"])
    result = {
        "schema": SCHEMA,
        "label": label,
        "corpus": corpus["name"],
        "corpus_sha256": corpus["corpus_sha256"],
        "seed_base": SEED,
        "permutations": permutations,
        "identity_contract": "Exact case-sensitive token strings; no Unicode, punctuation or case normalization.",
        "records_used": "VALIDATION only",
        "final_test_used": False,
        "split_record_counts": dict(sorted(all_counts.items())),
        "validation_counts": layout.counts(),
        "observed": observed,
        "null_families": families,
        "interpretation_lock": "Structural descriptor only; no H_C/H_D/H_G ranking is permitted.",
    }
    result["result_sha256"] = canonical_hash(result)
    return result


def corpus_payload(name: str, records: list[dict], source: dict) -> dict:
    body = {"schema": "PHASE15_LINE_CORPUS_v2", "name": name,
            "source": source, "records": records}
    body["corpus_sha256"] = canonical_hash(body)
    return body


def synthetic_corpora() -> dict[str, dict]:
    """Three deterministic fixtures frozen before real-corpus interpretation."""
    rng = random.Random(SEED)

    def rows(name: str, token_lines: list[list[str]]) -> dict:
        records = []
        for i, tokens in enumerate(token_lines):
            records.append({"document": name, "page": f"p{i // 8:03d}",
                            "order": i % 8, "line_id": f"l{i:04d}",
                            "split": "validation", "tokens": tokens})
        return corpus_payload(name, records, {"generator": name, "seed": SEED})

    weights = [1.0 / (i + 3) for i in range(80)]
    iid_lines = [rng.choices([f"t{i:02d}" for i in range(80)], weights=weights, k=12)
                 for _ in range(160)]

    cluster_lines = []
    for page in range(20):
        topic = (page // 4) % 5
        topic_tokens = [f"topic{topic}_{i}" for i in range(10)]
        common = [f"common{i}" for i in range(20)]
        for _ in range(8):
            cluster_lines.append([
                rng.choice(topic_tokens if rng.random() < 0.72 else common)
                for _ in range(12)
            ])

    order_lines = []
    for line in range(160):
        anchor = f"a{line % 24:02d}"
        fillers = [f"f{(line + j) % 70:02d}" for j in range(6)]
        sequence = []
        for filler in fillers:
            sequence.extend((anchor, filler))
        order_lines.append(sequence)

    return {
        "iid": rows("SYNTHETIC_IID_v1", iid_lines),
        "page_cluster": rows("SYNTHETIC_PAGE_CLUSTER_v1", cluster_lines),
        "line_order": rows("SYNTHETIC_LINE_ORDER_v1", order_lines),
    }


def calibration(permutations: int = PERMUTATIONS) -> dict:
    results = {name: analyze(corpus, name, permutations)
               for name, corpus in synthetic_corpora().items()}
    iid_z = [abs(metric["z"])
             for family in results["iid"]["null_families"].values()
             for metric in family["metrics"].values()
             if metric["varies_under_null"]]
    gates = {
        "iid_max_abs_z_at_most_3_5": max(iid_z) <= 3.5,
        "page_cluster_document_page_mass_z_at_least_5":
            results["page_cluster"]["null_families"]["document_shuffle"]["metrics"]
            ["page_repeat_mass"]["z"] >= 5.0,
        "page_cluster_short_page_return_z_at_least_5":
            results["page_cluster"]["null_families"]["document_shuffle"]["metrics"]
            ["page_return_gap1"]["z"] >= 5.0,
        "line_order_line_shuffle_gap1_abs_z_at_least_5":
            abs(results["line_order"]["null_families"]["line_shuffle"]["metrics"]
                ["line_identity_gap1"]["z"]) >= 5.0,
        "holm_minimum_resolution_below_0_01":
            len(METRICS) / (permutations + 1) < ALPHA,
    }
    output = {
        "schema": "PHASE16_SYNTHETIC_CALIBRATION_v1",
        "seed_base": SEED,
        "permutations": permutations,
        "iid_max_abs_z": max(iid_z),
        "gates": gates,
        "pass": all(gates.values()),
        "fixtures": results,
    }
    output["result_sha256"] = canonical_hash(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    cal = sub.add_parser("calibrate")
    cal.add_argument("--out", required=True)
    cal.add_argument("--permutations", type=int, default=PERMUTATIONS)
    run = sub.add_parser("analyze")
    run.add_argument("--corpus", required=True)
    run.add_argument("--label", required=True)
    run.add_argument("--out", required=True)
    run.add_argument("--permutations", type=int, default=PERMUTATIONS)
    args = parser.parse_args()
    if args.command == "calibrate":
        result = calibration(args.permutations)
    else:
        corpus = json.loads(Path(args.corpus).read_text(encoding="utf-8"))
        result = analyze(corpus, args.label, args.permutations)
    write_json(Path(args.out), result)
    print(json.dumps({"out": args.out, "schema": result["schema"],
                      "pass": result.get("pass"),
                      "result_sha256": result["result_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
