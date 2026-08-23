# Experiment 01 — First two pages as baseline repertoire

Date: 2026-08-23

## Question

If f1r and f1v are treated as the initial *bound-order* baseline, which STA glyph/block codes are already present, and which codes first appear immediately afterwards?

This is **not** yet a claim about production chronology.

## Data

Primary transliteration:

- René Zandbergen, Reference Transliteration RF1b
- Alphabet: reduced STA1
- Format: IVTFF 2.0
- Source: https://www.voynich.nu/data/sta/RF1b.txt
- STA definition: https://www.voynich.nu/data/sta/STA1_def.pdf

## Baseline result

Parsing each STA unit as `[A-Z][0-9a-z]`:

| Region | STA units | Distinct STA codes |
|---|---:|---:|
| f1r | 739 | 41 |
| f1v | 317 | 27 |
| f1r + f1v | 1056 | 43 |

Only two STA codes occur in f1v that were not already present on f1r:

- `B5`
- `D1`

This must be normalized for the larger amount of text on f1r.

## First post-baseline innovations in bound order

| First locus | STA | STA/EVA interpretation | RF1b total | Class |
|---|---|---|---:|---|
| f2r.4 | `Lo` | `{c'o}` | 4 | rare composite/ligature |
| f2r.10 | `Da` | `q'` | 10 | rare q-family variant |
| f2r.10 | `Ae` | `a'` (below) | 4 | rare a-family variant |
| f2v.2 | `M1` | `eee` | 431 | repeated block, not a new primitive stroke |
| f2v.5 | `Ub` | `{cko}` | 2 | rare composite/ligature |
| f3r.1 | `B4` | EVA `g` | 165 | distinct candidate glyph |
| f3r.9 | `Xb` | rare special form | 6 | rare/special glyph |
| f3v.4 | `M2` | `eeb` | 9 | composite block |
| f3v.9 | `N1` | `eeee` | 13 | repeated block |

## Methodological finding

Synthetic STA intentionally treats some ligatures and repeated sequences as single codes. Therefore:

    "new STA code" != "new primitive glyph"

Novelty must be run at two levels:

1. synthetic gesture/block novelty — STA;
2. primitive stroke novelty — analytical alignment alphabet (aaa) and direct image morphology.

## Candidate 1: B4 / EVA-g

B4 is currently the best first morphology probe because it:

- is absent from f1r/f1v and f2r/f2v;
- is first recorded at f3r.1;
- occurs 165 times in RF1b;
- appears while the early pages are still marked `H=1` in RF1b metadata.

The analytical representation of EVA-g is `c2:j1`, so direct image comparison is required before calling it a newly invented primitive.

## Next test

Build an image sample for B4:

- earliest 10–20 occurrences;
- middle 10–20 occurrences from the same proposed hand;
- late 10–20 occurrences from the same proposed hand;
- matched control glyph already common on f1r.

Measure width/height, slant, loop geometry, stroke curvature, component placement, baseline relation, and within-period variance.

## Current conclusion

No decipherment conclusion.

The first pages already contain a broad repertoire, while additional variants and composites begin appearing immediately afterwards. Both a pre-existing system with rare forms and an evolving system remain viable.
