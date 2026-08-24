#!/usr/bin/env python3
"""Decompose Voynich tokens as STEM + one terminal glyph."""
import argparse,re,collections
from pathlib import Path
TERMINALS=set("nmyrls")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("rf1b",type=Path)
    args=ap.parse_args()
    c=collections.Counter()
    for raw in args.rf1b.read_text(encoding="utf-8",errors="replace").splitlines():
        if raw.startswith("#") or "<!" in raw:continue
        m=re.match(r"^<[^>]+>\s*(.*)$",raw)
        if not m:continue
        body=re.sub(r"@\d+;","",m.group(1))
        for t in re.split(r"[.\s,]+",body):
            t=re.sub(r"[^a-z]","",t)
            if t:c[t]+=1
    fam=collections.defaultdict(collections.Counter)
    for t,n in c.items():
        if len(t)>=2 and t[-1] in TERMINALS:
            fam[t[:-1]][t[-1]]+=n
        else:
            fam[t]["Ø"]+=n
    for stem,ends in sorted(fam.items(),key=lambda kv:-sum(kv[1].values())):
        if len(ends)>=2:
            print(stem, sum(ends.values()), dict(ends))
if __name__=="__main__":
    main()
