#!/usr/bin/env python3
import json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"search"))

from null_models import *

FIXTURE=[
    {"page":"p1","lines":[
        [["QO","k","a","y"],["DA","i","n"],["o","r"]],
        [["s"],["QO","t","e","y"]]
    ]},
    {"page":"p2","lines":[
        [["DA","a","r"],["QO","k","ai","n"],["r"]],
        [["o","l"],["DA","e","y"]]
    ]}
]

def main():
    # deterministic seed contract
    assert derive_seed("A",0)==derive_seed("A",0)
    assert derive_seed("A",0)!=derive_seed("A",1)
    assert derive_seed("A",0)!=derive_seed("B",0)

    a=null_a_within_token_shuffle(FIXTURE,0)
    assert_null_a(FIXTURE,a)
    assert a==null_a_within_token_shuffle(FIXTURE,0)

    b=null_b_line_token_shuffle(FIXTURE,0)
    assert_null_b(FIXTURE,b)
    assert b==null_b_line_token_shuffle(FIXTURE,0)

    c=null_c_matched_synthetic(FIXTURE,FIXTURE,0)
    assert_null_c(FIXTURE,c,FIXTURE)
    assert c==null_c_matched_synthetic(FIXTURE,FIXTURE,0)

    d,m=null_d_label_permutation(FIXTURE,0)
    assert_null_d(FIXTURE,d,m)
    d2,m2=null_d_label_permutation(FIXTURE,0)
    assert d==d2 and m==m2

    print("ALL NULL-MODEL INVARIANTS PASS")
    print("A seed",derive_seed("A",0))
    print("B seed",derive_seed("B",0))
    print("C seed",derive_seed("C",0))
    print("D seed",derive_seed("D",0))

if __name__=="__main__":
    main()
