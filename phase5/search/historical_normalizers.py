#!/usr/bin/env python3
from __future__ import annotations
import html,re,unicodedata

VOWELS={'a':'A','e':'E','i':'I','o':'O','u':'U','y':'I'}
BASE={'p':'P','b':'P','t':'T','d':'T','k':'K','g':'K','f':'F','v':'F','w':'W',
      's':'S','h':'H','m':'M','n':'N','l':'L','r':'R','j':'J','q':'K'}
CONS=set('PTKFSXHMNNYLRJW') | {'SH','NY','C_FRONT','G_FRONT'}

def _prep(token):
    token=html.unescape(html.unescape(token))
    token=unicodedata.normalize('NFC',token).lower().replace('ſ','s').replace('ß','ss').replace('œ','oe').replace('æ','ae')
    for a,b in {'ˢ':'s','ᵉ':'e','ᵃ':'a','ᵒ':'o','ⁱ':'i','ᵛ':'v','ᵘ':'u'}.items(): token=token.replace(a,b)
    # punctuation/editorial markup is ignored; alphabetic unknowns remain detectable.
    return ''.join(c for c in token if c.isalpha())

def _base_char(c):
    # Keep cedilla semantically distinct for French before stripping diacritics.
    if c=='ç': return 'ç'
    d=unicodedata.normalize('NFD',c)
    b=''.join(x for x in d if not unicodedata.combining(x))
    return b if len(b)==1 else c

def _collapse_input_doubles(w):
    if not w:return w
    out=[w[0]]
    for c in w[1:]:
        if c==out[-1] and c not in 'aeiouy': continue
        out.append(c)
    return ''.join(out)

def _collapse_consonant_outputs(seq):
    out=[]
    for x in seq:
        if out and x==out[-1] and x not in {'A','E','I','O','U'}: continue
        out.append(x)
    return out

def normalize(token,lang):
    w=_prep(token)
    if not w:return None
    if lang in ('WG','OIT'): w=_collapse_input_doubles(w)
    out=[];i=0
    while i<len(w):
        # Work with base letters for accent-bearing vowels/consonants.
        rem=w[i:]
        # digraphs/trigraphs are checked on accent-stripped ASCII-like view locally.
        plain=''.join(_base_char(c) for c in rem[:3])
        if lang=='WG':
            rules=[('sch',['SH']),('ch',['X']),('ph',['F']),('qu',['K','W']),('ck',['K']),
                   ('tz',['T','S']),('ng',['N','K']),('pf',['P','F'])]
        elif lang=='FR':
            rules=[('ch',['SH']),('gn',['NY']),('qu',['K']),('ph',['F']),('th',['T'])]
        elif lang=='OIT':
            rules=[('gn',['NY']),('qu',['K','W']),('ch',['K']),('gh',['K'])]
        elif lang=='LAT':
            rules=[('qu',['K','W']),('ph',['F']),('th',['T']),('ch',['K']),('x',['K','S']),('z',['T','S'])]
        else: raise ValueError(lang)
        hit=False
        for pat,val in rules:
            if plain.startswith(pat):
                out.extend(val);i+=len(pat);hit=True;break
        if hit:continue
        c=_base_char(w[i]); nxt=_base_char(w[i+1]) if i+1<len(w) else ''
        if lang=='WG' and c=='z': out.extend(['T','S']);i+=1;continue
        if lang=='FR':
            if c=='ç':out.append('S');i+=1;continue
            if c=='c':out.append('S' if nxt in 'eiy' else 'K');i+=1;continue
            if c=='g':out.append('SH' if nxt in 'eiy' else 'K');i+=1;continue
            if c=='j':out.append('SH');i+=1;continue
        if lang=='OIT':
            if c=='s' and nxt=='c' and i+2<len(w) and _base_char(w[i+2]) in 'ei':
                out.append('SH');i+=2;continue
            if c in ('c','g') and nxt in 'ei':out.append('SH');i+=1;continue
            if c=='z':out.extend(['T','S']);i+=1;continue
        if lang=='LAT':
            if c=='c':out.append('C_FRONT' if nxt in 'eiy' else 'K');i+=1;continue
            if c=='g':out.append('G_FRONT' if nxt in 'eiy' else 'K');i+=1;continue
        if c=='x':out.extend(['K','S']);i+=1;continue
        if c in VOWELS:out.append(VOWELS[c]);i+=1;continue
        if c in BASE:out.append(BASE[c]);i+=1;continue
        # Common orthographic c/z handling outside dedicated rules.
        if c=='c':out.append('K');i+=1;continue
        if c=='z':out.append('S');i+=1;continue
        return None
    if lang in ('WG','OIT'):out=_collapse_consonant_outputs(out)
    return out or None
