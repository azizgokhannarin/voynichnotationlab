#!/usr/bin/env python3
"""
Compare atomic EVA and analytical/composite representations on RF1b-EVA.

This script implements the core page-held-out n-gram comparison used in v1.1.
It intentionally uses only a high-confidence basic-EVA subset and excludes tokens
with uncertain/high-ASCII readings.

Usage:
    python scripts/compare_atomic_vs_decomposed.py RF1b-e.txt

No external packages are required for the n-gram section.
The gallows discriminative logistic-regression probe described in the report is
kept separate because it requires scikit-learn.
"""
from __future__ import annotations
import argparse, collections, hashlib, math, re
from pathlib import Path

AAA = {
    "q":["g0"], "o":["o0"], "d":["d0"], "y":["y0"],
    "s":["c0",":t0"], "l":["e0"], "r":["i0",":t0"],
    "ch":["c2",":c1"], "sh":["c2",":v3",":c1"],
    "t":["q2",":p1"], "p":["q2",":x1"],
    "k":["l2",":p1"], "f":["l2",":x1"],
    "cth":["c2",":q3",":p3",":c1"],
    "cph":["c2",":q3",":x1",":c1"],
    "ckh":["c2",":l3",":p3",":c1"],
    "cfh":["c2",":l3",":x1",":c1"],
    "i":["i0"], "n":["i0",":b0"], "m":["i2",":j1"],
    "g":["c2",":j1"], "a":["a0"], "e":["c0"],
    "j":["d4"], "x":["e4"], "v":["a5"],
    "b":["c0",":b0"], "u":["a0",":b0"],
    "c":["c2"], "h":["c1"],
    "cphh":["c2",":q3",":x1",":c3",":c1"],
    "cfhh":["c2",":l3",":x1",":c3",":c1"],
    "ckhh":["c2",":l3",":p3",":c3",":c1"],
    "cthh":["c2",":q3",":p3",":c3",":c1"],
}
MULTI = sorted(AAA, key=len, reverse=True)
NORMAL = {"k","t","p","f"}
PED = {"ckh":"k","cth":"t","cph":"p","cfh":"f"}
CODE = {"k":(0,0),"t":(1,0),"p":(1,1),"f":(0,1)}

PAGE = re.compile(r"^<([^>.]+)>")
DATA = re.compile(r"^<([^>]+)>\s*(.*)$")

def glyphize(t):
    out=[]; i=0
    while i < len(t):
        for g in MULTI:
            if t.startswith(g,i):
                out.append(g); i += len(g); break
        else:
            return None
    return out

def clean_token(t):
    if any(x in t for x in ("@","?","'")) or any(c.isdigit() for c in t):
        return None
    t=t.replace("{","").replace("}","")
    return t if re.fullmatch(r"[a-z]+",t) else None

def load(path):
    page=None; rows=[]
    for raw in path.read_text(encoding="utf-8",errors="replace").splitlines():
        pm=PAGE.match(raw)
        if pm and "<!" in raw:
            page=pm.group(1); continue
        m=DATA.match(raw)
        if not m or m.group(2).startswith("<!"): continue
        body=m.group(2).replace("<->",".")
        for rt in re.split(r"[.\s,]+",body):
            if not rt: continue
            t=clean_token(rt)
            if not t: continue
            gs=glyphize(t)
            if gs:
                fold=int(hashlib.md5(page.encode()).hexdigest(),16)%5
                rows.append((page,fold,gs))
    return rows

def atomic(gs):
    return ["A:"+g for g in gs]

def analytical(gs):
    out=[]
    for g in gs:
        out.extend("S:"+x for x in AAA[g])
    return out

def factor(gs):
    out=[]
    for g in gs:
        if g in NORMAL:
            a,b=CODE[g]
            out += [f"G1:{a}",f"G2:{b}"]
        elif g in PED:
            a,b=CODE[PED[g]]
            out += ["GP:C2",f"GP1:{a}",f"GP2:{b}","GP:C1"]
        else:
            out.append("A:"+g)
    return out

def train(seqs,order):
    counts=[collections.Counter() for _ in range(order+1)]
    totals=[collections.Counter() for _ in range(order+1)]
    vocab={"<EOS>"}
    for seq in seqs:
        vocab.update(seq)
        ext=["<BOS>"]*order+seq+["<EOS>"]
        for pos in range(order,len(ext)):
            sym=ext[pos]
            for k in range(order+1):
                ctx=tuple(ext[pos-k:pos]) if k else ()
                counts[k][ctx,sym]+=1; totals[k][ctx]+=1
    return counts,totals,vocab

def bits(model,seq,order,alpha=.1):
    counts,totals,vocab=model; V=len(vocab)+1
    ext=["<BOS>"]*order+seq+["<EOS>"]; out=0.0
    for pos in range(order,len(ext)):
        sym=ext[pos]
        for k in range(order,-1,-1):
            ctx=tuple(ext[pos-k:pos]) if k else ()
            n=totals[k].get(ctx,0)
            if n or k==0:
                c=counts[k].get((ctx,sym),0)
                p=(c+alpha)/(n+alpha*V)
                out -= math.log2(p); break
    return out

def cv(rows,rep,order,alpha=.1):
    vals=[]
    for f in range(5):
        tr=[rep(gs) for _,ff,gs in rows if ff!=f]
        te=[(rep(gs),len(gs)) for _,ff,gs in rows if ff==f]
        model=train(tr,order)
        B=sum(bits(model,s,order,alpha) for s,_ in te)
        G=sum(n for _,n in te)
        vals.append(B/G)
    return sum(vals)/len(vals)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("rf1b",type=Path)
    args=ap.parse_args()
    rows=load(args.rf1b)
    print("usable_tokens",len(rows))
    print("order\tatomic\tgallows_factor\tanalytical")
    for order in range(5):
        print(order,
              f"{cv(rows,atomic,order):.6f}",
              f"{cv(rows,factor,order):.6f}",
              f"{cv(rows,analytical,order):.6f}",
              sep="\t")

if __name__=="__main__":
    main()
