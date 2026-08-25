#!/usr/bin/env python3
import argparse,html,json,math,random,re,sys,zipfile
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'phase5'/'search'))
from historical_normalizers import normalize
from prepare_target_streams import select_manifest
CANDIDATES={
'or_to_in_base':{'o':'I','r':'N'},'or_to_in_wave1':{'o':'I','r':'N','y':'E','l':'X'},
'or_to_en_base':{'o':'E','r':'N'},'or_to_en_wave1':{'o':'E','r':'N','l':'R'},
'or_to_am_base':{'o':'A','r':'M'},'or_to_am_wave1':{'o':'A','r':'M','DA':'R','i':'U','l':'L','y':'E','e':'T','CH':'W'}}
def target(repo,renzip):
 docs=[]
 with zipfile.ZipFile(renzip) as z:
  for r in select_manifest(Path(repo)/'phase5/corpora/ReN_1300_1500_manifest.csv'):
   s=z.read(r['file']).decode('utf8','ignore');d=[]
   for x in re.findall(r'<w\b[^>]*>(.*?)</w>',s,re.I|re.S):
    x=html.unescape(re.sub(r'<[^>]+>','',x)).strip(); n=normalize(x,'WG') if x else None
    if n:d.append(tuple(n))
   if d:docs.append(d)
 lex=Counter(x for d in docs for x in d); ids={w:i for i,w in enumerate(lex)}
 bi=Counter();ctx=Counter()
 for d in docs:
  for a,b in zip(d,d[1:]):bi[(ids[a],ids[b])]+=1;ctx[ids[a]]+=1
 V=len(ids);alpha=.25
 logp={(a,b):math.log2((c+alpha)/(ctx[a]+alpha*V)) for (a,b),c in bi.items()}
 default={a:math.log2(alpha/(ctx[a]+alpha*V)) for a in ids.values()}
 return lex,ids,bi,logp,default
def rows(pages,split,m,ids):
 out=[]
 for p in pages:
  if p['split']!=split:continue
  for line in p['lines']:
   arr=[]
   for t in line['tokens']:
    u=t['units']; d=tuple(m[x] for x in u) if all(x in m for x in u) else None
    arr.append(ids.get(d,-1) if d else -1)
   out.append(arr)
 return out
def metric(lines,bi,logp,default):
 pairs=att=0;lp=0.0
 for a in lines:
  for x,y in zip(a,a[1:]):
   if x>=0 and y>=0:
    pairs+=1; att+=bi.get((x,y),0)>0; lp+=logp.get((x,y),default[x])
 return pairs,att,(lp/pairs if pairs else None)
def null(lines,bi,logp,default,n,seed):
 rng=random.Random(seed);A=[];L=[]
 for _ in range(n):
  att=pair=0;lp=0.0
  for orig in lines:
   a=orig[:];rng.shuffle(a)
   for x,y in zip(a,a[1:]):
    if x>=0 and y>=0:
     pair+=1;att+=bi.get((x,y),0)>0;lp+=logp.get((x,y),default[x])
  A.append(att);L.append(lp/pair if pair else float('-inf'))
 return A,L
def stat(o,v):
 v=[x for x in v if math.isfinite(x)];mu=sum(v)/len(v);sd=(sum((x-mu)**2 for x in v)/(len(v)-1))**.5 if len(v)>1 else 0
 return {'mean':mu,'sd':sd,'z':(o-mu)/sd if sd else None,'p_emp':(1+sum(x>=o for x in v))/(len(v)+1)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--stream',required=True);ap.add_argument('--renzip',required=True);ap.add_argument('--out',required=True);ap.add_argument('--n',type=int,default=500);a=ap.parse_args()
 lex,ids,bi,logp,default=target(a.repo,a.renzip);pages=json.load(open(a.stream))['pages'];res={'schema':'ANCHOR-PHRASE-v1','branch':'ReN','final_test_used':False,'permutations':a.n,'candidates':{}}
 for ci,(name,m) in enumerate(CANDIDATES.items()):
  rr={'mapping':m}
  for si,split in enumerate(('train','validation')):
   ln=rows(pages,split,m,ids);pairs,att,lp=metric(ln,bi,logp,default);A,L=null(ln,bi,logp,default,a.n,20260825+ci*1000+si)
   rr[split]={'lexical_pair_occurrences':pairs,'attested_bigram_occurrences':att,'attested_ratio':att/pairs if pairs else None,'mean_target_bigram_log2p':lp,'attested_null':stat(att,A),'logp_null':stat(lp,L) if lp is not None else None}
  res['candidates'][name]=rr
 Path(a.out).write_text(json.dumps(res,indent=2),encoding='utf8')
if __name__=='__main__':main()
