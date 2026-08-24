#!/usr/bin/env python3
"""Scan RF1b/STA IVTFF for first appearances of STA codes."""
from __future__ import annotations
import argparse, re
from collections import Counter
from pathlib import Path

STA_RE = re.compile(r"[A-Z][0-9a-z]")
PAGE_RE = re.compile(r"^<([^>.]+)>")
LOCUS_RE = re.compile(r"^<([^>]+)>")

def parse(path: Path):
    page = None
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("<") and "<!" in line:
            m = PAGE_RE.match(line)
            if m:
                page = m.group(1)
            continue
        if not line.startswith("<"):
            continue
        m = LOCUS_RE.match(line)
        if not m:
            continue
        locus = m.group(1).split(",", 1)[0]
        body = line.split(">", 1)[1]
        yield page, locus, STA_RE.findall(body)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rf1b", type=Path)
    ap.add_argument("--baseline-pages", nargs="+", default=["f1r", "f1v"])
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()

    rows = list(parse(args.rf1b))
    baseline, counts = set(), Counter()
    for page, locus, codes in rows:
        counts.update(codes)
        if page in args.baseline_pages:
            baseline.update(codes)

    seen = set(baseline)
    print("Baseline pages:", ", ".join(args.baseline_pages))
    print("Distinct baseline STA codes:", len(baseline))
    print("page\tlocus\tSTA\tcorpus_count")
    emitted = 0
    for page, locus, codes in rows:
        if page in args.baseline_pages:
            continue
        for code in codes:
            if code not in seen:
                print(f"{page}\t{locus}\t{code}\t{counts[code]}")
                seen.add(code)
                emitted += 1
                if emitted >= args.limit:
                    return

if __name__ == "__main__":
    main()
