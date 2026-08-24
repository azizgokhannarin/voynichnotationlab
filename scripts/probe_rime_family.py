#!/usr/bin/env python3
"""Find replaceable-onset families sharing the same remainder/rime in RF1b-EVA."""
from __future__ import annotations
import argparse, re
from collections import Counter, defaultdict
from pathlib import Path

DATA_RE = re.compile(r'^<([^>]+)>\s*(.*)$')
PAGE_RE = re.compile(r'^<([^>.]+)>\s*<!')

def tokens(path):
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if PAGE_RE.match(raw):
            continue
        m = DATA_RE.match(raw)
        if not m or m.group(2).startswith("<!"):
            continue
        body = re.sub(r'@\d+;', '', m.group(2)).replace("<->", ".")
        for tok in re.split(r'[.\s,]+', body):
            tok = re.sub(r'[^a-z]', '', tok)
            if tok:
                yield tok

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ivtff", type=Path)
    ap.add_argument("--rime", default="aiin")
    args = ap.parse_args()

    c = Counter(tokens(args.ivtff))
    print("bare", args.rime, c[args.rime])
    hits = []
    for tok,n in c.items():
        if tok.endswith(args.rime) and tok != args.rime:
            prefix = tok[:-len(args.rime)]
            hits.append((n,prefix,tok))
    for n,prefix,tok in sorted(hits, reverse=True):
        print(n, prefix, tok)

if __name__ == "__main__":
    main()
