#!/usr/bin/env python3
"""
Analyze EVA q/qo frequency by physical bifolio layer from an RF1b EVA IVTFF file.

Example:
    python scripts/analyze_eva_qo_bifolio.py RF1b-e.txt --quire B

Reports:
- EVA letter count
- token count
- q count
- token-initial q
- token-initial qo
- q frequency by $B bifolio index

This script intentionally does not perform confirmatory p-value testing,
because tokens and glyphs are strongly dependent within words/lines/pages.
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

META_RE = re.compile(r"^<([^>.]+)>\s+<!.*?\$Q=([^\s>]+).*?\$B=([^\s>]+)")
LOCUS_RE = re.compile(r"^<([^>]+)>\s+(.*)$")

def clean_body(body: str) -> str:
    body = re.sub(r"@\d+;", "", body)
    body = body.replace("<->", ".")
    body = body.replace("{", "").replace("}", "")
    return body

def tokens(body: str):
    body = clean_body(body)
    return [
        t for t in re.split(r"[.\s,<>;\-]+", body)
        if t and re.search(r"[a-z]", t)
    ]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ivtff", type=Path)
    ap.add_argument("--quire", required=True)
    args = ap.parse_args()

    page = None
    bifolio = None
    in_quire = False

    stats = defaultdict(lambda: {
        "pages": set(), "letters": 0, "tokens": 0,
        "q": 0, "q_start": 0, "qo_start": 0, "q_internal": 0,
    })

    for raw in args.ivtff.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        m = META_RE.match(line)
        if m:
            page, qval, bval = m.groups()
            in_quire = (qval == args.quire)
            bifolio = bval if in_quire else None
            continue

        if not in_quire or bifolio is None:
            continue

        m = LOCUS_RE.match(line)
        if not m:
            continue

        body = clean_body(m.group(2))
        toks = tokens(body)
        rec = stats[bifolio]
        rec["pages"].add(page)
        rec["letters"] += len(re.findall(r"[a-z]", body))
        rec["tokens"] += len(toks)
        rec["q"] += body.count("q")

        for t in toks:
            if "q" in t:
                if t.startswith("q"):
                    rec["q_start"] += 1
                    if t.startswith("qo"):
                        rec["qo_start"] += 1
                else:
                    rec["q_internal"] += t.count("q")

    print("B\tpages\tletters\ttokens\tq\tq/1000letters\tq/100tokens\tq_start\tqo_start\tq_internal")
    for b in sorted(stats, key=lambda x: int(x) if x.isdigit() else x):
        r = stats[b]
        qpl = 1000 * r["q"] / r["letters"] if r["letters"] else 0
        qpt = 100 * r["q"] / r["tokens"] if r["tokens"] else 0
        print(
            f"{b}\t{','.join(sorted(r['pages']))}\t{r['letters']}\t{r['tokens']}\t"
            f"{r['q']}\t{qpl:.4f}\t{qpt:.4f}\t"
            f"{r['q_start']}\t{r['qo_start']}\t{r['q_internal']}"
        )

if __name__ == "__main__":
    main()
