#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"search"))
from campaign2_calibration import *
TOKENS=([['A','N'],['K','A','N'],['S','A','R'],['A','R'],['K','A','R'],['S','A','N']]*100)
tr=TOKENS[:400]; va=TOKENS[400:]
pos_tr,pos_va,groups=build_positive(tr,va,37)
pos_tr2,pos_va2,groups2=build_positive(tr,va,37)
assert pos_tr==pos_tr2 and pos_va==pos_va2 and groups==groups2
assert lengths(tr+va)==lengths(pos_tr+pos_va)
assert len({u for t in pos_tr for u in t})==37
neg_tr,neg_va=build_negative(pos_tr,pos_va,'TEST')
neg_tr2,neg_va2=build_negative(pos_tr,pos_va,'TEST')
assert (neg_tr,neg_va)==(neg_tr2,neg_va2)
assert lengths(pos_tr+pos_va)==lengths(neg_tr+neg_va)
assert counts(pos_tr+pos_va)==counts(neg_tr+neg_va)
assert {u for t in neg_va for u in t}<={u for t in neg_tr for u in t}
print('CAMPAIGN2 PRODUCTION CALIBRATION GENERATORS: PASS')
print('active source inventory:',len({u for t in pos_tr for u in t}))
