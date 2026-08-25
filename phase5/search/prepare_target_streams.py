#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,re,zipfile,html,random
from pathlib import Path
from historical_normalizers import normalize

WORD=re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-žẞßŒœÆæſ]+(?:['’\-][A-Za-zÀ-ÖØ-öø-ÿĀ-žẞßŒœÆæſ]+)*")

def hash_sequences(seqs):
    h=hashlib.sha256()
    for s in seqs:
        h.update((' '.join(s)+'\n').encode())
    return h.hexdigest()

def select_manifest(path):
    return list(csv.DictReader(Path(path).open(encoding='utf-8',newline='')))

def ref_words(refroot,manifest):
    out=[]
    for r in manifest:
        p=Path(refroot)/r['file']
        s=p.read_text(encoding='utf-8',errors='ignore')
        # annotated word layer, not lemma
        out += re.findall(r'<tok_anno\b[^>]*\butf="([^"]+)"',s,re.I)
    return out

def ren_words(renzip,manifest):
    out=[]
    with zipfile.ZipFile(renzip) as z:
        for r in manifest:
            s=z.read(r['file']).decode('utf-8','ignore')
            # Preserve w-token boundaries; remove embedded XML tags but retain surface text.
            for x in re.findall(r'<w\b[^>]*>(.*?)</w>',s,re.I|re.S):
                x=re.sub(r'<[^>]+>','',x)
                if x.strip():out.append(html.unescape(x))
    return out

def bfm_words(bfmzip,manifest):
    allowed={r['file'] for r in manifest};out=[]
    with zipfile.ZipFile(bfmzip) as z:
        for n in z.namelist():
            if n.startswith('tei_xml/') and Path(n).name in allowed:
                s=z.read(n).decode('utf-8','ignore')
                for x in re.findall(r'<w\b[^>]*>(.*?)</w>',s,re.I|re.S):
                    x=re.sub(r'<[^>]+>','',x)
                    if x.strip():out.append(html.unescape(x))
    return out

def dante_words(dantezip):
    vern={'inferno','purgatorio','paradiso','convivio','vitanuova','rime','fiore','dettodamore'}
    out=[]
    with zipfile.ZipFile(dantezip) as z:
        for n in sorted(z.namelist()):
            if '/grammaticale/' not in n or not n.endswith('-plain.xml'):continue
            if Path(n).name[:-10].lower() not in vern:continue
            s=z.read(n).decode('utf-8','ignore')
            for x in re.findall(r'<LM\b[^>]*>(.*?)</LM>',s,re.I|re.S):
                x=re.sub(r'<[^>]+>','',x)
                if x.strip():out.append(html.unescape(html.unescape(x)))
    return out

def latin_doc_selected(attrs):
    date=attrs.get('date','')
    years=[int(x) for x in re.findall(r'(?<!\d)(1[1-6]\d{2})(?!\d)',date)]
    if years:
        return max(years)>=1300 and min(years)<=1500
    # PRE-SCORE AMENDMENT: century-only metadata must lie inside the primary window.
    # Pure 16th-century records are not included merely because the interval starts at 1500.
    cents=[int(x) for x in re.findall(r'(?:cent\.\s*)?(1[3-6])',attrs.get('century',''),re.I)]
    return bool(cents and min(cents)>=14 and max(cents)<=15)

def latin_words(latzip):
    out=[];keep=False;docs=[];cur=None;cnt=0
    with zipfile.ZipFile(latzip) as z:
        for line in z.read('latin14.txt').decode('utf-8','ignore').splitlines():
            if line.startswith('<doc'):
                attrs=dict(re.findall(r'(\w+)="([^"]*)"',line));keep=latin_doc_selected(attrs);cur=attrs;cnt=0
            elif line.startswith('</doc'):
                if keep and cur:docs.append((cur,cnt))
                keep=False;cur=None
            elif keep and line and not line.startswith('<'):
                tok=line.split('\t',1)[0].strip()
                if WORD.fullmatch(tok):out.append(tok);cnt+=1
    return out,docs

def normalize_words(words,lang):
    seqs=[];kept_words=[];dropped=[];cache={}
    for w in words:
        if w not in cache: cache[w]=normalize(w,lang)
        s=cache[w]
        if s: seqs.append(s);kept_words.append(w)
        elif any(c.isalpha() for c in w): dropped.append(w)
    return seqs,kept_words,dropped

def branch(name,args):
    base=Path(args.repo)/'phase5/corpora'
    if name=='ReF':words=ref_words(args.refroot,select_manifest(base/'ReF_1350_1500_manifest.csv'));lang='WG';docs=None
    elif name=='ReN':words=ren_words(args.renzip,select_manifest(base/'ReN_1300_1500_manifest.csv'));lang='WG';docs=None
    elif name=='BFM':words=bfm_words(args.bfmzip,select_manifest(base/'BFM2022_1300_1500_manifest.csv'));lang='FR';docs=None
    elif name=='Dante':words=dante_words(args.dantezip);lang='OIT';docs=None
    elif name=='Latin':words,docs=latin_words(args.latzip);lang='LAT'
    else:raise ValueError(name)
    seqs,kept_words,dropped=normalize_words(words,lang)
    inv=sorted({u for s in seqs for u in s})
    # Requirement #9.3: fixed random inspection sample, drawn before Voynich scoring.
    rng=random.Random(20260825)
    idx=list(range(len(seqs))); rng.shuffle(idx); idx=idx[:min(200,len(idx))]
    sample=[{'source':kept_words[i],'normalized':seqs[i]} for i in idx]
    return {'branch':name,'normalizer':lang,'raw_tokens':len(words),'normalized_tokens':len(seqs),
            'dropped_tokens':len(dropped),'dropped_pct':100*len(dropped)/max(1,len(words)),
            'inventory':inv,'stream_sha256':hash_sequences(seqs),'sample200':sample,
            'latin_docs':docs},seqs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--refroot',required=True)
    ap.add_argument('--renzip',required=True);ap.add_argument('--bfmzip',required=True);ap.add_argument('--dantezip',required=True);ap.add_argument('--latzip',required=True);ap.add_argument('--out',required=True)
    a=ap.parse_args();summary={}
    for n in ['ReF','ReN','BFM','Dante','Latin']:
        x,_=branch(n,a); summary[n]={k:v for k,v in x.items() if k not in ('sample200','latin_docs')}
    Path(a.out).write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
