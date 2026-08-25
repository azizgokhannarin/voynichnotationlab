#!/usr/bin/env python3
"""
Freeze locally acquired Campaign-1 corpus payloads into CORPUS_MANIFEST_SHA256.csv.

Usage:
  python phase5/corpora/freeze_local_corpus.py WG-P2 /path/to/tei_1.1.zip --tokens 123456
"""
import argparse, csv, hashlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
MANIFEST=HERE/"CORPUS_MANIFEST_SHA256.csv"

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

ap=argparse.ArgumentParser()
ap.add_argument("corpus_id")
ap.add_argument("payload",type=Path)
ap.add_argument("--tokens",type=int,default=None,
                help="Filtered 1300-1500 usable token count after corpus-specific extraction")
args=ap.parse_args()

if not args.payload.is_file():
    raise SystemExit(f"payload not found: {args.payload}")

rows=[]
found=False
with MANIFEST.open(encoding="utf-8",newline="") as f:
    rd=csv.DictReader(f)
    fields=rd.fieldnames
    for r in rd:
        if r["corpus_id"]==args.corpus_id:
            found=True
            r["local_filename"]=args.payload.name
            r["local_bytes"]=str(args.payload.stat().st_size)
            r["local_sha256"]=sha256(args.payload)
            if args.tokens is not None:
                r["token_count_filtered"]=str(args.tokens)
            r["status"]="FROZEN_LOCAL" if args.tokens is not None else "LOCAL_HASHED_TOKENCOUNT_PENDING"
        rows.append(r)
if not found:
    raise SystemExit(f"unknown corpus_id: {args.corpus_id}")

with MANIFEST.open("w",encoding="utf-8",newline="") as f:
    wr=csv.DictWriter(f,fieldnames=fields)
    wr.writeheader();wr.writerows(rows)

print(args.corpus_id,args.payload.name,sha256(args.payload))
