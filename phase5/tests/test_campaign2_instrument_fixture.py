#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'search'))
from mapping_engine import NGramLM,SearchConfig,beam_search
from campaign2_calibration import build_positive,build_negative
TARGET=([['A','N'],['A','N'],['K','A','N'],['K','A','R'],['S','A','N'],['S','A','R'],['A','R']]*250)
lm=NGramLM().fit(TARGET)
raw=TARGET[:1000]; pos_tr,pos_va,_=build_positive(raw[:700],raw[700:],37); neg_tr,neg_va=build_negative(pos_tr,pos_va,'FIX')
def stream(ts,split,p): return [{'page':p,'split':split,'lines':[{'line':p+'.1','tokens':[{'surface':'x','units':list(t)} for t in ts]}]}]
cfg=SearchConfig(beam_width=256); inv={'A','N','K','S','R'}
pos=beam_search(stream(pos_tr,'train','p1'),stream(pos_va,'validation','p2'),lm,inv,cfg)
neg=beam_search(stream(neg_tr,'train','n1'),stream(neg_va,'validation','n2'),lm,inv,cfg)
assert pos['validation_objective']<neg['validation_objective'],(pos,neg)
print('CAMPAIGN2 37-SOURCE INSTRUMENT FIXTURE: PASS')
print('positive J:',f"{pos['validation_objective']:.6f}")
print('negative J:',f"{neg['validation_objective']:.6f}")
