#!/usr/bin/env python3
"""Test a paragraph-final closure allomorph against other physical line endings."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from phase22_human_layout.paragraph_scan import clean_letters, parse_ivtff


TERMINALS = "lmnrs y".replace(" ", "")


@dataclass(frozen=True)
class Occurrence:
    page: str
    section: str
    paragraph_end: int
    token: str
    raw_terminal: str
    raw_pre1: str
    raw_pre2: str
    stem: str
    terminal: str
    stem_last1: str
    stem_last2: str


def load_train_pages(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8") as fh:
        return {row["page"] for row in csv.DictReader(fh) if row["split"] == "train"}


def decompose(token: str) -> tuple[str, str]:
    token = clean_letters(token)
    if token and token[-1] in TERMINALS:
        return token[:-1], token[-1]
    return token, "Ø"


def occurrences(path: Path, train_pages: set[str]) -> list[Occurrence]:
    out = []
    for line in parse_ivtff(path):
        if line.page not in train_pages or not line.locus_type.startswith("P") or not line.tokens:
            continue
        token = clean_letters(line.tokens[-1])
        if not token:
            continue
        stem, terminal = decompose(token)
        out.append(
            Occurrence(
                page=line.page,
                section=line.illustration or "UNKNOWN",
                paragraph_end=int(line.paragraph_end),
                token=token,
                raw_terminal=token[-1],
                raw_pre1=token[-2] if len(token) >= 2 else "^",
                raw_pre2=token[-3:-1] if len(token) >= 3 else "^" + token[:-1],
                stem=stem,
                terminal=terminal,
                stem_last1=stem[-1] if stem else "^",
                stem_last2=stem[-2:] if len(stem) >= 2 else "^" + stem,
            )
        )
    return out


def entropy(counter: Counter) -> float:
    n = sum(counter.values())
    if not n:
        return 0.0
    return -sum((v / n) * math.log2(v / n) for v in counter.values() if v)


def conditional_information(rows: list[Occurrence], context_attr: str, terminal_attr: str, labels: list[int] | None = None) -> float:
    labels = labels if labels is not None else [x.paragraph_end for x in rows]
    by_context: dict[tuple[str, str], Counter] = defaultdict(Counter)
    by_both: dict[tuple[str, str, str], Counter] = defaultdict(Counter)
    for x, y in zip(rows, labels):
        context = (x.section, getattr(x, context_attr))
        terminal = getattr(x, terminal_attr)
        by_context[context][y] += 1
        by_both[context + (terminal,)][y] += 1
    n = len(rows)
    h_context = sum(sum(c.values()) * entropy(c) for c in by_context.values()) / n
    h_both = sum(sum(c.values()) * entropy(c) for c in by_both.values()) / n
    return h_context - h_both


def permuted_labels_within_page(rows: list[Occurrence], rng: random.Random) -> list[int]:
    groups: dict[str, list[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        groups[row.page].append(i)
    labels = [x.paragraph_end for x in rows]
    for idxs in groups.values():
        vals = [labels[i] for i in idxs]
        rng.shuffle(vals)
        for i, value in zip(idxs, vals):
            labels[i] = value
    return labels


def permutation_test(rows: list[Occurrence], context_attr: str, terminal_attr: str, n_perm: int, seed: int) -> dict:
    observed = conditional_information(rows, context_attr, terminal_attr)
    rng = random.Random(seed)
    null = [
        conditional_information(rows, context_attr, terminal_attr, permuted_labels_within_page(rows, rng))
        for _ in range(n_perm)
    ]
    null_sorted = sorted(null)
    q99 = null_sorted[min(len(null_sorted) - 1, math.ceil(0.99 * len(null_sorted)) - 1)]
    mean = statistics.mean(null)
    sd = statistics.pstdev(null)
    return {
        "observed_bits": observed,
        "null_mean_bits": mean,
        "null_sd_bits": sd,
        "null_q99_bits": q99,
        "z": (observed - mean) / sd if sd else None,
        "p_upper": (1 + sum(x >= observed for x in null)) / (n_perm + 1),
        "permutations": n_perm,
        "seed": seed,
    }


def auc(labels: list[int], scores: list[float]) -> float | None:
    pos = [s for y, s in zip(labels, scores) if y]
    neg = [s for y, s in zip(labels, scores) if not y]
    if not pos or not neg:
        return None
    wins = 0.0
    for p in pos:
        for n in neg:
            wins += (p > n) + 0.5 * (p == n)
    return wins / (len(pos) * len(neg))


def balanced_accuracy(labels: list[int], scores: list[float], threshold: float = 0.0) -> float | None:
    pos = [s for y, s in zip(labels, scores) if y]
    neg = [s for y, s in zip(labels, scores) if not y]
    if not pos or not neg:
        return None
    sensitivity = sum(s > threshold for s in pos) / len(pos)
    specificity = sum(s <= threshold for s in neg) / len(neg)
    return 0.5 * (sensitivity + specificity)


def loo_mapping(rows: list[Occurrence], context_attr: str, terminal_attr: str) -> dict:
    """Learn context-specific terminal log odds on every page except the scored page."""
    pages = sorted({x.page for x in rows})
    labels = []
    scores = []
    predicted_terminal_matches = []
    eligible_paragraph_ends = 0
    mapping_votes: dict[str, Counter] = defaultdict(Counter)
    terminals = sorted({getattr(x, terminal_attr) for x in rows})
    for held in pages:
        train = [x for x in rows if x.page != held]
        test = [x for x in rows if x.page == held]
        counts: dict[str, dict[int, Counter]] = defaultdict(lambda: {0: Counter(), 1: Counter()})
        totals: dict[str, Counter] = defaultdict(Counter)
        for x in train:
            ctx = getattr(x, context_attr)
            term = getattr(x, terminal_attr)
            counts[ctx][x.paragraph_end][term] += 1
            totals[ctx][x.paragraph_end] += 1
        for ctx in counts:
            best = max(
                terminals,
                key=lambda t: math.log((counts[ctx][1][t] + 0.5) / (totals[ctx][1] + 0.5 * len(terminals)))
                - math.log((counts[ctx][0][t] + 0.5) / (totals[ctx][0] + 0.5 * len(terminals))),
            )
            mapping_votes[ctx][best] += 1
        for x in test:
            ctx = getattr(x, context_attr)
            term = getattr(x, terminal_attr)
            if ctx not in counts:
                continue
            score = math.log((counts[ctx][1][term] + 0.5) / (totals[ctx][1] + 0.5 * len(terminals))) - math.log(
                (counts[ctx][0][term] + 0.5) / (totals[ctx][0] + 0.5 * len(terminals))
            )
            best = max(
                terminals,
                key=lambda t: math.log((counts[ctx][1][t] + 0.5) / (totals[ctx][1] + 0.5 * len(terminals)))
                - math.log((counts[ctx][0][t] + 0.5) / (totals[ctx][0] + 0.5 * len(terminals))),
            )
            labels.append(x.paragraph_end)
            scores.append(score)
            if x.paragraph_end:
                eligible_paragraph_ends += 1
                predicted_terminal_matches.append(int(term == best))
    stable_mapping = {ctx: votes.most_common(1)[0][0] for ctx, votes in sorted(mapping_votes.items())}
    return {
        "eligible_occurrences": len(labels),
        "eligible_paragraph_ends": eligible_paragraph_ends,
        "auc": auc(labels, scores),
        "balanced_accuracy_at_log_odds_zero": balanced_accuracy(labels, scores),
        "paragraph_end_candidate_coverage": statistics.mean(predicted_terminal_matches) if predicted_terminal_matches else None,
        "stable_context_to_closure_terminal": stable_mapping,
    }


def terminal_contrasts(rows: list[Occurrence]) -> dict:
    p = Counter(x.terminal for x in rows if x.paragraph_end)
    c = Counter(x.terminal for x in rows if not x.paragraph_end)
    pn, cn = sum(p.values()), sum(c.values())
    out = {}
    for terminal in sorted(set(p) | set(c)):
        a, b = p[terminal], pn - p[terminal]
        d, e = c[terminal], cn - c[terminal]
        out[terminal] = {
            "paragraph_end": {"count": a, "total": pn, "rate": a / pn if pn else None},
            "other_line_end": {"count": d, "total": cn, "rate": d / cn if cn else None},
            "corrected_odds_ratio": ((a + 0.5) * (e + 0.5)) / ((b + 0.5) * (d + 0.5)),
        }
    return out


def injected_allomorph_positive(rows: list[Occurrence], n_perm: int, seed: int) -> dict:
    """Inject a deterministic existing-terminal closure selected by stem-final class."""
    inventory = sorted({x.terminal for x in rows})
    control: dict[str, Counter] = defaultdict(Counter)
    for x in rows:
        if not x.paragraph_end:
            control[x.stem_last1][x.terminal] += 1
    mapping = {
        ctx: min(inventory, key=lambda t: (counts[t], t))
        for ctx, counts in control.items()
    }
    injected = [
        replace(x, terminal=mapping.get(x.stem_last1, x.terminal)) if x.paragraph_end else x
        for x in rows
    ]
    return {
        "description": "Each paragraph end receives one existing terminal deterministically conditioned on stem_last1; controls are unchanged.",
        "injected_mapping": dict(sorted(mapping.items())),
        "permutation_test": permutation_test(injected, "stem_last1", "terminal", n_perm, seed),
        "loo_mapping": loo_mapping(injected, "stem_last1", "terminal"),
    }


def exact_stem_pairs(rows: list[Occurrence], min_each: int = 2) -> dict:
    counts: dict[str, dict[int, Counter]] = defaultdict(lambda: {0: Counter(), 1: Counter()})
    for x in rows:
        counts[x.stem][x.paragraph_end][x.terminal] += 1
    pairs = []
    covered_ends = 0
    total_ends = sum(x.paragraph_end for x in rows)
    for stem, by_y in counts.items():
        if sum(by_y[0].values()) < min_each or sum(by_y[1].values()) < min_each:
            continue
        p_top, p_n = by_y[1].most_common(1)[0]
        c_top, c_n = by_y[0].most_common(1)[0]
        covered_ends += sum(by_y[1].values())
        pairs.append(
            {
                "stem": stem,
                "paragraph_end_total": sum(by_y[1].values()),
                "other_line_end_total": sum(by_y[0].values()),
                "paragraph_top_terminal": p_top,
                "paragraph_top_count": p_n,
                "control_top_terminal": c_top,
                "control_top_count": c_n,
                "different_top_terminal": p_top != c_top,
                "paragraph_terminals": dict(by_y[1].most_common()),
                "control_terminals": dict(by_y[0].most_common()),
            }
        )
    pairs.sort(key=lambda x: (-x["paragraph_end_total"], x["stem"]))
    return {
        "eligible_stems": len(pairs),
        "paragraph_end_coverage": covered_ends / total_ends if total_ends else None,
        "stems_with_different_top_terminal": sum(x["different_top_terminal"] for x in pairs),
        "top_pairs": pairs[:100],
    }


def summarize(rows: list[Occurrence], n_perm: int, seed: int) -> dict:
    return {
        "physical_line_ends": len(rows),
        "paragraph_ends": sum(x.paragraph_end for x in rows),
        "other_line_ends": sum(not x.paragraph_end for x in rows),
        "raw_suffix_tests": {
            "previous_1_plus_raw_terminal": permutation_test(rows, "raw_pre1", "raw_terminal", n_perm, seed),
            "previous_2_plus_raw_terminal": permutation_test(rows, "raw_pre2", "raw_terminal", n_perm, seed + 1),
            "loo_previous_1_mapping": loo_mapping(rows, "raw_pre1", "raw_terminal"),
            "loo_previous_2_mapping": loo_mapping(rows, "raw_pre2", "raw_terminal"),
        },
        "frozen_terminal_family_tests": {
            "stem_last1_plus_terminal": permutation_test(rows, "stem_last1", "terminal", n_perm, seed + 2),
            "stem_last2_plus_terminal": permutation_test(rows, "stem_last2", "terminal", n_perm, seed + 3),
            "loo_stem_last1_mapping": loo_mapping(rows, "stem_last1", "terminal"),
            "loo_stem_last2_mapping": loo_mapping(rows, "stem_last2", "terminal"),
            "exact_recurring_stem_pairs": exact_stem_pairs(rows),
        },
        "paragraph_terminal_counts": dict(Counter(x.terminal for x in rows if x.paragraph_end).most_common()),
        "other_line_terminal_counts": dict(Counter(x.terminal for x in rows if not x.paragraph_end).most_common()),
        "terminal_contrasts": terminal_contrasts(rows),
        "injected_allomorph_positive_control": injected_allomorph_positive(rows, n_perm, seed + 4),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zl", type=Path, required=True)
    ap.add_argument("--it", type=Path, required=True)
    ap.add_argument("--split", type=Path, required=True)
    ap.add_argument("--permutations", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=230827)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    train_pages = load_train_pages(args.split)
    result = {
        "status": "TRAIN_ONLY_EXPLORATORY_PARAGRAPH_CLOSURE_SCAN",
        "hypothesis": "mandatory paragraph closure with preceding-word-final-conditioned visible allomorph",
        "terminal_inventory": list(TERMINALS) + ["Ø"],
        "train_pages_in_manifest": len(train_pages),
        "ZL3b": summarize(occurrences(args.zl, train_pages), args.permutations, args.seed),
        "IT2a": summarize(occurrences(args.it, train_pages), args.permutations, args.seed + 10000),
        "success_rule": {
            "permutation": "observed gain above within-page null q99",
            "candidate_coverage_min": 0.80,
            "auc_min": 0.80,
            "replication": "same direction and mapping family in IT2a",
        },
        "limits": [
            "Paragraph labels are transcriber annotations pending blind image adjudication.",
            "The scan tests a bounded suffix/allomorph model; it cannot exclude an untranscribed flourish or spacing-only stop.",
            "No terminal is assigned a sound or semantic value.",
            "Validation and final-test pages are not used.",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
