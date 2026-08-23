#!/usr/bin/env python3
"""
Analyze a selected STA code by physical bifolio layer within an IVTFF quire.

Example:
    python scripts/analyze_bifolio_gradient.py RF1b.txt --quire A --code D1

The script uses page metadata $Q (quire) and $B (bifolio index).
It reports counts/rates by bifolio layer. P-values are intentionally omitted:
glyph observations are locally dependent, so unit-level Bernoulli tests are
not confirmatory.
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

STA_RE = re.compile(r"[A-Z][0-9a-z]")
PAGE_RE = re.compile(r"^<([^>.]+)>")
VAR_RE = re.compile(r"\$([A-Z])=([^\s>]+)")

def parse(path: Path):
    meta = {}
    current_page = None
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("<") and "<!" in line:
            m = PAGE_RE.match(line)
            if not m:
                continue
            current_page = m.group(1)
            meta = dict(VAR_RE.findall(line))
            continue

        if current_page and line.startswith("<") and ">" in line:
            body = line.split(">", 1)[1]
            yield current_page, meta, STA_RE.findall(body)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ivtff", type=Path)
    ap.add_argument("--quire", required=True, help="IVTFF $Q value, e.g. A")
    ap.add_argument("--code", default="D1", help="STA code, default D1")
    args = ap.parse_args()

    by_b = defaultdict(lambda: {"units": 0, "hits": 0, "pages": set()})

    for page, meta, codes in parse(args.ivtff):
        if meta.get("Q") != args.quire:
            continue
        b = meta.get("B")
        if not b:
            continue
        rec = by_b[b]
        rec["units"] += len(codes)
        rec["hits"] += sum(c == args.code for c in codes)
        rec["pages"].add(page)

    print("bifolio\tpages\tunits\thits\trate")
    def key(x):
        try:
            return int(x)
        except ValueError:
            return x
    for b in sorted(by_b, key=key):
        r = by_b[b]
        rate = r["hits"] / r["units"] if r["units"] else 0
        print(
            f"{b}\t{','.join(sorted(r['pages']))}\t"
            f"{r['units']}\t{r['hits']}\t{rate:.6f}"
        )

if __name__ == "__main__":
    main()
