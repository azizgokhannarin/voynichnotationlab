#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"search"))
from mapping_engine import *

# Deliberately tiny search space: 3 source units, 3 target classes + NULL.
# Exhaustive enumeration is the oracle; beam search must return exactly the same optimum.
target=( [["A","N"]]*80 + [["K","A"]]*50 + [["A","K"]]*30 +
         [["N","A","K"]]*20 + [["K","N"]]*10 )
lm=NGramLM().fit(target)

def page(pid,split,toks):
 return {"page":pid,"split":split,"lines":[{"line":pid+".1","tokens":
   [{"surface":"".join(t),"units":list(t)} for t in toks]}]}

train=[page("p1","train",
 [["x","n"],["x","n"],["k","x"],["x","k"],["n","x","k"]]*20)]
val=[page("p2","validation",
 [["x","n"],["k","x"],["x","k"],["n","x","k"]]*8)]
final=[page("p3","final_test",[["x","n"],["k","x"],["n","x","k"]]*3)]

cfg=SearchConfig(beam_width=256)
beam=beam_search(train,val,lm,{"A","N","K"},cfg)
oracle=exhaustive_search(train,val,lm,{"A","N","K"},cfg)

assert beam["mapping"]==oracle["mapping"],(beam,oracle)
assert abs(beam["validation_objective"]-oracle["validation_objective"])<1e-12
assert beam["mapping_sha256"]==oracle["mapping_sha256"]

beam2=beam_search(train,val,lm,{"A","N","K"},cfg)
assert beam2["mapping"]==beam["mapping"]
assert beam2["mapping_sha256"]==beam["mapping_sha256"]

guard=FinalTestGuard()
try:
 guard.score_final(lm,final,beam["mapping"],cfg); raise AssertionError("guard failed")
except RuntimeError: pass
frozen=guard.freeze(beam["mapping"])
guard.score_final(lm,final,beam["mapping"],cfg)
tampered=dict(beam["mapping"]); tampered["x"]="N" if tampered["x"]!="N" else "A"
try:
 guard.score_final(lm,final,tampered,cfg); raise AssertionError("mutation accepted")
except RuntimeError: pass

print("MAPPING ENGINE: PASS")
print("Beam == exhaustive optimum:",beam["mapping"])
print("Mapping SHA256:",beam["mapping_sha256"])
print("Validation objective:",f"{beam['validation_objective']:.9f}")
print("Final-test guard:",frozen)
