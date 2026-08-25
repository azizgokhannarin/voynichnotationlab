#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter, defaultdict
from itertools import product
import hashlib, json, math

BOS="<BOS>"; EOS="<EOS>"; UNK="<UNK>"

@dataclass(frozen=True)
class SearchConfig:
    alpha: float=0.25
    beam_width: int=256
    max_null: int=2
    lambda_complexity: float=0.015
    null_cost: float=2.0
    merge_cost: float=0.5

CONFIG=SearchConfig()

class NGramLM:
    def __init__(self,alpha=.25):
        self.alpha=alpha; self.rows=defaultdict(Counter); self.totals=Counter(); self.vocab=set()
    def fit(self,seqs):
        for seq in seqs:
            seq=list(seq); self.vocab.update(seq)
            x=[BOS,BOS]+seq+[EOS]
            for i in range(2,len(x)):
                ctx=(x[i-2],x[i-1]); y=x[i]
                self.rows[ctx][y]+=1; self.totals[ctx]+=1
        self.vocab.update({EOS,UNK}); return self
    def neglog2(self,seqs):
        V=max(1,len(self.vocab)); loss=0.0; emitted=0
        for seq in seqs:
            seq=list(seq); emitted+=len(seq); x=[BOS,BOS]+seq+[EOS]
            for i in range(2,len(x)):
                ctx=(x[i-2],x[i-1]); y=x[i]
                p=(self.rows[ctx].get(y,0)+self.alpha)/(self.totals.get(ctx,0)+self.alpha*V)
                loss-=math.log2(p)
        return (math.inf,0) if emitted==0 else (loss/emitted,emitted)

def complexity(m,cfg=CONFIG):
    nulls=sum(v is None for v in m.values())
    if nulls>cfg.max_null: return math.inf
    n=Counter(v for v in m.values() if v is not None)
    merges=sum(max(0,k-1) for k in n.values())
    return cfg.null_cost*nulls + cfg.merge_cost*merges

def mapping_key(m):
    return tuple(sorted((k,"" if v is None else v) for k,v in m.items()))

def mapping_sha256(m):
    b=json.dumps(mapping_key(m),ensure_ascii=False,separators=(",",":")).encode()
    return hashlib.sha256(b).hexdigest()

def map_tokens(stream,m,unknown_to_unk=False):
    out=[]
    for p in stream:
        for line in p["lines"]:
            for t in line["tokens"]:
                seq=[]
                for u in t["units"]:
                    if u in m:
                        if m[u] is not None: seq.append(m[u])
                    elif unknown_to_unk: seq.append(UNK)
                    else: raise KeyError(u)
                out.append(seq)
    return out

def objective(lm,stream,m,cfg=CONFIG,unknown_to_unk=False):
    H,n=lm.neglog2(map_tokens(stream,m,unknown_to_unk))
    C=complexity(m,cfg)
    return H+cfg.lambda_complexity*C,H,C,n

def source_order(train):
    f=Counter()
    for p in train:
        for line in p["lines"]:
            for t in line["tokens"]: f.update(t["units"])
    return sorted(f,key=lambda u:(-f[u],u))

def beam_search(train,val,lm,target_inventory,cfg=CONFIG):
    units=source_order(train); targets=tuple(sorted(target_inventory)); beam=[{}]
    for u in units:
        cand=[]
        for m in beam:
            vals=list(targets)
            if sum(v is None for v in m.values())<cfg.max_null: vals.append(None)
            for v in vals:
                x=dict(m); x[u]=v
                J,_,_,_=objective(lm,train,x,cfg,True)
                cand.append((J,mapping_key(x),x))
        cand.sort(key=lambda z:(z[0],z[1]))
        beam=[x for _,_,x in cand[:cfg.beam_width]]
    finals=[]
    for m in beam:
        J,H,C,n=objective(lm,val,m,cfg,False)
        finals.append((J,mapping_key(m),H,C,n,m))
    finals.sort(key=lambda z:(z[0],z[1]))
    J,_,H,C,n,m=finals[0]
    tJ,tH,_,tn=objective(lm,train,m,cfg,False)
    return {"mapping":m,"mapping_sha256":mapping_sha256(m),
            "validation_objective":J,"validation_loss":H,"complexity":C,
            "validation_emitted_symbols":n,"train_loss":tH,
            "train_emitted_symbols":tn,"beam_survivors":len(finals),"unit_order":units}

def exhaustive_search(train,val,lm,target_inventory,cfg=CONFIG):
    units=source_order(train); vals=list(sorted(target_inventory))+[None]
    best=None
    for assignment in product(vals,repeat=len(units)):
        m=dict(zip(units,assignment))
        if sum(v is None for v in assignment)>cfg.max_null: continue
        J,H,C,n=objective(lm,val,m,cfg,False)
        row=(J,mapping_key(m),H,C,n,m)
        if best is None or (row[0],row[1])<(best[0],best[1]): best=row
    J,_,H,C,n,m=best
    return {"mapping":m,"mapping_sha256":mapping_sha256(m),
            "validation_objective":J,"validation_loss":H,"complexity":C,
            "validation_emitted_symbols":n}

class FinalTestGuard:
    def __init__(self): self._hash=None
    def freeze(self,m):
        self._hash=mapping_sha256(m); return self._hash
    def score_final(self,lm,stream,m,cfg=CONFIG):
        if self._hash is None: raise RuntimeError("mapping not frozen")
        if mapping_sha256(m)!=self._hash: raise RuntimeError("mapping changed")
        return objective(lm,stream,m,cfg,False)
