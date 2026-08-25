#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'search'))
from historical_normalizers import normalize
cases=[
 ('WG','schaf',['SH','A','F']),('WG','nacht',['N','A','X','T']),('WG','quell',['K','W','E','L']),
 ('WG','tz',['T','S']),('WG','z',['T','S']),('WG','singen',['S','I','N','K','E','N']),('WG','pferd',['P','F','E','R','T']),
 ('FR','chose',['SH','O','S','E']),('FR','agneau',['A','NY','E','A','U']),('FR','qui',['K','I']),
 ('FR','ce',['S','E']),('FR','ca',['K','A']),('FR','ge',['SH','E']),('FR','je',['SH','E']),('FR','façon',['F','A','S','O','N']),
 ('OIT','che',['K','E']),('OIT','ghi',['K','I']),('OIT','gn',['NY']),('OIT','qui',['K','W','I']),
 ('OIT','ce',['SH','E']),('OIT','ge',['SH','E']),('OIT','sci',['SH','I']),('OIT','z',['T','S']),('OIT','notte',['N','O','T','E']),
 ('LAT','qu',['K','W']),('LAT','ph',['F']),('LAT','th',['T']),('LAT','ch',['K']),('LAT','x',['K','S']),('LAT','z',['T','S']),
 ('LAT','ce',['C_FRONT','E']),('LAT','ge',['G_FRONT','E']),('LAT','ca',['K','A'])]
for lang,src,want in cases:
    got=normalize(src,lang);assert got==want,(lang,src,got,want)
print('HISTORICAL NORMALIZER RULE TESTS: PASS',len(cases))
