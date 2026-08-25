#!/usr/bin/env python3
"""
Frozen Campaign-1 null generators.

Data model:
[
  {
    "page": "f1r",
    "lines": [
      [["QO","k","e","y"], ["DA","i","n"]],
      ...
    ]
  },
  ...
]

Each token is a list of frozen structural units.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter, defaultdict
import hashlib
import random
from typing import Iterable

MASTER_SEED = 20260825
VERSION = "C1-NULL-v1"

def derive_seed(null_id: str, replicate: int) -> int:
    key=f"{VERSION}|{null_id}|{replicate}|{MASTER_SEED}".encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8],"big")

def clone_stream(stream):
    return [
        {"page": p["page"],
         "lines": [[list(tok) for tok in line] for line in p["lines"]]}
        for p in stream
    ]

def iter_tokens(stream):
    for page in stream:
        for line in page["lines"]:
            for tok in line:
                yield tok

def inventory(stream):
    c=Counter()
    for tok in iter_tokens(stream):
        c.update(tok)
    return c

def token_length_vector(stream):
    return [len(t) for t in iter_tokens(stream)]

def null_a_within_token_shuffle(stream, replicate: int):
    rng=random.Random(derive_seed("A",replicate))
    out=clone_stream(stream)
    for tok in iter_tokens(out):
        rng.shuffle(tok)
    return out

def null_b_line_token_shuffle(stream, replicate: int):
    rng=random.Random(derive_seed("B",replicate))
    out=clone_stream(stream)
    for page in out:
        for line in page["lines"]:
            rng.shuffle(line)
    return out

@dataclass
class MarkovModel:
    starts: Counter
    transitions: dict
    global_units: Counter
    alpha: float = 0.5

def fit_markov(train_stream, alpha: float=0.5):
    starts=Counter()
    transitions=defaultdict(Counter)
    global_units=Counter()
    for tok in iter_tokens(train_stream):
        if not tok:
            continue
        starts[tok[0]] += 1
        global_units.update(tok)
        for a,b in zip(tok,tok[1:]):
            transitions[a][b] += 1
    return MarkovModel(starts,dict(transitions),global_units,alpha)

def _sample_counter(counter: Counter, rng: random.Random):
    if not counter:
        raise ValueError("empty sampling distribution")
    items=list(counter)
    weights=[counter[x] for x in items]
    return rng.choices(items,weights=weights,k=1)[0]

def _sample_smoothed_next(prev, model: MarkovModel, rng: random.Random):
    inv=list(model.global_units)
    row=model.transitions.get(prev,Counter())
    if not row:
        return _sample_counter(model.global_units,rng)
    weights=[row.get(u,0)+model.alpha for u in inv]
    return rng.choices(inv,weights=weights,k=1)[0]

def null_c_matched_synthetic(layout_stream, train_stream, replicate: int):
    """
    Train model on train_stream; generate new tokens in layout_stream while
    preserving each token's observed length and the page/line skeleton.
    """
    rng=random.Random(derive_seed("C",replicate))
    model=fit_markov(train_stream,0.5)
    if not model.global_units:
        raise ValueError("empty train inventory")
    out=clone_stream(layout_stream)
    for tok in iter_tokens(out):
        n=len(tok)
        if n==0:
            continue
        first=_sample_counter(model.starts or model.global_units,rng)
        new=[first]
        while len(new)<n:
            new.append(_sample_smoothed_next(new[-1],model,rng))
        tok[:] = new
    return out

def null_d_label_permutation(stream, replicate: int):
    rng=random.Random(derive_seed("D",replicate))
    units=sorted(inventory(stream))
    shuffled=units[:]
    rng.shuffle(shuffled)
    mapping=dict(zip(units,shuffled))
    out=clone_stream(stream)
    for tok in iter_tokens(out):
        tok[:] = [mapping[u] for u in tok]
    return out,mapping

# ---------- invariant checks ----------

def structure_shape(stream):
    return [
        (p["page"], [len(line) for line in p["lines"]])
        for p in stream
    ]

def assert_null_a(original,out):
    assert structure_shape(original)==structure_shape(out)
    assert token_length_vector(original)==token_length_vector(out)
    assert inventory(original)==inventory(out)

def assert_null_b(original,out):
    assert structure_shape(original)==structure_shape(out)
    for p0,p1 in zip(original,out):
        for l0,l1 in zip(p0["lines"],p1["lines"]):
            assert Counter(tuple(t) for t in l0)==Counter(tuple(t) for t in l1)

def assert_null_c(layout,out,train):
    assert structure_shape(layout)==structure_shape(out)
    assert token_length_vector(layout)==token_length_vector(out)
    allowed=set(inventory(train))
    assert all(u in allowed for t in iter_tokens(out) for u in t)

def assert_null_d(original,out,mapping):
    assert structure_shape(original)==structure_shape(out)
    assert len(mapping)==len(set(mapping.values()))
    inv={v:k for k,v in mapping.items()}
    restored=clone_stream(out)
    for tok in iter_tokens(restored):
        tok[:] = [inv[u] for u in tok]
    assert restored==original
