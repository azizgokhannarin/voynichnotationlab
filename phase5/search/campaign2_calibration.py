#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
import hashlib
import random

MASTER_SEED=20260825
VERSION="C2-CAL-v1"

def _seed(branch):
    key=f"{VERSION}|{branch}|{MASTER_SEED}".encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8],"big")

def invented_alphabet(n=37):
    if n < 1:
        raise ValueError(n)
    return [f"X{i:02d}" for i in range(n)]

def build_positive_encoding(phonographic_tokens, branch, source_size=37):
    """
    Deterministically assign each distinct target class to one invented source symbol.
    If target inventory exceeds source_size, fail rather than silently merge.
    """
    classes=sorted({u for tok in phonographic_tokens for u in tok})
    if len(classes)>source_size:
        raise ValueError("target inventory exceeds invented source alphabet")
    rng=random.Random(_seed(branch))
    src=invented_alphabet(source_size)
    rng.shuffle(src)
    mapping=dict(zip(classes,src))
    encoded=[[mapping[u] for u in tok] for tok in phonographic_tokens]
    return encoded,mapping

def build_negative_matched(phonographic_tokens, branch):
    """
    Preserve exact token lengths and exact global class multiset, but destroy
    within-token conditional structure by shuffling the pooled classes globally
    and repartitioning by the original token-length vector.

    This is intentionally stronger than a per-token shuffle as a calibration negative:
    it preserves marginals/lengths but removes token-internal class co-occurrence.
    """
    rng=random.Random(_seed(branch+"|NEG"))
    lengths=[len(t) for t in phonographic_tokens]
    pool=[u for tok in phonographic_tokens for u in tok]
    rng.shuffle(pool)
    out=[]
    pos=0
    for n in lengths:
        out.append(pool[pos:pos+n])
        pos+=n
    assert pos==len(pool)
    return out

def token_lengths(tokens):
    return [len(t) for t in tokens]

def global_counts(tokens):
    c=Counter()
    for t in tokens:
        c.update(t)
    return c
