#!/usr/bin/env python3
"""Analyze EVA q/qo by physical bifolio with $Q/$B/$L/$H controls."""
from __future__ import annotations
import argparse, re
from collections import defaultdict
from pathlib import Path

PAGE_RE = re.compile(r'^<([^>.]+)>\s*<!\s*(.*?)>')
VAR_RE = re.compile(r'\$([A-Z])=([^\s>]+)')
DATA_RE = re.compile(r'^<([^>]+)>\s*(.*)$')

def tokens(body: str):
    body = re.sub(r'@\d+;', '', body).replace('<->','.')
    out = []
    for t in re.split(r'[.\s,]+', body):
        t = t.strip().replace('{','').replace('}','')
        if t and re.search(r'[a-z]', t):
            out.append(t)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ivtff", type=Path)
    ap.add_argument("--quires", nargs="*")
    args = ap.parse_args()

    page, meta = None, {}
    s = defaultdict(lambda: {
        "pages":set(),"tokens":0,"q":0,"q_start":0,"qo_start":0,"q_internal":0,
        "L":set(),"H":set(),"I":set()
    })

    for raw in args.ivtff.read_text(encoding="utf-8", errors="replace").splitlines():
        pm = PAGE_RE.match(raw)
        if pm:
            page = pm.group(1)
            meta = dict(VAR_RE.findall(pm.group(2)))
            continue
        if not raw.startswith("<") or page is None:
            continue
        dm = DATA_RE.match(raw)
        if not dm or dm.group(2).startswith("<!"):
            continue

        Q, B = meta.get("Q"), meta.get("B")
        if not Q or not B or (args.quires and Q not in args.quires):
            continue

        ts = tokens(dm.group(2))
        r = s[(Q,B)]
        r["pages"].add(page)
        r["tokens"] += len(ts)
        for f in ("L","H","I"):
            if meta.get(f): r[f].add(meta[f])
        for t in ts:
            n = t.count("q")
            r["q"] += n
            if t.startswith("q"):
                r["q_start"] += 1
                if t.startswith("qo"): r["qo_start"] += 1
                n -= 1
            r["q_internal"] += max(n,0)

    print("Q\tB\tpages\ttokens\tq\tq_start\tqo_start\tqo/100tok\tq_internal\tL\tH\tI")
    def key(k):
        Q,B=k
        try: bi=int(B)
        except ValueError: bi=999
        return Q,bi,B
    for Q,B in sorted(s,key=key):
        r=s[(Q,B)]
        rate=100*r["qo_start"]/r["tokens"] if r["tokens"] else 0
        print(
            f"{Q}\t{B}\t{','.join(sorted(r['pages']))}\t{r['tokens']}\t{r['q']}\t"
            f"{r['q_start']}\t{r['qo_start']}\t{rate:.6f}\t{r['q_internal']}\t"
            f"{','.join(sorted(r['L']))}\t{','.join(sorted(r['H']))}\t"
            f"{','.join(sorted(r['I']))}"
        )

if __name__ == "__main__":
    main()
