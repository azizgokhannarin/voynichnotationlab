#!/usr/bin/env python3
from __future__ import annotations
import numpy as np, math, random, hashlib
from collections import Counter,defaultdict

BOS=-1
EOS=-2

class DenseTrigramLM:
    def __init__(self,target_units,alpha=0.25):
        self.units=tuple(sorted(target_units))
        self.idx={u:i for i,u in enumerate(self.units)}
        self.K=len(self.units)
        self.BOS=self.K
        self.EOS=self.K+1
        self.alpha=alpha
        self.logp=None
    def fit(self,tokens):
        K2=self.K+2
        counts=np.zeros((K2,K2,K2),dtype=np.float64)
        totals=np.zeros((K2,K2),dtype=np.float64)
        for tok in tokens:
            seq=[self.BOS,self.BOS]+[self.idx[u] for u in tok if u in self.idx]+[self.EOS]
            for a,b,c in zip(seq,seq[1:],seq[2:]):
                counts[a,b,c]+=1; totals[a,b]+=1
        V=self.K+1 # target symbols + EOS, BOS not emitted
        probs=(counts+self.alpha)/(totals[:,:,None]+self.alpha*V)
        # BOS should never be emitted; keep finite but unused
        self.logp=np.log2(probs)
        return self

def source_ngram_table(tokens,source_units,lm):
    sidx={u:i for i,u in enumerate(source_units)}
    C=Counter()
    for tok in tokens:
        seq=[lm.BOS,lm.BOS]+[sidx[u] for u in tok]+[lm.EOS]
        for a,b,c in zip(seq,seq[1:],seq[2:]): C[(a,b,c)]+=1
    pats=np.array(list(C.keys()),dtype=np.int16)
    cnt=np.array(list(C.values()),dtype=np.float64)
    affected=[[] for _ in source_units]
    for j,row in enumerate(pats):
        for x in set(int(v) for v in row if v>=0 and v<len(source_units)):
            affected[x].append(j)
    affected=[np.asarray(x,dtype=np.int32) for x in affected]
    return pats,cnt,affected

def mapped_rows(pats,key,lm):
    out=pats.astype(np.int32,copy=True)
    S=len(key)
    for col in range(3):
        x=out[:,col]
        mask=(x>=0)&(x<S)
        x[mask]=key[x[mask]]
        x[x==BOS]=lm.BOS
        x[x==EOS]=lm.EOS
        out[:,col]=x
    return out

def total_score(pats,cnt,key,lm):
    m=mapped_rows(pats,key,lm)
    return float(np.sum(cnt*lm.logp[m[:,0],m[:,1],m[:,2]]))

def score_rows(pats,cnt,key,lm,rows):
    if len(rows)==0:return 0.0
    p=pats[rows]
    m=mapped_rows(p,key,lm)
    return float(np.sum(cnt[rows]*lm.logp[m[:,0],m[:,1],m[:,2]]))

def random_key(S,K,max_mult,rng):
    # Guarantee all S assigned with cap max_mult.
    slots=[t for t in range(K) for _ in range(max_mult)]
    if len(slots)<S: raise ValueError("capacity impossible")
    rng.shuffle(slots)
    return np.asarray(slots[:S],dtype=np.int16)

def stochastic_search(tokens,source_units,lm,restarts=20,iterations=20000,max_mult=3,
                      seed=20260825,initial_keys=None,temp0=10.0,temp_end=0.05):
    pats,cnt,affected=source_ngram_table(tokens,source_units,lm)
    S=len(source_units);K=lm.K
    master=random.Random(seed)
    best_score=-1e300;best_key=None
    starts=list(initial_keys or [])
    while len(starts)<restarts:
        starts.append(random_key(S,K,max_mult,master))
    trace=[]
    for rr in range(restarts):
        rng=random.Random(master.randrange(1<<63))
        key=np.array(starts[rr],dtype=np.int16,copy=True)
        mult=np.bincount(key,minlength=K)
        score=total_score(pats,cnt,key,lm)
        local_best=score; local_key=key.copy()
        for it in range(iterations):
            frac=it/max(1,iterations-1)
            temp=temp0*((temp_end/temp0)**frac)
            if rng.random()<0.35:
                # swap labels of two source units: always capacity-safe
                a,b=rng.sample(range(S),2)
                if key[a]==key[b]:continue
                rows=np.union1d(affected[a],affected[b])
                old=score_rows(pats,cnt,key,lm,rows)
                key[a],key[b]=key[b],key[a]
                new=score_rows(pats,cnt,key,lm,rows)
                delta=new-old
                if delta>=0 or rng.random()<math.exp(delta/max(temp,1e-12)):
                    score+=delta
                else:
                    key[a],key[b]=key[b],key[a]
            else:
                a=rng.randrange(S); oldt=int(key[a])
                candidates=[t for t in range(K) if t!=oldt and mult[t]<max_mult]
                if not candidates:continue
                newt=rng.choice(candidates)
                rows=affected[a]
                old=score_rows(pats,cnt,key,lm,rows)
                key[a]=newt
                new=score_rows(pats,cnt,key,lm,rows)
                delta=new-old
                if delta>=0 or rng.random()<math.exp(delta/max(temp,1e-12)):
                    mult[oldt]-=1;mult[newt]+=1;score+=delta
                else:key[a]=oldt
            if score>local_best:
                local_best=score;local_key=key.copy()
        if local_best>best_score:
            best_score=local_best;best_key=local_key.copy()
        trace.append(local_best)
    return {"key":best_key,"score":best_score,"trace":trace,
            "bits_per_trigram_event":-best_score/float(cnt.sum())}

def key_mapping(source_units,key,lm):
    return {s:lm.units[int(t)] for s,t in zip(source_units,key)}

def key_sha256(mapping):
    x=repr(sorted(mapping.items())).encode()
    return hashlib.sha256(x).hexdigest()

def decode_tokens(tokens,mapping):
    return [tuple(mapping[u] for u in t) for t in tokens]
