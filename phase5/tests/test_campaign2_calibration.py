#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"search"))

from campaign2_calibration import *

TOKENS=[
 ["A","N"],["K","A","N"],["S","A","R"],["A","R"],
 ["K","A","R"],["S","A","N"],["A","N"],["K","A","N"]
]*20

enc,key=build_positive_encoding(TOKENS,"TEST",37)
enc2,key2=build_positive_encoding(TOKENS,"TEST",37)
assert enc==enc2 and key==key2
assert token_lengths(enc)==token_lengths(TOKENS)

neg=build_negative_matched(TOKENS,"TEST")
neg2=build_negative_matched(TOKENS,"TEST")
assert neg==neg2
assert token_lengths(neg)==token_lengths(TOKENS)
assert global_counts(neg)==global_counts(TOKENS)

# Negative should usually differ from original sequence organization.
assert neg != TOKENS

print("CAMPAIGN2 CALIBRATION GENERATORS: PASS")
print("positive mapping size:",len(key))
print("negative global-count preservation:",global_counts(neg)==global_counts(TOKENS))
