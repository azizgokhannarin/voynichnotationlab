#!/usr/bin/env python3
"""Inspect EVA-y terminal families in RF1b-style token lists."""
from collections import Counter
import argparse, re
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("rf1b",type=Path)
    args=ap.parse_args()
    c=Counter()
    for raw in args.rf1b.read_text(encoding="utf-8",errors="replace").splitlines():
        if raw.startswith("#") or "<!" in raw: continue
        m=re.match(r"^<[^>]+>\s*(.*)$",raw)
        if not m: continue
        body=re.sub(r"@\d+;","",m.group(1))
        for t in re.split(r"[.\s,]+",body):
            t=re.sub(r"[^a-z]","",t)
            if t:c[t]+=1
    rows=[]
    for t,n in c.items():
        if len(t)>=2 and t.endswith("y"):
            b=t[:-1]
            rows.append((n,c[b],t,b))
    for n,bn,t,b in sorted(rows,reverse=True):
        if bn:
            print(f"{t}\t{n}\tbase={b}\tbase_count={bn}")
if __name__=="__main__":
    main()
