#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
import hashlib
import random
from copy import deepcopy

MASTER_SEED = 20260825
VERSION = "C2-v1"

def derive_seed(component: str, branch: str, replicate: int) -> int:
    key=f"{VERSION}|{component}|{branch}|{replicate}|{MASTER_SEED}".encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8],"big")

def clone_stream(stream):
    return deepcopy(stream)

def iter_tokens(stream):
    for page in stream:
        for line in page["lines"]:
            for tok in line["tokens"]:
                yield tok["units"]

def shape_signature(stream):
    return [
        (
            p["page"],
            p["split"],
            [
                (
                    line["line"],
                    [len(tok["units"]) for tok in line["tokens"]]
                )
                for line in p["lines"]
            ]
        )
        for p in stream
    ]

def unit_counts(stream):
    c=Counter()
    for tok in iter_tokens(stream):
        c.update(tok)
    return c

def weak_within_token_shuffle(stream, branch: str, replicate: int):
    """
    Preserve exact page/line/token layout, exact token length at each position,
    and exact corpus-wide unit multiset. Shuffle units only within each token.
    """
    rng=random.Random(derive_seed("weak",branch,replicate))
    out=clone_stream(stream)
    for tok in iter_tokens(out):
        rng.shuffle(tok)
    return out

class SlotModel:
    def __init__(self,single,start,core,terminal):
        self.single=Counter(single)
        self.start=Counter(start)
        self.core=Counter(core)
        self.terminal=Counter(terminal)

def fit_slot_model(train_stream):
    single=Counter()
    start=Counter()
    core=Counter()
    terminal=Counter()
    for tok in iter_tokens(train_stream):
        if not tok:
            continue
        if len(tok)==1:
            single[tok[0]] += 1
        else:
            start[tok[0]] += 1
            terminal[tok[-1]] += 1
            if len(tok)>2:
                core.update(tok[1:-1])
    return SlotModel(single,start,core,terminal)

def _sample_counter(counter, rng):
    if not counter:
        raise ValueError("cannot sample from empty distribution")
    items=list(counter)
    weights=[counter[x] for x in items]
    return rng.choices(items,weights=weights,k=1)[0]

def independent_slot_surrogate(layout_stream, train_stream, branch: str, replicate: int):
    """
    Fit START/CORE/TERMINAL/singleton marginals on TRAIN only.
    Apply them to the supplied layout skeleton while preserving exact token lengths.
    """
    rng=random.Random(derive_seed("slot",branch,replicate))
    model=fit_slot_model(train_stream)
    out=clone_stream(layout_stream)

    # Backoffs are fixed and purely mechanical, to keep generator defined on tiny fixtures.
    fallback = unit_counts(train_stream)
    single_dist = model.single or fallback
    start_dist = model.start or fallback
    core_dist = model.core or fallback
    terminal_dist = model.terminal or fallback

    for tok in iter_tokens(out):
        n=len(tok)
        if n==0:
            continue
        if n==1:
            tok[:] = [_sample_counter(single_dist,rng)]
        else:
            new=[_sample_counter(start_dist,rng)]
            if n>2:
                new += [_sample_counter(core_dist,rng) for _ in range(n-2)]
            new += [_sample_counter(terminal_dist,rng)]
            tok[:] = new
    return out

def assert_weak_invariants(original, out):
    assert shape_signature(original)==shape_signature(out)
    assert unit_counts(original)==unit_counts(out)

def assert_slot_invariants(layout, out, train):
    assert shape_signature(layout)==shape_signature(out)
    allowed=set(unit_counts(train))
    assert all(u in allowed for tok in iter_tokens(out) for u in tok)
