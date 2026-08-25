#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,html,json,math,random,re,statistics,subprocess,sys,zipfile
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'phase5'/'search'))
from historical_normalizers import normalize
from prepare_target_streams import select_manifest

CANDIDATES={
 'or_to_in_base': {'o':'I','r':'N'},
 'or_to_in_wave1': {'o':'I','r':'N','y':'E','l':'X'},
 'or_to_en_base': {'o':'E','r':'N'},
 'or_to_en_wave1': {'o':'E','r':'N','l':'R'},
 'or_to_am_base': {'o':'A','r':'M'},
 'or_to_am_wave1': {'o':'A','r':'M','DA':'R','i':'U','l':'L','y':'E','e':'T','CH':'W'},
}

def ren_docs(renzip,manifest):
    docs=[]
    with zipfile.ZipFile(renzip) as z:
        for r in manifest:
            s=z.read(r['file']).decode('utf-8','ignore')
            seq=[]
            for x in re.findall(r'<w\b[^>]*>(.*?)</w>',s,re.I|re.S):
                x=re.sub(r'<[^>]+>','',x)
                x=html.unescape(x).strip()
                if not x: continue
                n=normalize(x,'WG')
                if n: seq.append(tuple(n))
            if seq: docs.append(seq)
    return docs

def load_voynich(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))['pages']

def decode(tok,m):
    u=tok['units']
    if not all(x in m for x in u): return None
    return tuple(m[x] for x in u)

def build_target(docs):
    uni=Counter(); bi=Counter(); ctx=Counter()
    for d in docs:
        uni.update(d)
        for a,b in zip(d,d[1:]): bi[(a,b)]+=1;ctx[a]+=1
    return uni,bi,ctx

def line_rows(pages,split,m,lex):
    rows=[]
    for p in pages:
        if p['split']!=split: continue
        for line in p['lines']:
            arr=[]
            for tok in line['tokens']:
                d=decode(tok,m)
                arr.append((tuple(tok['units']),d, bool(d and d in lex)))
            rows.append(arr)
    return rows

def metrics(lines,bi,ctx,lex,V):
    pair_occ=att=0; logp=0.0; scored=0
    anchor_pairs=anchor_att=0
    alpha=.25
    examples=[]
    for line in lines:
        for (sa,a,oka),(sb,b,okb) in zip(line,line[1:]):
            if oka and okb:
                pair_occ+=1
                if bi[(a,b)]>0: att+=1
                # smoothed target word-bigram log probability
                p=(bi[(a,b)]+alpha)/(ctx[a]+alpha*V)
                logp+=math.log2(p);scored+=1
                if len(examples)<30:
                    examples.append({'src_a':'+'.join(sa),'src_b':'+'.join(sb),
                        'dec_a':' '.join(a),'dec_b':' '.join(b),'target_bigram_count':bi[(a,b)]})
            if (sa==('o','r') and okb) or (sb==('o','r') and oka):
                anchor_pairs+=1
                if sa==('o','r'):
                    hit=bi[(a,b)]>0 if oka and okb else False
                else:
                    hit=bi[(a,b)]>0 if oka and okb else False
                anchor_att+=int(hit)
    return {'lexical_pair_occurrences':pair_occ,'attested_bigram_occurrences':att,
            'attested_ratio':att/pair_occ if pair_occ else None,
            'mean_target_bigram_log2p':logp/scored if scored else None,
            'anchor_neighbor_pairs':anchor_pairs,'anchor_neighbor_attested':anchor_att,
            'examples':examples}

def shuffled(lines,rng):
    out=[]
    for line in lines:
        x=list(line);rng.shuffle(x);out.append(x)
    return out

def null(lines,bi,ctx,lex,V,n,seed):
    rng=random.Random(seed)
    at=[];lp=[]
    for _ in range(n):
        x=metrics(shuffled(lines,rng),bi,ctx,lex,V)
        at.append(x['attested_bigram_occurrences'])
        lp.append(x['mean_target_bigram_log2p'] if x['mean_target_bigram_log2p'] is not None else float('-inf'))
    return at,lp

def stat(obs,vals,higher=True):
    vals=[float(v) for v in vals if math.isfinite(v)]
    mu=sum(vals)/len(vals)
    sd=(sum((v-mu)**2 for v in vals)/(len(vals)-1))**0.5 if len(vals)>1 else 0
    z=(obs-mu)/sd if sd else None
    if higher: hits=sum(v>=obs for v in vals)
    else: hits=sum(v<=obs for v in vals)
    return {'null_mean':mu,'null_sd':sd,'z':z,'p_emp':(1+hits)/(len(vals)+1),'hits':hits}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--stream',required=True)
    ap.add_argument('--renzip',required=True);ap.add_argument('--out',required=True);ap.add_argument('--n',type=int,default=1000)
    a=ap.parse_args(); repo=Path(a.repo)
    docs=ren_docs(a.renzip,select_manifest(repo/'phase5/corpora/ReN_1300_1500_manifest.csv'))
    lex,bi,ctx=build_target(docs);V=len(lex);pages=load_voynich(a.stream)
    result={'schema':'ANCHOR-PHRASE-v1','branch':'ReN','final_test_used':False,'permutations':a.n,'candidates':{}}
    for ci,(name,m) in enumerate(CANDIDATES.items()):
        rr={'mapping':m}
        for split in ('train','validation'):
            lines=line_rows(pages,split,m,lex)
            obs=metrics(lines,bi,ctx,lex,V)
            at,lp=null(lines,bi,ctx,lex,V,a.n,20260825+ci*10000+(0 if split=='train' else 1))
            obs['attested_bigram_null']=stat(obs['attested_bigram_occurrences'],at,True)
            if obs['mean_target_bigram_log2p'] is not None:
                obs['bigram_logp_null']=stat(obs['mean_target_bigram_log2p'],lp,True)
            rr[split]=obs
        result['candidates'][name]=rr
    Path(a.out).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
