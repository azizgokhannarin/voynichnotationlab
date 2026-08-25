#!/usr/bin/env python3
import sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"search"))
from structural_serializer import *
s=[
 {"page":"p1","split":"train","lines":[{"line":"p1.1","tokens":[{"surface":"qa","units":["QO","a"]}]}]},
 {"page":"p2","split":"validation","lines":[{"line":"p2.1","tokens":[{"surface":"dy","units":["d","y"]}]}]},
 {"page":"p3","split":"final_test","lines":[{"line":"p3.1","tokens":[{"surface":"or","units":["o","r"]}]}]}]
assert validate_stream(s)
h=stream_sha256(s)
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/"x.json"; assert write_canonical(s,p)==h; assert read_canonical(p)==s
assert inventory_counts(s,"train")["QO"]==1
print("STRUCTURAL SERIALIZER: PASS")
print("SHA256",h)
