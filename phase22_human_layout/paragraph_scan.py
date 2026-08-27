#!/usr/bin/env python3
"""Scan IVTFF paragraph boundaries without treating them as ground truth.

The parser preserves three separate levels:

1. transcriber-proposed paragraph starts/ends (<%>, <$>);
2. physical line starts/ends;
3. token/glyph patterns that are tested only after boundaries are read.

ZL3b is the primary EVA descriptive source. IT2a is an independent EVA
challenger. GC2a contributes boundary annotations but uses v101, so its glyph
strings are not mixed into EVA glyph statistics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


PAGE_RE = re.compile(r"^<([^.,;>]+)>\s*(?:<!\s*(.*?)\s*>)?")
LINE_RE = re.compile(r"^<([^>]+)>\s*(.*)$")
VAR_RE = re.compile(r"\$([A-Z])=([^\s>]+)")
ALT_RE = re.compile(r"\[([^:\]]+)(?::[^\]]+)+\]")
COMMENT_RE = re.compile(r"<[^>]*>")
HIGH_ASCII_RE = re.compile(r"@\d{3};")


@dataclass(frozen=True)
class Line:
    page: str
    locus: str
    locus_type: str
    illustration: str
    paragraph_start: bool
    paragraph_end: bool
    tokens: tuple[str, ...]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tokenize(text: str) -> tuple[str, ...]:
    text = text.replace("<->", ".").replace("<~>", ".")
    text = text.replace("<%>", "").replace("<$>", "")
    text = ALT_RE.sub(lambda m: m.group(1), text)
    text = COMMENT_RE.sub("", text)
    text = HIGH_ASCII_RE.sub("¤", text)
    text = text.translate(str.maketrans({"{": "", "}": "", "(": "", ")": ""}))
    return tuple(t for t in re.split(r"[.,\s]+", text) if t)


def parse_ivtff(path: Path) -> list[Line]:
    page = ""
    page_vars: dict[str, str] = {}
    lines: list[Line] = []
    for raw in path.read_text(encoding="latin-1").splitlines():
        if not raw or raw.startswith("#"):
            continue
        pm = PAGE_RE.match(raw)
        if pm and "." not in pm.group(1):
            page = pm.group(1)
            page_vars = dict(VAR_RE.findall(pm.group(2) or ""))
            continue
        lm = LINE_RE.match(raw)
        if not lm or not page:
            continue
        locus, text = lm.groups()
        code = locus.split(",", 1)[1].split(";", 1)[0] if "," in locus else ""
        locus_type = code[1:] if len(code) >= 3 else ""
        lines.append(
            Line(
                page=page,
                locus=locus.split(",", 1)[0],
                locus_type=locus_type,
                illustration=page_vars.get("I", ""),
                paragraph_start="<%>" in text,
                paragraph_end="<$>" in text,
                tokens=tokenize(text),
            )
        )
    return lines


def clean_letters(token: str) -> str:
    return "".join(ch for ch in token.lower() if "a" <= ch <= "z")


def starts_direct_gallows(token: str) -> bool:
    token = clean_letters(token)
    return bool(token) and token[0] in "ktpf"


def contains_bench_gallows(token: str) -> bool:
    token = clean_letters(token)
    return any(unit in token for unit in ("ckh", "cth", "cph", "cfh"))


def ends_with(token: str, char: str) -> bool:
    token = clean_letters(token)
    return bool(token) and token.endswith(char)


def rate(n: int, d: int) -> float | None:
    return n / d if d else None


def odds_ratio(a: int, b: int, c: int, d: int) -> float:
    """Haldane-Anscombe corrected odds ratio for [[a,b],[c,d]]."""
    return ((a + 0.5) * (d + 0.5)) / ((b + 0.5) * (c + 0.5))


def boundary_agreement(a: list[Line], b: list[Line], attr: str) -> dict:
    sa = {line.locus for line in a if getattr(line, attr)}
    sb = {line.locus for line in b if getattr(line, attr)}
    union = sa | sb
    return {
        "a_count": len(sa),
        "b_count": len(sb),
        "intersection": len(sa & sb),
        "union": len(union),
        "jaccard": len(sa & sb) / len(union) if union else None,
        "a_only_examples": sorted(sa - sb)[:20],
        "b_only_examples": sorted(sb - sa)[:20],
    }


def summarize_eva(lines: list[Line]) -> dict:
    running = [line for line in lines if line.locus_type.startswith("P") and line.tokens]
    starts = [line for line in running if line.paragraph_start]
    nonstarts = [line for line in running if not line.paragraph_start]
    ends = [line for line in running if line.paragraph_end]
    nonends = [line for line in running if not line.paragraph_end]

    start_g = sum(starts_direct_gallows(x.tokens[0]) for x in starts)
    other_g = sum(starts_direct_gallows(x.tokens[0]) for x in nonstarts)
    start_bench = sum(contains_bench_gallows(x.tokens[0]) for x in starts)
    other_bench = sum(contains_bench_gallows(x.tokens[0]) for x in nonstarts)
    end_m = sum(ends_with(x.tokens[-1], "m") for x in ends)
    other_m = sum(ends_with(x.tokens[-1], "m") for x in nonends)

    first_start = Counter(clean_letters(x.tokens[0])[:1] or "?" for x in starts)
    first_other = Counter(clean_letters(x.tokens[0])[:1] or "?" for x in nonstarts)
    final_start = Counter(clean_letters(x.tokens[-1])[-1:] or "?" for x in ends)
    final_other = Counter(clean_letters(x.tokens[-1])[-1:] or "?" for x in nonends)

    terminal_profiles = {}
    for char in sorted(set(final_start) | set(final_other)):
        a = final_start[char]
        c = final_other[char]
        terminal_profiles[char] = {
            "paragraph_end": {"count": a, "total": len(ends), "rate": rate(a, len(ends))},
            "other_running_line": {"count": c, "total": len(nonends), "rate": rate(c, len(nonends))},
            "odds_ratio": odds_ratio(a, len(ends) - a, c, len(nonends) - c),
        }

    by_section: dict[str, dict[str, int]] = defaultdict(lambda: {"lines": 0, "paragraphs": 0, "ends": 0})
    for line in running:
        sec = line.illustration or "UNKNOWN"
        by_section[sec]["lines"] += 1
        by_section[sec]["paragraphs"] += int(line.paragraph_start)
        by_section[sec]["ends"] += int(line.paragraph_end)

    # Reconstruct paragraph lengths only inside each page; IVTFF requires paired
    # start/end markers on one page, but malformed stretches are reported.
    lengths_lines: list[int] = []
    lengths_tokens: list[int] = []
    malformed: list[str] = []
    current_page = None
    open_lines = open_tokens = 0
    opened = False
    for line in running:
        if current_page != line.page:
            if opened:
                malformed.append(f"{current_page}:unclosed")
            current_page, opened = line.page, False
        if line.paragraph_start:
            if opened:
                malformed.append(f"{line.page}:{line.locus}:nested_start")
            opened, open_lines, open_tokens = True, 0, 0
        if opened:
            open_lines += 1
            open_tokens += len(line.tokens)
        if line.paragraph_end:
            if not opened:
                malformed.append(f"{line.page}:{line.locus}:end_without_start")
            else:
                lengths_lines.append(open_lines)
                lengths_tokens.append(open_tokens)
            opened = False
    if opened:
        malformed.append(f"{current_page}:unclosed")

    return {
        "running_lines": len(running),
        "paragraph_starts": len(starts),
        "paragraph_ends": len(ends),
        "paragraph_length_lines": {
            "median": statistics.median(lengths_lines) if lengths_lines else None,
            "mean": statistics.mean(lengths_lines) if lengths_lines else None,
            "min": min(lengths_lines) if lengths_lines else None,
            "max": max(lengths_lines) if lengths_lines else None,
        },
        "paragraph_length_tokens": {
            "median": statistics.median(lengths_tokens) if lengths_tokens else None,
            "mean": statistics.mean(lengths_tokens) if lengths_tokens else None,
            "min": min(lengths_tokens) if lengths_tokens else None,
            "max": max(lengths_tokens) if lengths_tokens else None,
        },
        "malformed_paragraph_sequences": malformed,
        "direct_gallows_at_first_token": {
            "paragraph_start": {"count": start_g, "total": len(starts), "rate": rate(start_g, len(starts))},
            "other_running_line": {"count": other_g, "total": len(nonstarts), "rate": rate(other_g, len(nonstarts))},
            "odds_ratio": odds_ratio(start_g, len(starts) - start_g, other_g, len(nonstarts) - other_g),
        },
        "bench_gallows_inside_first_token": {
            "paragraph_start": {"count": start_bench, "total": len(starts), "rate": rate(start_bench, len(starts))},
            "other_running_line": {"count": other_bench, "total": len(nonstarts), "rate": rate(other_bench, len(nonstarts))},
            "odds_ratio": odds_ratio(start_bench, len(starts) - start_bench, other_bench, len(nonstarts) - other_bench),
        },
        "terminal_m_at_physical_line_end": {
            "paragraph_end": {"count": end_m, "total": len(ends), "rate": rate(end_m, len(ends))},
            "other_running_line": {"count": other_m, "total": len(nonends), "rate": rate(other_m, len(nonends))},
            "odds_ratio": odds_ratio(end_m, len(ends) - end_m, other_m, len(nonends) - other_m),
        },
        "initial_letter_top20": {
            "paragraph_start": first_start.most_common(20),
            "other_running_line": first_other.most_common(20),
        },
        "final_letter_top20": {
            "paragraph_end": final_start.most_common(20),
            "other_running_line": final_other.most_common(20),
        },
        "terminal_character_profiles": terminal_profiles,
        "by_illustration_section": dict(sorted(by_section.items())),
    }


def quire20_boundary_audit(parsed: dict[str, list[Line]], star_source: Path | None) -> dict | None:
    if star_source is None:
        return None
    source = json.loads(star_source.read_text(encoding="utf-8"))
    star_counts = source["page_star_counts"]
    pages = list(star_counts)
    rows = []
    for page in pages:
        row = {"page": page, "stars": star_counts[page]}
        for name, lines in parsed.items():
            row[f"{name}_paragraph_starts"] = sum(
                x.paragraph_start for x in lines if x.page == page
            )
        rows.append(row)
    totals = {
        "pages": len(rows),
        "stars": sum(row["stars"] for row in rows),
    }
    for name in parsed:
        n = sum(row[f"{name}_paragraph_starts"] for row in rows)
        totals[f"{name}_paragraph_starts"] = n
        totals[f"stars_minus_{name}"] = totals["stars"] - n
    return {
        "status": "DESCRIPTIVE_STAR_VS_TRANSCRIBER_BOUNDARY_AUDIT",
        "source": source["source"],
        "source_sha256": sha256(star_source),
        "totals": totals,
        "pages": rows,
        "interpretation_limit": (
            "A star/paragraph count mismatch does not identify the unit's meaning; "
            "it shows that marginal stars and visually inferred paragraph gaps cannot "
            "be assumed to be the same segmentation layer."
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zl", type=Path, required=True)
    ap.add_argument("--it", type=Path, required=True)
    ap.add_argument("--gc", type=Path, required=True)
    ap.add_argument("--rf", type=Path, required=True)
    ap.add_argument("--quire20-stars", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    parsed = {name: parse_ivtff(path) for name, path in {"ZL3b": args.zl, "IT2a": args.it, "GC2a": args.gc, "RF1b": args.rf}.items()}
    result = {
        "status": "EXPLORATORY_TRANSCRIBER_BOUNDARY_SCAN_NOT_IMAGE_GROUND_TRUTH",
        "sources": {
            "ZL3b": {"path": str(args.zl), "sha256": sha256(args.zl)},
            "IT2a": {"path": str(args.it), "sha256": sha256(args.it)},
            "GC2a": {"path": str(args.gc), "sha256": sha256(args.gc)},
            "RF1b": {"path": str(args.rf), "sha256": sha256(args.rf)},
        },
        "boundary_counts": {
            name: {
                "starts": sum(x.paragraph_start for x in lines),
                "ends": sum(x.paragraph_end for x in lines),
            }
            for name, lines in parsed.items()
        },
        "boundary_agreement": {
            "ZL3b_vs_IT2a_start": boundary_agreement(parsed["ZL3b"], parsed["IT2a"], "paragraph_start"),
            "ZL3b_vs_IT2a_end": boundary_agreement(parsed["ZL3b"], parsed["IT2a"], "paragraph_end"),
            "ZL3b_vs_GC2a_start": boundary_agreement(parsed["ZL3b"], parsed["GC2a"], "paragraph_start"),
            "ZL3b_vs_GC2a_end": boundary_agreement(parsed["ZL3b"], parsed["GC2a"], "paragraph_end"),
        },
        "zl3b_eva_description": summarize_eva(parsed["ZL3b"]),
        "it2a_eva_sensitivity": summarize_eva(parsed["IT2a"]),
        "quire20_star_boundary_audit": quire20_boundary_audit(parsed, args.quire20_stars),
        "interpretation_limits": [
            "Paragraph markers are transcriber decisions, not image-grounded truth.",
            "A gallows association does not identify a phonetic value.",
            "A paragraph-final glyph association must be separated from generic physical-line-final allography.",
            "GC2a uses v101 and contributes boundary agreement only; its glyph strings are not pooled with EVA.",
            "RF1b has no retained paragraph markers and cannot contribute to boundary agreement.",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
