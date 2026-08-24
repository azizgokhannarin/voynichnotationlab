#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument("file",type=Path)
ap.add_argument("--md5")
ap.add_argument("--sha256")
a=ap.parse_args()
data=a.file.read_bytes()
got_md5=hashlib.md5(data).hexdigest()
got_sha=hashlib.sha256(data).hexdigest()
print("MD5",got_md5)
print("SHA256",got_sha)
if a.md5 and got_md5.lower()!=a.md5.lower():
    raise SystemExit("published MD5 mismatch")
if a.sha256 and got_sha.lower()!=a.sha256.lower():
    raise SystemExit("published SHA256 mismatch")
