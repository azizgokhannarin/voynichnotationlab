#!/usr/bin/env python3
"""Report an EVA base glyph's follower and two-glyph positional behavior."""
from __future__ import annotations
import argparse, re
from collections import Counter
from pathlib import Path

PAGE_RE = re.compile(r'^<([^>.]+)>\s*<!')
DATA_RE = re.compile(r'^<([^>]+)>\s*(.*)$')

def parse_tokens(path):
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if PAGE_RE.match(raw):
            continue
        m = DATA_RE.match(raw)
        if not m or m.group(2).startswith("<!"):
            continue
        body = re.sub(r'@\d+;', '', m.group(2)).replace("<->", ".")
        for t in re.split(r'[.\s,]+', body):
            t = re.sub(r'[^a-z]', '', t)
            if t:
                yield t

def classify_bigram(t, bg, pos):
    if len(t) == 2:
        return "whole_token"
    if pos == 0:
        return "token_initial"
    if pos + 2 == len(t):
        return "token_final"
    return "medial"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ivtff", type=Path)
    ap.add_argument("--base", default="d")
    ap.add_argument("--pairs", nargs="+", default=["da","dy"])
    args = ap.parse_args()

    toks = list(parse_tokens(args.ivtff))
    followers = Counter()
    total = 0
    pair_pos = {bg: Counter() for bg in args.pairs}

    for t in toks:
        for i,ch in enumerate(t):
            if ch == args.base:
                total += 1
                followers[t[i+1] if i+1 < len(t) else "<END>"] += 1
        for bg in args.pairs:
            start = 0
            while True:
                j = t.find(bg, start)
                if j < 0: break
                pair_pos[bg][classify_bigram(t,bg,j)] += 1
                start = j + 1

    print("base", args.base, "count", total)
    print("followers")
    for k,v in followers.most_common():
        print(k, v, f"{100*v/total:.3f}%")
    for bg in args.pairs:
        print("\n", bg, dict(pair_pos[bg]))

if __name__ == "__main__":
    main()
