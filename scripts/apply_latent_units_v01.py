#!/usr/bin/env python3
"""Apply Voynich-Notation-Lab latent-unit inventory v0.1 to clean EVA tokens."""
from __future__ import annotations
import argparse, re
from pathlib import Path

MULTI = sorted(["cfhh","cphh","ckhh","cthh","cfh","cph","ckh","cth","ch","sh"],key=len,reverse=True)
MAP = {("q","o"):"QO",("d","a"):"DA",("d","y"):"DY",("ch",):"CH",("sh",):"SH"}
KEYS = sorted(MAP,key=len,reverse=True)

def glyphs(t):
    out=[];i=0
    while i<len(t):
        g=next((m for m in MULTI if t.startswith(m,i)),None)
        if g: out.append(g);i+=len(g)
        else: out.append(t[i]);i+=1
    return out

def latent(gs):
    out=[];i=0
    while i<len(gs):
        for k in KEYS:
            if tuple(gs[i:i+len(k)])==k:
                out.append(MAP[k]);i+=len(k);break
        else:
            out.append(gs[i]);i+=1
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("token",nargs="+")
    args=ap.parse_args()
    for t in args.token:
        print(t,"=>"," | ".join(latent(glyphs(t))))

if __name__=="__main__":
    main()
