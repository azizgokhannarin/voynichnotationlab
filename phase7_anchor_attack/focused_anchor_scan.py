#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from anchor_scan import load_stream,source_stats,LexIndex,anchor_mapping,evaluate

FOCUS=[('o','l'),('a','r'),('o','r'),('s',),('a','l'),('y',),('QO',),('SH','o'),('d','y'),('a','m')]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stream',required=True);ap.add_argument('--lexicon',required=True);ap.add_argument('--branch',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
 pages=load_stream(a.stream);tr_occ,tr_pages=source_stats(pages,'train');va_occ,_=source_stats(pages,'validation')
 raw=json.loads(Path(a.lexicon).read_text(encoding='utf-8'));lex=LexIndex(raw['entries'])
 out={'branch':a.branch,'ranking_basis':'TRAIN_ONLY','sources':{}}
 for src in FOCUS:
  rows=[]
  if tr_occ[src]==0: continue
  for tgt,rec in lex.words.get(len(src),[])[:120]:
   if rec['frequency']<10:continue
   m=anchor_mapping(src,tgt)
   if m is None:continue
   tr=evaluate(m,tr_occ,lex,anchor=src,max_source_types=400)
   va=evaluate(m,va_occ,lex,anchor=None,max_source_types=300)
   rows.append({'source':' '.join(src),'source_surface':''.join(src),'source_freq':tr_occ[src],
                'target':' '.join(tgt),'target_example':rec['example'],'target_frequency':rec['frequency'],
                'mapping':m,'train':tr,'validation':va})
  rows.sort(key=lambda x:(-x['train']['score'],-x['train']['resolved_exact_occurrences'],-x['train']['unique_partial_types'],x['target']))
  out['sources'][''.join(src)]=rows[:15]
  if rows:
   r=rows[0]
   print(a.branch,''.join(src),'best ->',r['target_example'],'score',r['train']['score'],'exact',r['train']['resolved_exact_types'],'unique',r['train']['unique_partial_types'],'ext',r['train']['consistent_extension_symbols'],'VAL exact',r['validation']['resolved_exact_types'])
 Path(a.out).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
if __name__=='__main__':main()
