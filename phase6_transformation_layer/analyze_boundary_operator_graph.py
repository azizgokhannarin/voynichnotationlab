#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math, random, statistics
from collections import Counter, defaultdict
from pathlib import Path

def auc(items):
    xs=sorted(items,key=lambda x:x[0])
    pos=sum(y for _,y in xs); neg=len(xs)-pos
    if not pos or not neg: return float("nan")
    ranks=[0.0]*len(xs); i=0
    while i<len(xs):
        j=i+1
        while j<len(xs) and xs[j][0]==xs[i][0]: j+=1
        rank=(i+1+j)/2
        for k in range(i,j): ranks[k]=rank
        i=j
    rsum=sum(r for r,(_,y) in zip(ranks,xs) if y)
    return (rsum-pos*(pos+1)/2)/(pos*neg)

def load(path):
    x=json.loads(Path(path).read_text(encoding="utf-8"))
    if x.get("schema")!="C1-STRUCT-v1": raise ValueError("wrong stream schema")
    return x["pages"]

def split_pages(pages, split):
    return [p for p in pages if p["split"]==split]

def all_tokens(pages,split):
    for p in split_pages(pages,split):
        for line in p["lines"]:
            for t in line["tokens"]:
                yield tuple(t["units"])

def family_edges(pages,split,which):
    tc=Counter(all_tokens(pages,split))
    fam=defaultdict(set)
    examples=defaultdict(list)
    for tok in tc:
        if len(tok)<2: continue
        if which=="FIRST":
            core,val=tok[1:],tok[0]
        else:
            core,val=tok[:-1],tok[-1]
        fam[core].add(val)
    edge=Counter()
    for core,vals in fam.items():
        vals=sorted(vals)
        if len(vals)<2: continue
        for i,a in enumerate(vals):
            for b in vals[i+1:]:
                e=(a,b); edge[e]+=1
                if len(examples[e])<6: examples[e].append(core)
    return edge,examples

def relation(a,b):
    if len(a)!=len(b): return None
    dif=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    if len(dif)!=1: return None
    i=dif[0]
    edge=tuple(sorted((a[i],b[i])))
    if i==0: return ("FIRST",edge)
    if i==len(a)-1: return ("LAST",edge)
    return ("INNER",edge)

def lines_for(pages,split):
    return [[tuple(t["units"]) for t in line["tokens"]]
            for p in split_pages(pages,split) for line in p["lines"]]

def observed_adjacency(lines):
    kinds=Counter(); edges=Counter()
    for toks in lines:
        for a,b in zip(toks,toks[1:]):
            r=relation(a,b)
            if r:
                kinds[r[0]]+=1; edges[r]+=1
    return kinds,edges

def permutation_null(lines,n=300,seed=20260825):
    rng=random.Random(seed)
    kinds={"FIRST":[],"LAST":[],"INNER":[]}
    edges=[]
    for _ in range(n):
        kc=Counter(); ec=Counter()
        for toks in lines:
            a=list(toks); rng.shuffle(a)
            for x,y in zip(a,a[1:]):
                r=relation(x,y)
                if r: kc[r[0]]+=1; ec[r]+=1
        for k in kinds: kinds[k].append(kc[k])
        edges.append(ec)
    return kinds,edges

def heldout_auc(train_edge,val_edge):
    units=sorted({u for e in list(train_edge)+list(val_edge) for u in e})
    pairs=[(units[i],units[j]) for i in range(len(units)) for j in range(i+1,len(units))]
    raw=auc([(train_edge[e], int(val_edge[e]>0)) for e in pairs])
    deg=Counter()
    for (a,b),c in train_edge.items():
        deg[a]+=c; deg[b]+=c
    marginal=auc([(deg[a]*deg[b], int(val_edge[(a,b)]>0)) for a,b in pairs])
    total=sum(train_edge.values())
    lifts=[]
    for a,b in pairs:
        expected=(deg[a]*deg[b])/(2*total) if total else 0
        score=math.log((train_edge[(a,b)]+0.5)/(expected+0.5))
        lifts.append((score,int(val_edge[(a,b)]>0)))
    return raw,marginal,auc(lifts),sum(1 for e in pairs if val_edge[e]>0),len(pairs)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("stream")
    ap.add_argument("--outdir",required=True)
    ap.add_argument("--permutations",type=int,default=300)
    args=ap.parse_args()
    out=Path(args.outdir);out.mkdir(parents=True,exist_ok=True)
    pages=load(args.stream)

    # Explicit guard: this analysis uses train and validation only.
    train_lines=lines_for(pages,"train")
    obs_kind,obs_edge=observed_adjacency(train_lines)
    null_kind,null_edges=permutation_null(train_lines,args.permutations)

    rows=[]
    result={"schema":"TRANSFORM-PROBE-v1","final_test_used":False,
            "permutations":args.permutations,"global_adjacency":{},"heldout":{}}
    for k in ["FIRST","LAST","INNER"]:
        mu=statistics.mean(null_kind[k]); sd=statistics.stdev(null_kind[k])
        result["global_adjacency"][k]={"observed":obs_kind[k],"null_mean":mu,
          "null_sd":sd,"z":(obs_kind[k]-mu)/sd if sd else None}

    for kind in ["FIRST","LAST"]:
        tr,examples=family_edges(pages,"train",kind)
        va,_=family_edges(pages,"validation",kind)
        raw,margin,lift,npos,npairs=heldout_auc(tr,va)
        recurrent=sum(1 for e,c in tr.items() if c>=3 and va[e]>0)
        eligible=sum(1 for e,c in tr.items() if c>=3)
        result["heldout"][kind]={
          "train_edges_core_ge_3":eligible,
          "validation_recurrent":recurrent,
          "transfer_rate":recurrent/eligible if eligible else None,
          "auc_train_pair_support":raw,
          "auc_marginal_frequency_product":margin,
          "auc_pair_specific_lift":lift,
          "validation_positive_pairs":npos,"candidate_pairs":npairs,
          "top10_support_share":sum(c for _,c in tr.most_common(10))/sum(tr.values()),
          "top20_support_share":sum(c for _,c in tr.most_common(20))/sum(tr.values())
        }
        for e,ncore in tr.most_common(40):
            vals=[r[(kind,e)] for r in null_edges]
            mu=statistics.mean(vals); sd=statistics.stdev(vals)
            z=(obs_edge[(kind,e)]-mu)/sd if sd else None
            rows.append({
              "position":kind,"unit_a":e[0],"unit_b":e[1],
              "train_distinct_core_support":ncore,
              "validation_distinct_core_support":va[e],
              "train_adjacent_observed":obs_edge[(kind,e)],
              "train_adjacent_null_mean":mu,
              "train_adjacent_z":z,
              "example_cores":" | ".join("+".join(c) for c in examples[e][:5])
            })

    (out/"operator_probe_summary.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    with (out/"operator_edges_top40.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
