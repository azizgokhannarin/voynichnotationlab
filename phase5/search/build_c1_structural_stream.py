#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,re,json,hashlib
from collections import Counter
from pathlib import Path
from structural_serializer import validate_stream,stream_sha256,write_canonical

MULTI=sorted(['cfhh','cphh','ckhh','cthh','cfh','cph','ckh','cth','ch','sh'],key=len,reverse=True)

def glyphs(token):
    out=[];i=0
    while i<len(token):
        g=next((m for m in MULTI if token.startswith(m,i)),None)
        if g:
            out.append(g);i+=len(g)
        else:
            out.append(token[i]);i+=1
    return out

def frozen_units(token):
    gs=glyphs(token);out=[];i=0
    while i<len(gs):
        if i+1<len(gs) and gs[i]=='q' and gs[i+1]=='o':
            out.append('QO');i+=2
        elif i+1<len(gs) and gs[i]=='d' and gs[i+1]=='a':
            out.append('DA');i+=2
        else:
            # ch/sh are single EVA glyphs; uppercase labels are naming controls only.
            out.append(gs[i].upper() if gs[i] in ('ch','sh') else gs[i]);i+=1
    return out

def load_split(path):
    rows={}
    with Path(path).open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f):
            split={'train':'train','validation':'validation','test':'final_test'}[r['split']]
            rows[r['page']]={'split':split,'expected_tokens':int(r['tokens'])}
    return rows

def parse_rf1b(path, split_manifest):
    split=load_split(split_manifest)
    pages={p:{'page':p,'split':x['split'],'lines':[]} for p,x in split.items()}
    counts=Counter(); dropped_empty=0
    locus_re=re.compile(r'^<([^>]+)>\s*(.*)$')
    for raw in Path(path).read_text(encoding='utf-8',errors='replace').splitlines():
        if raw.startswith('#') or '<!' in raw:
            continue
        m=locus_re.match(raw)
        if not m: continue
        locus,body=m.group(1),m.group(2)
        page=locus.split('.')[0]
        if page not in pages: continue
        # This is the exact parser family used to create the frozen split token counts.
        body=re.sub(r'@\d+;','',body).replace('<->','.')
        tokens=[]
        for rawtok in re.split(r'[.\s,]+',body):
            surface=re.sub(r'[^a-z]','',rawtok)
            if not surface:
                dropped_empty+=1;continue
            tokens.append({'surface':surface,'units':frozen_units(surface)})
            counts[page]+=1
        if tokens:
            pages[page]['lines'].append({'line':locus,'tokens':tokens})
    missing=set(split)-set(p for p,n in counts.items() if n>0)
    if missing: raise RuntimeError(f'missing pages: {sorted(missing)}')
    mismatches=[]
    for p,x in split.items():
        if counts[p]!=x['expected_tokens']:
            mismatches.append((p,x['expected_tokens'],counts[p]))
    if mismatches: raise RuntimeError(f'token-count mismatch: {mismatches[:20]}')
    # Deterministic manifest order, not dictionary insertion order.
    stream=[pages[p] for p in sorted(pages)]
    validate_stream(stream)
    return stream,counts

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rf1b',type=Path)
    ap.add_argument('split_manifest',type=Path)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--report',type=Path)
    a=ap.parse_args()
    stream,counts=parse_rf1b(a.rf1b,a.split_manifest)
    sha=write_canonical(stream,a.out)
    inv=Counter();split_t=Counter();split_p=Counter();split_l=Counter()
    for p in stream:
        split_p[p['split']]+=1
        for line in p['lines']:
            split_l[p['split']]+=1
            split_t[p['split']]+=len(line['tokens'])
            for t in line['tokens']:inv.update(t['units'])
    report={
      'schema':'C1-STRUCT-v1','stream_sha256':sha,'pages':len(stream),
      'page_counts':dict(split_p),'line_counts':dict(split_l),'token_counts':dict(split_t),
      'tokens_total':sum(split_t.values()),'unit_inventory_size':len(inv),
      'unit_counts':dict(inv.most_common()),
    }
    if a.report:a.report.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
