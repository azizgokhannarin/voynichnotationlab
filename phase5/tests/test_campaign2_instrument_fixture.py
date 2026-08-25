#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"search"))

from mapping_engine import NGramLM, SearchConfig, beam_search
from campaign2_calibration import build_positive_encoding, build_negative_matched

TARGET=(
 [["A","N"],["A","N"],["K","A","N"],["K","A","R"],
  ["S","A","N"],["S","A","R"],["A","R"]]*200
)
lm=NGramLM().fit(TARGET)

src_tokens,key=build_positive_encoding(TARGET[:700],"FIX",37)
neg_tokens=build_negative_matched(TARGET[:700],"FIX")

def mk_stream(tokens,split,pid):
    return [{"page":pid,"split":split,"lines":[{"line":pid+".1","tokens":[
        {"surface":"x","units":list(t)} for t in tokens
    ]}]}]

# deterministic train/validation cut
pos_train=mk_stream(src_tokens[:500],"train","p1")
pos_val=mk_stream(src_tokens[500:700],"validation","p2")
neg_train=mk_stream(neg_tokens[:500],"train","n1")
neg_val=mk_stream(neg_tokens[500:700],"validation","n2")

target_inventory={"A","N","K","S","R"}
cfg=SearchConfig(beam_width=256)

pos=beam_search(pos_train,pos_val,lm,target_inventory,cfg)
neg=beam_search(neg_train,neg_val,lm,target_inventory,cfg)

assert pos["validation_objective"] < neg["validation_objective"], (pos,neg)

print("CAMPAIGN2 INSTRUMENT FIXTURE: PASS")
print("positive J:",f"{pos['validation_objective']:.6f}")
print("negative J:",f"{neg['validation_objective']:.6f}")
