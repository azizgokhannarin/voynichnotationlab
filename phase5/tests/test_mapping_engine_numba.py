#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'search'))
from mapping_engine import NGramLM,beam_search
from mapping_engine_numba import fast_beam_search

target=([['A','N']]*80+[['K','A']]*50+[['A','K']]*30+[['N','A','K']]*20+[['K','N']]*10)
def page(pid,toks):return {'page':pid,'split':'train','lines':[{'line':pid+'.1','tokens':[{'surface':'x','units':list(t)} for t in toks]}]}
train=[page('p1',[['x','n'],['x','n'],['k','x'],['x','k'],['n','x','k']]*20)]
val=[page('p2',[['x','n'],['k','x'],['x','k'],['n','x','k']]*8)]
old=beam_search(train,val,NGramLM().fit(target),{'A','N','K'})
new=fast_beam_search(train,val,target)
assert old['mapping']==new['mapping'],(old,new)
assert abs(old['validation_objective']-new['validation_objective'])<1e-12,(old,new)
assert old['mapping_sha256']==new['mapping_sha256']
print('NUMBA ENGINE == FROZEN REFERENCE: PASS')
print(new['mapping'],new['validation_objective'],new['mapping_sha256'])
