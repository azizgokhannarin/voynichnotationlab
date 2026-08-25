#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from collections import Counter,defaultdict

def pattern(seq):
    d={};n=0;out=[]
    for x in seq:
        if x not in d:d[x]=n;n+=1
        out.append(d[x])
    return tuple(out)

def anchor_mapping(src,tgt):
    if len(src)!=len(tgt) or pattern(src)!=pattern(tgt): return None
    return dict(zip(src,tgt))

def load_stream(path): return json.loads(Path(path).read_text(encoding='utf-8'))['pages']

def source_stats(pages,split):
    occ=Counter();pgs=defaultdict(set)
    for p in pages:
        if p['split']!=split:continue
        for line in p['lines']:
            for t in line['tokens']:
                s=tuple(t['units']);occ[s]+=1;pgs[s].add(p['page'])
    return occ,{k:len(v) for k,v in pgs.items()}

class LexIndex:
    def __init__(self,entries,minfreq=3,maxlen=10,top_per_len=8000):
        bylen=defaultdict(list)
        for rec in entries:
            seq=tuple(rec['seq']); n=rec['frequency']
            if n>=minfreq and 1<=len(seq)<=maxlen: bylen[len(seq)].append((seq,rec))
        self.words={};self.inv={}
        for L,items in bylen.items():
            items.sort(key=lambda x:-x[1]['frequency']);items=items[:top_per_len]
            self.words[L]=items
            ix=defaultdict(set)
            for idx,(seq,rec) in enumerate(items):
                for pos,val in enumerate(seq):ix[(pos,val)].add(idx)
            self.inv[L]=ix
    def candidates(self,src,mapping):
        L=len(src); items=self.words.get(L,[])
        if not items:return []
        constraints=[(i,mapping[s]) for i,s in enumerate(src) if s in mapping]
        if not constraints:return []
        sets=[self.inv[L].get(k,set()) for k in constraints]
        if any(not s for s in sets):return []
        ids=set.intersection(*sets)
        rev={v:k for k,v in mapping.items()}
        out=[]
        for idx in ids:
            word,rec=items[idx];new={};newrev={}
            ok=True
            for s,t in zip(src,word):
                if s in mapping:
                    if mapping[s]!=t:ok=False;break
                else:
                    if t in rev and rev[t]!=s:ok=False;break
                    if s in new and new[s]!=t:ok=False;break
                    if t in newrev and newrev[t]!=s:ok=False;break
                    new[s]=t;newrev[t]=s
            if ok:out.append((word,rec,new))
        return out
    def exact(self,target):
        L=len(target)
        # exact map precomputed lazily
        for seq,rec in self.words.get(L,[]):
            if seq==target:return rec
        return None

def evaluate(mapping,source_occ,lex,anchor=None,max_source_types=400):
    exact_types=exact_occ=0; unique=[]; conflict=0; votes=defaultdict(Counter)
    source_items=[(s,n) for s,n in source_occ.most_common(max_source_types) if len(s)<=10]
    exactsets={L:{seq for seq,_ in lex.words.get(L,[])} for L in lex.words}
    for src,nocc in source_items:
        if anchor is not None and src==anchor:continue
        known=sum(s in mapping for s in src)
        if known==len(src):
            tgt=tuple(mapping[s] for s in src)
            if tgt in exactsets.get(len(src),set()):exact_types+=1;exact_occ+=nocc
            continue
        if known<2:continue
        cands=lex.candidates(src,mapping)
        if len(cands)==1:
            word,rec,ext=cands[0];unique.append((src,nocc,word,rec,ext))
            for s,t in ext.items():votes[s][t]+=nocc
    extensions={}
    for s,v in votes.items():
        if len(v)==1:extensions[s]=next(iter(v))
        else:conflict+=1
    rev={v:k for k,v in mapping.items()}; tgtnew=defaultdict(list)
    for s,t in extensions.items():tgtnew[t].append(s)
    clean={}
    for s,t in extensions.items():
        if (t in rev and rev[t]!=s) or len(tgtnew[t])>1:conflict+=1
        else:clean[s]=t
    score=exact_occ+5*exact_types+3*len(unique)+2*len(clean)-5*conflict
    return {'score':score,'resolved_exact_occurrences':exact_occ,'resolved_exact_types':exact_types,
            'unique_partial_types':len(unique),'consistent_extension_symbols':len(clean),
            'conflicting_unique_types':conflict,'extensions':clean,
            'unique_examples':[{'source':' '.join(s),'occ':n,'target':' '.join(w),
                                'target_example':rec['example'],'extension':ext}
                               for s,n,w,rec,ext in unique[:20]]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stream',required=True);ap.add_argument('--lexicon',required=True)
    ap.add_argument('--branch',required=True);ap.add_argument('--out',required=True)
    ap.add_argument('--top-source',type=int,default=30);ap.add_argument('--top-target',type=int,default=60)
    a=ap.parse_args();pages=load_stream(a.stream)
    tr_occ,tr_pages=source_stats(pages,'train');va_occ,_=source_stats(pages,'validation')
    raw=json.loads(Path(a.lexicon).read_text(encoding='utf-8'));lex=LexIndex(raw['entries'])
    sources=[s for s,n in tr_occ.most_common() if 1<=len(s)<=3 and n>=20 and tr_pages[s]>=10][:a.top_source]
    rows=[]
    for src in sources:
        targets=lex.words.get(len(src),[])[:a.top_target]
        for tgt,rec in targets:
            if rec['frequency']<10:continue
            m=anchor_mapping(src,tgt)
            if m is None:continue
            tr=evaluate(m,tr_occ,lex,anchor=src);va=evaluate(m,va_occ,lex,anchor=None,max_source_types=300)
            rows.append({'source':' '.join(src),'source_surface':''.join(src),'source_freq':tr_occ[src],
                         'source_pages':tr_pages[src],'target':' '.join(tgt),'target_example':rec['example'],
                         'target_frequency':rec['frequency'],'mapping':m,'train':tr,'validation':va})
    rows.sort(key=lambda x:(-x['train']['score'],-x['train']['resolved_exact_occurrences'],
                            -x['train']['unique_partial_types'],x['source'],x['target']))
    Path(a.out).write_text(json.dumps({'branch':a.branch,'ranking_basis':'TRAIN_ONLY','anchors_tested':len(rows),'top':rows[:100]},indent=2,ensure_ascii=False),encoding='utf-8')
    print(a.branch,'anchors',len(rows))
    for i,x in enumerate(rows[:10],1):
        print(i,x['source_surface'],'->',x['target_example'],'train',x['train']['score'],
              'exact',x['train']['resolved_exact_types'],'unique',x['train']['unique_partial_types'],
              'ext',x['train']['consistent_extension_symbols'],'val-exact',x['validation']['resolved_exact_types'],
              'val-unique',x['validation']['unique_partial_types'])
if __name__=='__main__':main()
