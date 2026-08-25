#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib
from collections import Counter
from pathlib import Path

SCHEMA_VERSION="C1-STRUCT-v1"
SPLITS={"train","validation","final_test"}

def validate_stream(stream):
    pages=set()
    for p in stream:
        if set(p)!={"page","split","lines"}: raise ValueError("page schema")
        if not p["page"] or p["page"] in pages: raise ValueError("page id")
        pages.add(p["page"])
        if p["split"] not in SPLITS: raise ValueError("split")
        lines=set()
        for line in p["lines"]:
            if set(line)!={"line","tokens"}: raise ValueError("line schema")
            if not line["line"] or line["line"] in lines: raise ValueError("line id")
            lines.add(line["line"])
            for t in line["tokens"]:
                if set(t)!={"surface","units"}: raise ValueError("token schema")
                if not isinstance(t["surface"],str): raise ValueError("surface")
                if not isinstance(t["units"],list) or not t["units"]: raise ValueError("units")
                if any(not isinstance(u,str) or not u for u in t["units"]): raise ValueError("unit")
    return True

def canonical_bytes(stream):
    validate_stream(stream)
    return json.dumps({"schema":SCHEMA_VERSION,"pages":stream},
        ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()

def stream_sha256(stream):
    return hashlib.sha256(canonical_bytes(stream)).hexdigest()

def write_canonical(stream,path):
    Path(path).write_bytes(canonical_bytes(stream))
    return stream_sha256(stream)

def read_canonical(path):
    x=json.loads(Path(path).read_text(encoding="utf-8"))
    if x.get("schema")!=SCHEMA_VERSION: raise ValueError("schema")
    validate_stream(x["pages"]); return x["pages"]

def select_split(stream,split):
    if split not in SPLITS: raise ValueError(split)
    return [p for p in stream if p["split"]==split]

def inventory_counts(stream,split=None):
    c=Counter()
    pages=stream if split is None else select_split(stream,split)
    for p in pages:
        for line in p["lines"]:
            for t in line["tokens"]: c.update(t["units"])
    return c

def to_null_stream(stream):
    return [{"page":p["page"],
             "lines":[[list(t["units"]) for t in line["tokens"]] for line in p["lines"]]}
            for p in stream]
