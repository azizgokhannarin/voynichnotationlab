#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
import hashlib, random

MASTER_SEED=20260825
VERSION="C2-CAL-PROD-v1"

def production_seed(branch):
    return int.from_bytes(hashlib.sha256(f"C2|calibration-production-v1|{branch}|{MASTER_SEED}".encode()).digest()[:8],"big")

def invented_alphabet(n=37): return [f"X{i:02d}" for i in range(n)]

def allocate_aliases(train_tokens, source_size=37):
    freq=Counter(u for t in train_tokens for u in t)
    classes=sorted(freq,key=lambda u:(-freq[u],u))
    if not classes: raise ValueError("empty calibration train")
    if len(classes)>source_size: raise ValueError("target inventory exceeds source inventory")
    groups={c:[] for c in classes}
    src=invented_alphabet(source_size)
    # one guaranteed alias per observed class
    for c,x in zip(classes,src[:len(classes)]): groups[c].append(x)
    remaining=src[len(classes):]
    # assign extra aliases only when that class has enough occurrences to activate them in TRAIN
    for x in remaining:
        eligible=[c for c in classes if freq[c] > len(groups[c])]
        if not eligible: raise ValueError("insufficient occurrences to activate 37 aliases")
        # Prefer high-frequency classes while balancing alias load/frequency.
        c=min(eligible,key=lambda u:(len(groups[u])/freq[u],-freq[u],u))
        groups[c].append(x)
    return groups

def encode_with_aliases(tokens,groups,state=None):
    counts=Counter() if state is None else state
    out=[]
    for t in tokens:
        row=[]
        for u in t:
            if u not in groups: raise ValueError(f"class unseen in calibration TRAIN: {u}")
            arr=groups[u];row.append(arr[counts[u]%len(arr)]);counts[u]+=1
        out.append(row)
    return out,counts

def build_positive(train_tokens,val_tokens,source_size=37):
    groups=allocate_aliases(train_tokens,source_size)
    tr,state=encode_with_aliases(train_tokens,groups)
    va,_=encode_with_aliases(val_tokens,groups,state)
    active=set(x for t in tr for x in t)
    if len(active)!=source_size: raise AssertionError((len(active),source_size))
    return tr,va,groups

def build_negative(train_tokens,val_tokens,branch):
    all_tokens=[list(t) for t in train_tokens+val_tokens]
    lengths=[len(t) for t in all_tokens]
    pool=[u for t in all_tokens for u in t]
    rng=random.Random(int.from_bytes(hashlib.sha256(f"{VERSION}|NEG|{branch}|{MASTER_SEED}".encode()).digest()[:8],"big"))
    rng.shuffle(pool)
    out=[];p=0
    for n in lengths: out.append(pool[p:p+n]);p+=n
    cut=len(train_tokens)
    # deterministic rotations until validation source inventory is a subset of train source inventory.
    for _ in range(len(pool)+1):
        tr,va=out[:cut],out[cut:]
        if set(x for t in va for x in t) <= set(x for t in tr for x in t): return tr,va
        pool=pool[1:]+pool[:1];out=[];p=0
        for n in lengths:out.append(pool[p:p+n]);p+=n
    raise RuntimeError("could not produce train-covered negative")

def lengths(ts): return [len(t) for t in ts]
def counts(ts):
    c=Counter()
    for t in ts:c.update(t)
    return c
