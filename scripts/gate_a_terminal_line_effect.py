#!/usr/bin/env python3
"""Gate-A core: test terminal line-final enrichment conditional on normalized stem."""
import argparse,re,collections,math
from pathlib import Path

TERMS=set("nmyrls")
LABELS=["Ø","l","m","n","r","s","y"]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("rf1b",type=Path)
    args=ap.parse_args()
    lines=[]
    for raw in args.rf1b.read_text(encoding="utf-8",errors="replace").splitlines():
        if "<!" in raw: continue
        m=re.match(r"^<[^>]+>\s*(.*)$",raw)
        if not m: continue
        body=re.sub(r"@\d+;","",m.group(1)).replace("<->",".")
        ts=[]
        for t in re.split(r"[.\s,]+",body):
            t=re.sub(r"[^a-z]","",t)
            if t:ts.append(t)
        if ts:lines.append(ts)

    fam=collections.defaultdict(collections.Counter)
    last=collections.defaultdict(collections.Counter)
    for ts in lines:
        for i,t in enumerate(ts):
            if len(t)>=2 and t[-1] in TERMS:
                stem,end=t[:-1],t[-1]
            else:
                stem,end=t,"Ø"
            fam[stem][end]+=1
            if i==len(ts)-1:last[stem][end]+=1

    for e in LABELS:
        obs=exp=var=0.
        for stem,c in fam.items():
            N=sum(c.values());K=sum(last[stem].values());M=c[e]
            if M and K and N>1:
                obs+=last[stem][e]
                exp+=M*K/N
                var+=K*(M/N)*(1-M/N)*((N-K)/(N-1))
        z=(obs-exp)/math.sqrt(var) if var else float("nan")
        print(e, "observed",obs,"expected",round(exp,2),"z",round(z,2))

if __name__=="__main__":
    main()
