# Campaign 1 — Frozen Historical Phonographic Normalization v1

Date frozen: 2026-08-25

Status: **FROZEN BEFORE MAPPING SEARCH**

## 1. Purpose

The historical corpora are not compared to Voynich by modern spelling.

At the same time, exact IPA reconstruction for every place and decade from 1300–1500 is not
sufficiently certain to use as if it were ground truth.

Campaign 1 therefore uses **coarse historical phonographic classes**.

These classes preserve robust sound-structure information while merging distinctions whose
historical realization is uncertain.

The normalizer is part of the target-language model and is fixed before Voynich mappings are
optimized.

---

# 2. Universal class inventory

Primary consonant classes:

- `P`  labial stop class: p/b where voicing is intentionally collapsed
- `T`  coronal stop class: t/d
- `K`  dorsal stop class: k/g and hard c where appropriate
- `F`  labial fricative class: f/v where historical voicing is unstable
- `S`  sibilant class: s/z and language-specific close variants
- `SH` postalveolar/palatal sibilant class
- `X`  velar/palatal fricative class
- `H`  glottal/laryngeal class
- `M`
- `N`
- `NY` palatal nasal
- `L`
- `R`
- `J`  palatal glide
- `W`  labial glide

Primary vowel classes:

- `A`
- `E`
- `I`
- `O`
- `U`

Optional length/quality feature:
- long/short or open/close vowel distinctions are retained only when the corpus
  transcription reliably marks them.
- otherwise they collapse to the base vowel class.

Diphthongs remain ordered two-vowel sequences unless a language-specific rule below freezes
them as one class.

Voicing is deliberately collapsed in the primary Campaign-1 normalizer. A voiced/unvoiced
robustness normalizer may be run only after the primary result is frozen.

---

# 3. Shared preprocessing

Applied identically before language-specific rules:

1. Unicode NFC.
2. Lowercase.
3. Remove punctuation and editorial markup.
4. Preserve corpus token boundaries.
5. Remove tokens marked foreign where available.
6. Do not use lemmas as the phonographic stream.
7. Expand editorial abbreviations only if the corpus provides an explicit normalized expansion.
8. Treat `i/j` and `u/v` according to the source's normalized/transcribed layer rather than
   manually reconstructing scribal shape distinctions.
9. No rule may inspect Voynich data.

---

# 4. West Germanic normalizer

Primary input:
- ReF normalized/annotated word layer;
- ReN normalized/annotated word layer.

Frozen high-confidence grapheme groups:

- `sch` -> SH
- `ch` -> X
- `ph` -> F
- `qu` -> K W
- `ck` -> K
- `tz`, `z` in affricate spellings -> T S
- `ng` -> N K as the conservative primary representation
- `pf` -> P F
- `sp`, `st` remain S+P / S+T rather than automatically modernizing to SH

Single consonant letters map to their broad universal classes.

Repeated consonant spelling does not create a doubled phoneme in the primary model.

Vowels map to A/E/I/O/U classes.
Historically variable diphthong spellings remain ordered vowel sequences.

No modern Standard-German pronunciation rule is imported automatically.

---

# 5. Romance normalizers

## 5.1 Medieval French / BFM

Frozen coarse rules:

- `ch` -> SH
- `gn` -> NY
- `qu` -> K
- `ph` -> F
- `th` -> T
- `c` before front vowel -> S; otherwise K
- `g` before front vowel -> J/SH-like palatal class represented as SH
- `j` -> J/SH-like class represented as SH
- `ill` between vowels may map to J only in the explicitly defined normalizer rule;
  otherwise L is retained
- written final consonants are retained in the primary representation rather than
  silently deleted, because medieval realization is date/dialect dependent

Nasal-vowel spelling is not converted to a modern French nasal vowel. It remains
vowel + N/M class unless a later preregistered robustness model is used.

## 5.2 Old Italian / DanteSearch

Frozen coarse rules:

- `ch` -> K
- `gh` -> K
- `gn` -> NY
- `qu` -> K W
- `ci`, `ce` -> SH-like affricate/sibilant class represented as SH
- `gi`, `ge` -> SH-like voiced counterpart, voicing-collapsed to SH
- `sc` before front vowel -> SH
- `z` -> T S broad affricate sequence
- double consonants collapse to the same consonant class in the primary model

Vowels map transparently to A/E/I/O/U.

---

# 6. West Slavic / Old Czech normalizer

Primary input:
- Staročeská textová banka transcribed layer.

Because the bank is transcribed into modern Czech orthographic conventions, use a conservative
Czech grapheme-to-class map:

- `č` -> SH
- `š` -> SH
- `ž` -> SH
- `ň` -> NY
- `ch` -> X
- `ř` -> R + SH as a conservative two-feature representation
- `c` -> T S
- `j` -> J
- `y` and `i` -> I
- `ě` -> J + E
- `ou` -> O U
- voiced/unvoiced obstruent distinctions collapse into broad P/T/K/F/S classes

No modern phonological process such as automatic final devoicing is separately applied,
because voicing is already collapsed.

---

# 7. Latin normalizer

Latin in 1300–1500 had strong regional pronunciation variation.

Campaign 1 therefore uses a conservative **orthographic-phonographic** normalizer rather than
claiming one universal medieval Latin pronunciation.

Frozen rules:

- `qu` -> K W
- `ph` -> F
- `th` -> T
- `ch` -> K
- `x` -> K S
- `z` -> T S
- `c` before e/i/y -> ambiguity collapsed to the broad `K/S` front-c class,
  encoded as `C_FRONT`
- `g` before e/i/y -> `G_FRONT`
- other `c/g` -> K
- `j/i` consonantal distinction follows normalized source spelling where available;
  otherwise `i` remains I
- `u/v` follows normalized source spelling where available

The special classes `C_FRONT` and `G_FRONT` are legal target classes in Latin only and count
as one normalizer class, not as a free Voynich context-sensitive mapping.

A robustness pass may instantiate them as regional values only after the primary Latin score
is frozen.

---

# 8. Why the classes are deliberately coarse

Campaign 1 asks first:

> Does the Voynich representation fit the *phonotactic architecture* of one historical
> language zone better than others?

It does not yet ask:

> Can every Voynich symbol be assigned a precise IPA phoneme?

Coarse classes reduce false negatives caused by uncertain historical voicing and regional
pronunciation while still preserving:

- consonant/vowel sequencing;
- sonority/rime patterns;
- affricate/sibilant structure;
- onset and coda constraints;
- recurring phonographic neighborhoods.

---

# 9. Normalizer validation before Voynich search

Each normalizer must pass three checks on its own corpus:

1. no more than 1% of alphabetic tokens are dropped as unhandled;
2. class inventory and token-length statistics are recorded;
3. round-trip inspection of at least 200 randomly sampled words is completed for obvious
   rule bugs.

These checks inspect only the historical corpus, never Voynich output.

---

# 10. Frozen normalizer IDs

- `PHONO-WG-v1`
- `PHONO-FR-v1`
- `PHONO-OIT-v1`
- `PHONO-OCZ-v1`
- `PHONO-LAT-v1`

Any altered rule set receives a new ID and cannot replace v1 inside Campaign 1 after language
mapping scores have been observed.
