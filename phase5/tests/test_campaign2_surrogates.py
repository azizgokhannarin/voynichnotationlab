#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"search"))

from campaign2_surrogates import *

STREAM=[
 {"page":"p1","split":"train","lines":[
  {"line":"p1.1","tokens":[
   {"surface":"abcd","units":["a","b","c","d"]},
   {"surface":"xy","units":["x","y"]},
   {"surface":"s","units":["s"]}
  ]},
  {"line":"p1.2","tokens":[
   {"surface":"ab","units":["a","b"]},
   {"surface":"acd","units":["a","c","d"]}
  ]}
 ]},
 {"page":"p2","split":"validation","lines":[
  {"line":"p2.1","tokens":[
   {"surface":"abcd","units":["a","b","c","d"]},
   {"surface":"xy","units":["x","y"]},
   {"surface":"s","units":["s"]}
  ]}
 ]}
]

train=[STREAM[0]]
val=[STREAM[1]]

a=weak_within_token_shuffle(STREAM,"TEST",0)
assert_weak_invariants(STREAM,a)
assert a==weak_within_token_shuffle(STREAM,"TEST",0)
assert a!=weak_within_token_shuffle(STREAM,"TEST",1)

s=independent_slot_surrogate(STREAM,train,"TEST",0)
assert_slot_invariants(STREAM,s,train)
assert s==independent_slot_surrogate(STREAM,train,"TEST",0)
assert s!=independent_slot_surrogate(STREAM,train,"TEST",1)

# Ensure slot roles are sampled only from TRAIN-fitted role inventories.
model=fit_slot_model(train)
for tok in iter_tokens(s):
    if len(tok)==1:
        assert tok[0] in (set(model.single) or set(unit_counts(train)))
    else:
        assert tok[0] in (set(model.start) or set(unit_counts(train)))
        assert tok[-1] in (set(model.terminal) or set(unit_counts(train)))
        if len(tok)>2:
            assert all(u in (set(model.core) or set(unit_counts(train))) for u in tok[1:-1])

print("CAMPAIGN2 SURROGATES: PASS")
print("weak seed 0:",derive_seed("weak","TEST",0))
print("slot seed 0:",derive_seed("slot","TEST",0))
