#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,sys
from pathlib import Path
from collections import Counter,defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'phase5'/'search'))
from prepare_target_streams import select_manifest,ref_words,ren_words,bfm_words,dante_words,latin_words
from historical_normalizers import normalize

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',required=True);ap.add_argument('--branch',required=True)
    ap.add_argument('--refroot');ap.add_argument('--renzip');ap.add_argument('--bfmzip')
    ap.add_argument('--dantezip');ap.add_argument('--latzip');ap.add_argument('--out',required=True)
    a=ap.parse_args();base=Path(a.repo)/'phase5'/'corpora'
    if a.branch=='ReF':words=ref_words(a.refroot,select_manifest(base/'ReF_1350_1500_manifest.csv'));lang='WG'
    elif a.branch=='ReN':words=ren_words(a.renzip,select_manifest(base/'ReN_1300_1500_manifest.csv'));lang='WG'
    elif a.branch=='BFM':words=bfm_words(a.bfmzip,select_manifest(base/'BFM2022_1300_1500_manifest.csv'));lang='FR'
    elif a.branch=='Dante':words=dante_words(a.dantezip);lang='OIT'
    elif a.branch=='Latin':words,_=latin_words(a.latzip);lang='LAT'
    else:raise ValueError(a.branch)
    freq=Counter();examples=defaultdict(Counter)
    for w in words:
        seq=normalize(w,lang)
        if not seq:continue
        key=tuple(seq);freq[key]+=1;examples[key][w]+=1
    entries=[]
    for seq,n in freq.items():
        ex=examples[seq].most_common(1)[0][0]
        entries.append({'seq':list(seq),'frequency':n,'example':ex,
                        'examples':[w for w,_ in examples[seq].most_common(5)]})
    entries.sort(key=lambda r:(-r['frequency'],len(r['seq']),r['seq']))
    Path(a.out).write_text(json.dumps({'branch':a.branch,'normalizer':lang,
        'token_count':sum(freq.values()),'type_count':len(freq),'entries':entries},
        ensure_ascii=False,indent=2),encoding='utf-8')
    print(a.branch,'tokens',sum(freq.values()),'types',len(freq))
if __name__=='__main__':main()
